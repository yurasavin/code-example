from factory import Faker
from factory.django import DjangoModelFactory

from tickets.models import Ticket


class TicketFactory(DjangoModelFactory):
    name = Faker('word')
    date = Faker('date')

    class Meta:
        model = Ticket
