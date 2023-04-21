from django.db import models

class Pellet(models.Model):
    is_inbound = models.BooleanField(default = True)
    column = models.CharField(max_length=8)
    row = models.CharField(max_length=8)
    pellet_name = models.CharField(max_length=32)
    pellet_desc = models.CharField(max_length=100, null=True)
    source = models.CharField(max_length = 50, null = True)
    destination = models.CharField(max_length = 50, null = True)
    class Meta:
       unique_together = ('column', 'row')
    def __str__(self):
       return (f"Inbound {self.id} ({self.pellet_name}) from {self.inbound_shipment} with source {self.source} is stored at column {self.column} row {self.row}. Its contents are", self.pellet_desc if self.pellet_desc else "not defined") if self.is_inbound else\
              (f"Outbound {self.id} ({self.pellet_name}) fulfilling {self.outbound_shipment} for destination {self.destination} is stored at column {self.column} row {self.row}. Its contents are", self.pellet_desc if self.pellet_desc else "not defined")+ "."

class Cargo(models.Model):
    on_pellet = models.ForeignKey('Pellet', on_delete = models.SET_NULL,  null=True)
    destination = models.CharField(max_length = 50, null = True)
    arrival_date = models.DateField()
    origin = models.CharField(max_length = 50, null = True)
    due_outbound_date = models.DateField(null = True)
    name = models.CharField(max_length = 32)
    desc = models.CharField(max_length = 100, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.ForeignKey('Products', on_delete = models.SET_NULL, null=True)
    def __str__(self):
        return f"Box {self.id} ({self.name}) is on the pellet {self.on_pellet}. Its weight is {self.weight} kg and it contains", self.desc if self.desc else "an undefined thing" + f"It will be shipped out on {self.due_outbound_date} to {self.destination}"if self.due_outbound_date else '' + "."
    
class Order(models.Model):
    due_date = models.DateField()
    order_type = models.ForeignKey('Products', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    destination = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null = True)
    def __str__(self) -> str:
        return f"Order {self.id} for {self.quantity} {self.order_type} to {self.destination} is due on {self.due_date}."

class Products(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    def __str__(self) -> str:
        return f"Produce {self.id} is {self.name}."
# Create your models here.

