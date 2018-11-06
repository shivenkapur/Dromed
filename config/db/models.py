from django.db import models

# Create your models here.

class ClinicManager(models.Model):

    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    clinicLocation = models.CharField(max_length=200)
    latitude = models.FloatField() 
    longitude = models.FloatField() 
    altitude = models.FloatField() 

    def __str__(self):
        return self.name

class Delivery(models.Model):
    
    deliveryNo = models.IntegerField()
    weight = models.FloatField() 
    datetime= models.DateField() 

   

class Item(models.Model):

    IV = 'IV'
    CATEGORY_SET = (
        (IV, 'IV Fluids'),
        (IV, 'IV Fluids')
        )
    itemNo = models.IntegerField()
    weight = models.FloatField() 
    description = models.CharField(max_length=2000)
    qty_avail = models.IntegerField()
    category = models.CharField(max_length=200, choices = CATEGORY_SET, default = IV)

  

class Order(models.Model):

    U = "U"
    I = "I"
    L = "L"

    PRIORITY_SET = (
    (U, 'Urgent'),
    (I, 'Intermediate'),
    (L, 'Low')
    )

    ORDER_STATUS = (
    ('QFP', 'Queued for Processing'),
    ('PBW', 'Processing by Warehouse'),
    ('QFD', 'Queued for Dispatch'),
    ('DIS', 'Dispatched'),
    ('DEL', 'Delivered'))

    orderNo = models.IntegerField()
    priority = models.CharField(max_length=200, choices = PRIORITY_SET, default = U)
    orderStatus = models.CharField(max_length=200, choices = ORDER_STATUS, default = 'QFP')
    weight = models.FloatField(blank = True, null = True) 
    datetime= models.DateField() 
    
    items = models.ManyToManyField(Item)
    clinicManager_username = models.ForeignKey(ClinicManager, on_delete=models.CASCADE)
    deliveryNo = models.ForeignKey(Delivery, on_delete=models.CASCADE, blank = True, null = True)

 