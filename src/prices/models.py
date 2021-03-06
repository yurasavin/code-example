from django.db import models


class AbstractPrice(models.Model):
    money = models.DecimalField('Сумма', max_digits=11, decimal_places=2)
    limit = models.ForeignKey('limits.LimitMoney', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.money)


class StartPrice(AbstractPrice):
    tender = models.ForeignKey('tenders.Tender', on_delete=models.CASCADE)


class ContractPrice(AbstractPrice):
    start_price = models.OneToOneField(StartPrice, null=True, blank=True,
                                       on_delete=models.CASCADE)
    contract = models.ForeignKey('contracts.Contract',
                                 on_delete=models.CASCADE)


class ContractPriceChange(models.Model):
    delta = models.DecimalField(max_digits=11, decimal_places=2)
    change = models.ForeignKey('contracts.ContractChange',
                               on_delete=models.CASCADE)
    price = models.ForeignKey(ContractPrice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.delta)
