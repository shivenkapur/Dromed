from django.contrib import admin

# Register your models here.


from .models import Delivery,Users,Item,Order, ClinicLocation, Item_Asoc_Order, Order_Asoc_Delivery, StoredValues, clinicAsocclinic

admin.site.register(Delivery)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Users)
admin.site.register(ClinicLocation)
admin.site.register(Item_Asoc_Order)
admin.site.register(Order_Asoc_Delivery)
admin.site.register(StoredValues)
admin.site.register(clinicAsocclinic)
