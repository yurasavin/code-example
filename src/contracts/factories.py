from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory

from contracts.models import Contract, ContractChange

from tenders.factories import TenderFactory

from tickets.factories import TicketFactory


class ContractFactory(DjangoModelFactory):
    tender = SubFactory(TenderFactory)
    num = Sequence(lambda n: str(n))
    date = Faker('date')
    specif = Faker('paragraph')
    ticket = SubFactory(TicketFactory)
    bank_guar = False
    pledge = 0
    kontragent = Faker('company')

    class Meta:
        model = Contract


class ContractChangeFactory(DjangoModelFactory):
    contract = SubFactory(ContractFactory)
    num = Sequence(lambda n: str(n))
    date = Faker('date')

    class Meta:
        model = ContractChange
