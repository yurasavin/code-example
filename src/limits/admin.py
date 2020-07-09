from django.contrib import admin

from limits import models

# TODO: add raw_id_fields
admin.site.register(models.Limit)
admin.site.register(models.LimitDateInfo)
admin.site.register(models.Source)
admin.site.register(models.LimitArticle)
admin.site.register(models.IndustryCode)
admin.site.register(models.LimitMoney)
admin.site.register(models.Debt)
