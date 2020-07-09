from celery import chain, shared_task
from celery.utils.log import get_task_logger

from django.db import models
from django.db.models.functions import Coalesce

from contracts.models import Contract

from prices.models import ContractPrice

from tenders.models import Tender

logger = get_task_logger(__name__)


@shared_task(name='update_prices_flow')
def update_prices_flow():
    chain(
        update_contracts_prices.s(),
        update_tenders_prices.s(),
    ).apply_async()


@shared_task(name='update_contracts_prices')
def update_contracts_prices():
    aggregated_prices = ContractPrice.objects.filter(
        contract_id=models.OuterRef('pk')).annotate(
        price=models.ExpressionWrapper(
            models.F('money') + Coalesce(
                models.Sum('contractpricechange__delta'),
                models.Value(0),
            ),
            output_field=models.DecimalField(max_digits=11, decimal_places=2),
        ),
    ).values('price')[:1]
    Contract.objects.filter(tender__status=Tender.Status.IN_WORK) \
        .update(price=models.Subquery(aggregated_prices))


@shared_task(name='update_tenders_prices')
def update_tenders_prices():
    start_prices = (
        ContractPrice.objects
            .filter(contract__tender__id=models.OuterRef('pk'))  # noqa: E131
            .values('contract__tender__id')
            .annotate(price=models.Sum('money'))
            .values('price')[:1]
    )
    contract_price = (
        Contract.objects.filter(tender__id=models.OuterRef('pk'))
            .values('tender__id')  # noqa: E131
            .annotate(total_money=models.Sum('contractprice__money'))
            .values('total_money')[:1]
    )
    Tender.objects.filter(status=Tender.Status.IN_WORK).update(
        price=Coalesce(models.Subquery(start_prices), models.Value(0)),
        economy=Coalesce(
            models.Subquery(start_prices) - models.Subquery(contract_price),
            models.Value(0),
            output_field=models.DecimalField(max_digits=11, decimal_places=2),
        ),
    )
