from django.contrib import admin

from contracts.models import Contract, ContractChange

admin.site.register(Contract)
admin.site.register(ContractChange)
