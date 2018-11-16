from django.db import models

# Create your models here.


class ClinicLocation(models.Model):
    clinicLocation = models.CharField(max_length=200)
    latitude = models.FloatField() 
    longitude = models.FloatField() 
    altitude = models.FloatField() 

    def __str__(self):
        return self.clinicLocation

"""class Distance(models.Model):
    clinicManager_location1 = models.ForeignKey(ClinicLocation, null = True, blank = True, on_delete=models.SET_NULL)
    distance = models.FloatField()
"""


class Delivery(models.Model):
    
    deliveryNo = models.IntegerField()
    weight = models.FloatField() 
    datetime= models.DateField() 
    
    def __str__(self):
        return str(self.deliveryNo)
   

class Item(models.Model):

    IV = 'IV'
    CATEGORY_SET = (
        (IV, 'IV Fluids'),
        (IV, 'IV Fluids')
        )
    itemNo = models.IntegerField()
    weight = models.FloatField() 
    description = models.CharField(max_length=2000)
    qty_avail = models.IntegerField(blank=True, null = True)
    category = models.CharField(max_length=200, choices = CATEGORY_SET, default = IV)
    profile_image = models.ImageField(upload_to="gallery", default = "gallery")
    urlroot = "Users/anujkapur/Documents/GitHub/Dromed/"

    def __str__(self):
        return self.description

class Order(models.Model):

    U = "U"
    I = "I"
    L = "L"

    PRIORITY_SET = (
    (U, 'High'),
    (I, 'Medium'),
    (L, 'Low')
    )

    ORDER_STATUS = (
    ('QFP', 'Queued for Processing'),
    ('PBW', 'Processing by Warehouse'),
    ('QFD', 'Queued for Dispatch'),
    ('DIS', 'Dispatched'),
    ('DEL', 'Delivered'))

    TYPE_SET = (
    ('N', 'New'),
    ('D', 'Dequeued'))
    lastorder = 0
    orderNo = models.IntegerField()
    priority = models.CharField(max_length=200, choices = PRIORITY_SET, default = U)
    orderStatus = models.CharField(max_length=200, choices = ORDER_STATUS, default = 'QFP')
    weight = models.FloatField(blank = True, null = True) 
    datetime= models.DateField(blank = True, null = True) 
    noOfItems = models.IntegerField(blank = True, null = True)
    orderType = models.CharField(max_length=200, choices = TYPE_SET, default = 'N')

    clinicManager_location = models.ForeignKey(ClinicLocation, null = True, blank = True, on_delete=models.SET_NULL)
    deliveryNo = models.ForeignKey(Delivery, on_delete=models.SET_NULL, blank = True, null = True)

    @classmethod
    def create(cls, orderNo, noOfItems = 0, priority = L, orderStatus = 'QFP', weight = 0):
        order = cls(orderNo = orderNo, noOfItems = noOfItems, priority = priority, orderStatus = orderStatus, weight = weight);
        return order

    def __str__(self):
        return str(self.orderNo)

class Item_Asoc_Order(models.Model):
    itemNo = models.IntegerField()
    orderNo = models.IntegerField()
    qty = models.IntegerField(default = 1)

    @classmethod
    def create(cls, itemNo, orderNo, qty):
        asoc = cls(orderNo = orderNo, itemNo = itemNo, qty = qty);
        return asoc

class Users(models.Model):
    
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    username = models.CharField(max_length=200, primary_key = True)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    emailID = models.EmailField()
    clinic = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE)

    @classmethod
    def create(cls, firstname, lastname, username, password, role, emailID):
        user = cls(firstname = firstname, lastname = lastname, username = username, password = password, role = role, emailID = emailID);
        return user

    def _str_(self):
        return str(self.firstname)
