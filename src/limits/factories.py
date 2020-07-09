from factory import Faker, LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory

from limits.models import (IndustryCode, Limit, LimitArticle, LimitDateInfo,
                           LimitMoney, Source)


class LimitFactory(DjangoModelFactory):
    year = Sequence(lambda n: 2000 + n)

    class Meta:
        model = Limit


class SourceFactory(DjangoModelFactory):
    num = Sequence(lambda n: n)
    name = Sequence(lambda n: str(n))
    limit = SubFactory(LimitFactory)

    class Meta:
        model = Source


class LimitArticleFactory(DjangoModelFactory):
    num = Sequence(lambda n: n)
    name = Sequence(lambda n: str(n))
    source = SubFactory(SourceFactory)

    class Meta:
        model = LimitArticle


class IndustryCodeFactory(DjangoModelFactory):
    num = Sequence(lambda n: n)
    name = Sequence(lambda n: str(n))
    limit_article = SubFactory(LimitArticleFactory)

    class Meta:
        model = IndustryCode


class LimitMoneyFactory(DjangoModelFactory):
    name = Sequence(lambda n: str(n))
    subsidy_code = Sequence(lambda n: str(n))
    money = Faker(
        'pydecimal', left_digits=9, right_digits=2, min_value=1,
        max_value=999_000_000,
    )
    industry_code = SubFactory(IndustryCodeFactory)

    class Meta:
        model = LimitMoney


class LimitDateInfoFactory(DjangoModelFactory):
    limit = SubFactory(LimitFactory)
    data = LazyAttribute(lambda o: {})

    class Meta:
        model = LimitDateInfo
