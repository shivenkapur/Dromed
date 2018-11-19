from django.contrib import admin
from db.models import *
# Register your models here.



admin.site.register(Delivery)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Users)
admin.site.register(ClinicLocation)
admin.site.register(Item_Asoc_Order)
admin.site.register(Order_Asoc_Delivery)
admin.site.register(StoredValues)
