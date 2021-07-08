from django.contrib import admin
from .models import Employee, Service, Customer, Invoice, InvoiceServices
# Register your models here.

admin.site.register([Employee, Service, Customer, InvoiceServices, Invoice])