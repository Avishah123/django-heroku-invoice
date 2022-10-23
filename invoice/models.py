from django.db import models
import datetime

class Customer(models.Model):
    customer_id = models.CharField(max_length=100,primary_key=True)
    customer_email = models.EmailField(null=True,blank=True)
    billing_address = models.TextField(null=True,blank=True)
    customer_name =models.CharField(max_length=100)
    city = models.CharField(max_length=100,null=True,blank=True)
    country =models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
        
    def __str__(self):
        return str(self.customer_id)
    
    

class Invoice(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=100,primary_key=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default= "This is a default message.")
    
    
    
class LineItem(models.Model):
    pid = models.CharField(max_length=100,primary_key=True)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.rate
        super(LineItem,self).save(*args, **kwargs)
        
class LineItemIndi(models.Model):
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    pid = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    serial_number =models.CharField(max_length=100)
    

class Ledger(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.CharField(max_length=100)
    
   