from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from tenders.factories import TenderFactory

from contracts.factories import ContractChangeFactory, ContractFactory

from prices.models import ContractPrice, ContractPriceChange, StartPrice


class StartPriceFactory(DjangoModelFactory):
    money = Faker(
        'pydecimal', left_digits=7, right_digits=2, min_value=1,
        max_value=5_000_000,
    )
    tender = SubFactory(TenderFactory)

    class Meta:
        model = StartPrice


class ContractPriceFactory(DjangoModelFactory):
    money = Faker(
        'pydecimal', left_digits=7, right_digits=2, min_value=1,
        max_value=5_000_000,
    )
    start_price = SubFactory(StartPriceFactory)
    contract = SubFactory(ContractFactory)

    class Meta:
        model = ContractPrice


class ContractPriceChangeFactory(DjangoModelFactory):
    change = SubFactory(ContractChangeFactory)
    price = SubFactory(ContractPriceFactory)
    delta = Faker(
        'pydecimal', left_digits=7, right_digits=2, min_value=1,
        max_value=1_000_000,
    )

    class Meta:
        model = ContractPriceChange
