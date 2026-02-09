from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CreditReport, RequestedReport

admin.site.register(CreditReport)
admin.site.register(RequestedReport)