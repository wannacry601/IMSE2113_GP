from django.db import models

class Pellet(models.Model):
    is_inbound = models.BooleanField(default = True)

    column = models.CharField(max_length=8)
    row = models.CharField(max_length=8)
    pellet_name = models.CharField(max_length=32)
    pellet_desc = models.CharField(max_length=100, null=True)

    inbound_shipment = models.ForeignKey('Inbound', on_delete = models.CASCADE, null = True)
    source = models.CharField(max_length = 50, null = True)

    outbound_shipment = models.ForeignKey('Outbound', on_delete = models.CASCADE, null = True)
    destination = models.CharField(max_length = 50, null = True)
    class Meta:
       unique_together = ('column', 'row')
    def __str__(self):
       return (f"Inbound {self.id} ({self.pellet_name}) from {self.inbound_shipment} with source {self.source} is stored at column {self.column} row {self.row}. Its contents are", self.pellet_desc if self.pellet_desc else "not defined") if self.is_inbound else\
              (f"Outbound {self.id} ({self.pellet_name}) fulfilling {self.outbound_shipment} for destination {self.destination} is stored at column {self.column} row {self.row}. Its contents are", self.pellet_desc if self.pellet_desc else "not defined")+ "."

class Cargo(models.Model):
    on_pellet = models.ForeignKey('Pellet', on_delete = models.CASCADE)
    destination = models.CharField(max_length = 50, null = True)
    name = models.CharField(max_length = 32)
    desc = models.CharField(max_length = 100, null=True)
    weight = models.NumField()
    barcode = models.CharField(maxlength = 100)
    def __str__(self):
        return f"Box {self.id} ({self.name}) is on the pellet {self.on_pellet}. Its weight is {self.weight} and it contains", self.desc if self.desc else "an undefined thing" + "."
# Create your models here.
