from django.forms.models import ModelForm, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import Customer, LineItem, Invoice , LineItemIndi ,Ledger
from .forms import LineItemFormset, InvoiceForm, Product_update_form, AuthorBooksFormset, OrderForm ,Customer_creation , LineItemForm , LineItemFormIndi
from django.views import generic
import pdfkit
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, CreateView, DetailView, FormView)

from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.forms import formset_factory

from django.http import JsonResponse
# Things to be added 
# 1. To add the functionlity to select a user using dropdown or else they can create a new customer
# Solution for 1.  we will provide a button which will redirect to creating a new user and then go back to the creaation form 
# Create a new model known as customers and then link it to line items and invoice using foreign key
# 2. To add the functionality to remove an object from the formset 
# Add discount and tax functionality s

class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices": invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)

    def post(self, request):
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))
        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')


class invoiceupdate(generic.UpdateView):
    model = Invoice
    template_name = 'invoice/test.html'
    fields = ['customer_email', 'billing_address', 'message']
    success_url = reverse_lazy('invoice:invoice-list')


class productupdate(generic.UpdateView):
    model = LineItem
    template_name = 'invoice/test.html'
    fields = ['customer', 'service', 'description',
        'quantity', 'rate', 'amount']

    success_url = reverse_lazy('invoice:invoice-list')


def createInvoice(request):
   
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                    customer_email=form.data["customer_email"],
                    billing_address=form.data["billing_address"],
                    date=form.data["date"],
                    due_date=form.data["due_date"],
                    message=form.data["message"],
                    )
           
        if formset.is_valid():
            
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        # "customer" : Invoice.objects.values('customer'),
    }
    return render(request, 'invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, invoice_id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "AviTech ",
            "address": "xyz lane , Mumbai ",
            "phone": "(916) XXX XXXX",
            "email": "contact@avitech.com",
        },
        "invoice_id": invoice.invoice_id,
        "invoice_total": invoice.total_amount,
        
        
        
        "due_date": invoice.due_date,
        "message": invoice.message,
        "lineitem": lineitem,

    }
    return render(request, 'invoice/pdf_template.html', context)


def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response


def change_status(request):
    return redirect('invoice:invoice-list')


def view_404(request,  *args, **kwargs):
    return redirect('invoice:invoice-list')


def product_view(request, customer):
    invoice = LineItem.objects.filter(
        customer=Invoice.objects.get(customer=customer))
    # invoice= LineItem.objects.all()
    for inst in invoice:
        print(inst.id)

    return render(request, 'invoice/test2.html', {'invoice': invoice})


