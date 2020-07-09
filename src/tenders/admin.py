from django.contrib import admin

from tenders.models import Tender

# TODO: add raw_id_fields
admin.site.register(Tender)
