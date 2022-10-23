from django import forms
from django.forms import formset_factory
from .models import *
from django.forms.models import inlineformset_factory


class InvoiceForm(forms.Form):
    customer_id = forms.ModelChoiceField(required=True,queryset=Customer.objects.only('customer_id'))    
    invoice_id = forms.CharField(required=True)
    due_date = forms.DateTimeField()
    message = forms.CharField(required=True)


# class InvoiceForm(forms.Form):
    
       
#     customer_id = forms.CharField(
#         label='Customer id',
        
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Customer id',
#             'rows':1    
#         }
        
#     )
#     )
#     invoice_id = forms.CharField(
#         label='Invoice Id',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Invoice Id',
#             'rows':1
#         })
#     )
#     total_amount = forms.CharField(
#         label='Total amount',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Total amount',
#             'rows':1
#         })
#     )

class LineItemFormIndi(forms.Form):
    serial_number = forms.CharField(required=True)
    
    
   

class LineItemForm(forms.Form):
    
    service = forms.CharField(
        label='Service/Product',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Service Name'
        })
    )
    
    pid = forms.CharField(
        label='Product Id',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'P Id'
        })
    )
    
    description = forms.CharField(
        label='Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter Book Name here',
            "rows":1
        })
    )
    quantity = forms.IntegerField(
        label='Qty',
        widget=forms.TextInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'
        }) #quantity should not be less than one
    )
    rate = forms.DecimalField(
        label='Rate $',
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Rate'
        })
    )



    
    # amount = forms.DecimalField(
    #     disabled = True,
    #     label='Amount $',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #     })
    # )
    
LineItemFormset = formset_factory(LineItemForm, extra=1)

class Product_update_form(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['service','description','quantity','rate']

AuthorBooksFormset = inlineformset_factory(Invoice,LineItem, fields=('service',))

class OrderForm(forms.ModelForm):
	class Meta:
		model = LineItem
		fields = '__all__'
  
  
class Customer_creation(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'