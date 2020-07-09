from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from tickets.factories import TicketFactory

from tenders.models import Tender


class TenderFactory(DjangoModelFactory):
    ikz = Sequence(lambda n: str(n))
    num = Sequence(lambda n: str(n))
    smp = False
    ticket = SubFactory(TicketFactory)

    class Meta:
        model = Tender
