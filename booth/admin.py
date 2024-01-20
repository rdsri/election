from django.contrib import admin

# Register your models here.
from .models import ParlimentReport, CasteReport

admin.site.register(ParlimentReport)
admin.site.register(CasteReport)