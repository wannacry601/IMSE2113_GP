from django.db import models

class Pellet(models.Model):
    is_inbound = models.BooleanField(default = True)
    column = models.CharField(max_length=8)
    row = models.CharField(max_length=8)
    pellet_name = models.CharField(max_length=32)
    pellet_desc = models.CharField(max_length=200, null=True)
    inbound_shipment = models.DateField()
    outbound_shipment = models.DateField(null = True)
    source = models.CharField(max_length = 50, null = True)
    destination = models.CharField(max_length = 50, null = True)
    class Meta:
       unique_together = ('column', 'row')

class Cargo(models.Model):
    is_in_warehouse = models.BooleanField(default=True)
    on_pellet = models.ForeignKey('Pellet', on_delete = models.SET_NULL,  null=True)
    destination = models.CharField(max_length = 50, null = True)
    arrival_date = models.DateField()
    origin = models.CharField(max_length = 50, null = True)
    due_outbound_date = models.DateField(null = True)
    name = models.CharField(max_length = 32)
    desc = models.CharField(max_length = 200, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.ForeignKey('Products', on_delete = models.SET_NULL, null=True)
   
class Order(models.Model):
    due_date = models.DateField()
    order_type = models.ForeignKey('Products', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    destination = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null = True)
   
class Products(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

# Products(name='table', description='company')

# Create your models here.

