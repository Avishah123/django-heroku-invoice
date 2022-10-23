from django.contrib import admin

from .models import Invoice, LineItem,Customer,Ledger

admin.site.register(Invoice)
admin.site.register(LineItem)
admin.site.register(Customer)
admin.site.register(Ledger)
# Register your models here.
