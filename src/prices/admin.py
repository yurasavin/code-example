from django.contrib import admin

from prices.models import ContractPrice, ContractPriceChange, StartPrice

# TODO: add raw_id_fields
admin.site.register(StartPrice)
admin.site.register(ContractPrice)
admin.site.register(ContractPriceChange)
