from random import shuffle

from django.core.management import BaseCommand
from django.db import transaction

from limits.factories import (IndustryCodeFactory, LimitArticleFactory,
                              LimitFactory, LimitMoneyFactory, SourceFactory)
from limits.models import Limit
from limits.tasks import update_limit_info

from prices.factories import (ContractPriceChangeFactory, ContractPriceFactory,
                              StartPriceFactory)

from tickets.models import Ticket


class Command(BaseCommand):
    help = 'Remove current Limits and create random data for test project'

    @transaction.atomic
    def handle(self, *args, **options):
        Limit.objects.all().delete()
        Ticket.objects.all().delete()

        limit_money_ids = self._create_limits()
        self.stdout.write(self.style.SUCCESS('Limits created!'))

        shuffle(limit_money_ids)
        chunk_size = int(len(limit_money_ids) * 0.5)
        part1 = limit_money_ids[:chunk_size]
        part2 = limit_money_ids[chunk_size:]

        self._create_tenders(part1)
        self.stdout.write(self.style.SUCCESS('Tenders created!'))

        self._create_contracts(part2)
        self.stdout.write(self.style.SUCCESS('Contracts created!'))

        self._create_limit_info()
        self.stdout.write(self.style.SUCCESS('Limit info created!'))

    def _create_limits(self):
        limit_money_ids = []
        limits = LimitFactory.create_batch(2)

        for limit in limits:

            sources = SourceFactory.create_batch(3, limit=limit)

            for source in sources:
                articles = LimitArticleFactory.create_batch(3, source=source)

                for article in articles:
                    ind_codes = IndustryCodeFactory.create_batch(
                        3, limit_article=article)

                    for ind_code in ind_codes:
                        limit_moneys = LimitMoneyFactory.create_batch(
                            3, industry_code=ind_code)

                        limit_money_ids.extend(
                            (obj.id for obj in limit_moneys))

        return limit_money_ids

    def _create_tenders(self, limit_money_ids):
        for limit_money_id in limit_money_ids:
            StartPriceFactory.create_batch(4, limit_id=limit_money_id)

    def _create_contracts(self, limit_money_ids):
        chunk_size = int(len(limit_money_ids) * 0.45)
        part1 = limit_money_ids[:chunk_size]
        part2 = limit_money_ids[chunk_size:chunk_size * 2]
        part3 = limit_money_ids[chunk_size * 2:]

        for limit_money_id in part1:
            ContractPriceFactory.create_batch(
                4, start_price__limit_id=limit_money_id,
                limit_id=limit_money_id)

        for limit_money_id in part2:
            ContractPriceFactory.create_batch(
                4, start_price=None, limit_id=limit_money_id)

        for limit_money_id in part3:
            ContractPriceChangeFactory.create_batch(
                4, price__start_price=None,
                price__limit_id=limit_money_id)

    def _create_limit_info(self):
        for id_ in Limit.objects.values_list('id', flat=True).order_by('id'):
            update_limit_info(id_)
