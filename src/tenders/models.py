from django.db import models
from django.utils.translation import gettext_lazy as _


class Tender(models.Model):
    class Status(models.TextChoices):
        IN_WORK = 'in_work', _('In work')
        DONE = 'done', _('Done')
        ZERO = 'zero', _('Zero')
        CANCEL = 'cancel', _('Cancelled')

    ikz = models.CharField(max_length=36, blank=True)
    num = models.CharField(max_length=19, unique=True)
    status = models.CharField(max_length=20, blank=True,
                              choices=Status.choices,
                              default=Status.IN_WORK.value)
    smp = models.BooleanField()
    ticket = models.OneToOneField('tickets.Ticket', on_delete=models.CASCADE)

    # aggregated fields
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0,
                                editable=False)
    economy = models.DecimalField(max_digits=11, decimal_places=2, default=0,
                                  editable=False)

    def __str__(self):
        return f'{self.num}; {self.price}'
