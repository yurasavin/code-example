from django.db import models


class Ticket(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, db_index=True)

    status = models.BooleanField(max_length=10, default=True)
    year = models.ManyToManyField('limits.Limit', db_index=True)

    def __str__(self):
        return self.name
