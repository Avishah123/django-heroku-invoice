from django.contrib import admin
from django.urls import path
from .views import InvoiceListView, createInvoice, generate_PDF, view_PDF
from .views import *
from django.contrib.auth import views as auth_views
app_name = 'invoice'

urlpatterns = [
    path('', InvoiceListView.as_view(), name="invoice-list"),
    path('create/', createInvoiceNew, name="invoice-create"),
    path('invoice-detail/<id>', view_PDF, name='invoice-detail'),
    path('invoice-download/<id>', generate_PDF, name='invoice-download'),
    path('update/<int:pk>',
         invoiceupdate.as_view(),name='invoiceupdate'),
    path('productupdate/<int:pk>',
         productupdate.as_view(),name='productupdate'),


    path('test/<customer>',product_view,name='test'),
    path('edit/<customer>',edit_product, name="edit_product"),

    path('update_order/<customer>/', createOrder, name="update_order"),
    path('testnew/', customer_view, name="update_order"),
    path('testp/<id>',invoice_view_new,name="testp"),
    path('update_order1/<id>/', createOrderNew, name="update_order1"),
    path('delete_item/<id>/', delete_lineitem, name="delete_item"),
    path('update_item/<int:id>/', update_lineitem, name="update_item"),
    path('formset',formset_view,name="formset"),
    path('create_new/', createInvoiceNew2, name="invoice-create_new"),
    path('ledger/<customer_id>', total_amount_aggregator, name="total_amount_aggregator"),
    path('ledger_view', ledger_view, name="ledger_view"),
    path('ledger_view/<customer_id>', ledger_item, name="ledger_item"),
    
    
]