def edit_product(request, customer):
    template = 'invoice/test3.html'
    book = get_object_or_404(
        LineItem, customer=Invoice.objects.get(customer=customer))
    form = Product_update_form(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {"form": form}
    return render(request, 'invoice/test.html', context)


def updateOrder(request, customer):
    order = LineItem.objects.filter(
        customer=Invoice.objects.get(customer=customer))
    print(order)
    array = []
    for i in order:
        print(i.id)
        form = OrderForm(instance=(i))
        array.append(form)

        if request.method == 'POST':
            form = OrderForm(request.POST, instance=i)

            if form.is_valid():
                form.save()

    print(array)
    context = {'form': array}

    return render(request, 'invoice/order_form.html', context)


def createOrder(request, customer):
    OrderFormSet = modelformset_factory(LineItem, fields=('rate', 'description'),extra=0)
    formset = OrderFormSet(queryset=LineItem.objects.filter(
        customer=Invoice.objects.get(customer=customer)))
    
    query1 = queryset=LineItem.objects.filter(
        customer=Invoice.objects.get(customer=customer))
    
    if request.method == 'POST':

        formset = OrderFormSet(request.POST)

        if formset.is_valid():
            
            formset.save()
            sum1=0
            query2 = queryset=LineItem.objects.filter(customer=Invoice.objects.get(customer=customer))
            for i in query2:
                sum1 += i.amount
                print(sum1)
            invoice = Invoice.objects.get(customer=customer)
            invoice.total_amount = sum1
            invoice.save()

            return redirect('/')

    context = {'formset':formset}
    
    return render(request, 'invoice/order_form.html',{'formset':formset})


def customer_view(request):
    context ={} 
    # create object of form
    form = Customer_creation(request.POST or None, request.FILES or None)
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        customer_id = form.cleaned_data.get('customer_id')
        print(customer_id)
        form.save()
        x = Ledger.objects.create(customer_id_id=customer_id,total_amount=0)
        x.save()
        return redirect('/')
    
    
        
    context['form']= form
    
    return render(request, 'invoice/test4.html',context)


def createInvoiceNew(request):
    obj2 = LineItem.objects.values('invoice_id')
    print(obj2)

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid():
            print('inside first form')
            invoice = Invoice.objects.create(customer_id=form.cleaned_data.get('customer_id'),
                    invoice_id=form.data["invoice_id"],                                        
                    due_date=form.data["due_date"],
                    message=form.data["message"],
                    )
            print('the customer_id',invoice.customer_id)
        if formset.is_valid():
            total = 0
            for form in formset:
                
                pid = form.cleaned_data.get('pid')
                invoice_id = form.cleaned_data.get('invoice_id')
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    print('inside first2 form')
                    print('the quantity of the product is: ',quantity)
                    amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(pid=pid,invoice_id=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            print('total amount of this one is : ',total)
            x = Ledger.objects.get(customer_id_id=invoice.customer_id)
            x.total_amount = float(x.total_amount) + float(total)
            x.save()
            invoice.total_amount = total
            print('total amount of this one in db : ',invoice.total_amount)           
            
            invoice.save()

            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')

    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def invoice_view_new(request,id):
    invoice = LineItem.objects.filter(invoice_id=id)
    for i in invoice:
        print(i)   
    return render(request, 'invoice/lineitem_details.html', {'invoice': invoice})
        
        
def delete_lineitem(request,id=None):
    obj = get_object_or_404(LineItem, pid=id)
    obj2 = LineItem.objects.values_list('invoice_id')
    print(obj2)
    
    
    if request.method =="POST":
        obj.delete()
                        
        return HttpResponseRedirect("/")
    return render(request, 'invoice/delete.html')


def update_lineitem(request,id=None):
    obj = get_object_or_404(LineItem, id=id)
    form = LineItemForm(request.POST)
    if request.method == 'POST':
        form = LineItemForm(request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    
    return render(request, 'invoice/update.html',context = {"form": form})


def createOrderNew(request, id):
    OrderFormSet = modelformset_factory(LineItem, fields=('service','quantity','rate', 'description'),extra=0)
    formset = OrderFormSet(queryset=LineItem.objects.filter(invoice_id=id))
   
    query1 = LineItem.objects.filter(invoice_id=id)
    if request.method == 'POST':
        print('into the post 1')
        formset = OrderFormSet(request.POST)
        if formset.is_valid():
            print('into the post 2')
            
            formset.save()
            sum1=0
            query2 = LineItem.objects.filter(invoice_id=id)
            for i in query2:
                sum1 += i.amount
                print(sum1)
            invoice = Invoice.objects.get(invoice_id=id)
            invoice.total_amount = sum1
            invoice.save()
        
            return redirect('/')
    
    return render(request, 'invoice/order_form.html',{'formset':formset})


def createInvoiceNew2(request):
    GeeksFormSet = formset_factory(LineItemFormIndi)

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
        # form2 = GeeksFormSet(request.GET or None)
        GeeksFormSet = formset_factory(LineItemFormIndi)
        
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        # form2 = GeeksFormSet(request.POST)
        GeeksFormSet = formset_factory(LineItemFormIndi)
        
        if form.is_valid():
            invoice = Invoice.objects.create(customer_id=form.cleaned_data.get('customer_id'),
                    invoice_id=form.data["invoice_id"],
                                        
                    due_date=form.data["due_date"],
                    message=form.data["message"],
                    )

        if formset.is_valid():
           
            total = 0
            for form in formset:
                invoice_id = form.cleaned_data.get('invoice_id')
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    GeeksFormSet = formset_factory(LineItemFormIndi, extra =quantity)
                    
                    if GeeksFormSet.is_valid():
                        for form2 in GeeksFormSet:
                            serial_number =form.cleaned_data.get('serial_number')                            
                            LineItemIndi(invoice_id=invoice,serial_number=serial_number).save()
                        
                    print('the quantity of the product is: ',quantity)
                    amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(invoice_id=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        "GeeksFormSet":GeeksFormSet,
    }
    return render(request, 'invoice/invoice_create_new.html', context)


def formset_view(request):
    context ={}
    GeeksFormSet = formset_factory(LineItemFormIndi, extra = 5)
    formset = GeeksFormSet()

    context['formset']= formset
    return render(request, "invoice/serial3.html", context)


# Total Amount for Invoice = Sum of amount of all the lineitems 
# Total Amount for Customer = Sum of all total_amounts for Invoices 
def total_amount_aggregator(request,customer_id):
    obj2 = Invoice.objects.filter(customer_id=customer_id)
    if(Ledger.objects.filter(customer_id=customer_id).exists()== False):
        sum1=0
        for i in obj2:
            sum1 = sum1+(i.total_amount)
            print(sum1)
                   
        x=Ledger.objects.create(customer_id_id=customer_id,total_amount=sum1)
        x.save()
    
    else :
        print('inside else')
        sum2 =0
        for i in obj2:
            sum2 = sum2+(i.total_amount)
            print(sum2)
        
        x=Ledger.objects.get(customer_id_id=customer_id)
        x.total_amount = sum2
        x.save()
        
                  
    context={}
    return render(request, "invoice/home.html", context)

# 45666

def ledger_view(request):
    ledger = Ledger.objects.all()
    for i in ledger:
        print(i.customer_id)
    
    context ={
        'ledger':ledger,
    }
    return render(request, "invoice/ledger.html", context)
    
# A ledger refresh function where all the ledgers will be refreshed 

def test_pge(request):   
    return render(request, "invoice/web1_s.html")


def test_pge3(request):
    posts =Invoice.objects.all()    
    print(posts)
    return render(request, "invoice/web_s.html",{'posts':posts})
    
def ledger_item(request,customer_id):
    items = Invoice.objects.filter(customer_id=customer_id)
    
    return render(request, "invoice/ledger_detail.html",{'items':items})

def customer_list(request):
    items = Customer.objects.all()
    
    return render(request, "invoice/customer_list.html",{'items':items})
    
    
