from django.shortcuts import render
from db.models import Item, Order, Item_Asoc_Order, Users
from db.models import Item, Order, Item_Asoc_Order, Delivery, Order_Asoc_Delivery, StoredValues
from django.views.generic import View
from braces import views
from django.http import FileResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from django.shortcuts import redirect
from .forms import NameForm
from django.http import HttpResponse
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
import json
from django.contrib import auth, messages
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36
from heapq import heappush, heappop


# Create your views here.

def item_view(request):
    context_object_name = 'Items'
    objects = Item.objects.all()

    context = {
        'Items': objects,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'db/order.html', context)

def new_WP(request):
    context_object_name = 'Order'
    objects = Order.objects.all()

    context = {
        'Order': objects,
    }
    return render(request, 'db/newWP.html', context)

def dispatcher(request):
    context_object_name = 'Delivery'
    objects = Delivery.objects.all()

    context = {
        'Delivery': objects,
    }
    return render(request, 'db/dispatcher.html', context)


def dequeue_WP(request):
    context_object_name = 'Order'
    objects = Order.objects.all()

    context = {
        'Order': objects,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'db/dequeuedWP.html', context)

def travellingSalesmanAlgorithm(clinicLocations):
    clinicAsoc = dict()
    clinics = ClinicLocation.objects.all();

    for clinic in clinics:
        obj1 = clinicAsocclinic.objects.filter(clinicID1 = clinic.clinicID)
        obj2 = clinicAsocclinic.objects.filter(clinicID2 = clinic.clinicID)
        for obj in obj1:
            clinicAsoc[(clinic.clinicID,obj.clinicID2)] = obj.distance

        for obj in obj2: 
            clinicAsoc[(clinic.clinicID,obj.clinicID1)] = obj.distance

    frontier = []
    hospitalID = 8 
    for clinicLocation in clinicLocations:
        frontier.append((clinicAsoc[(8, clinicLocation)] , clinicLocation))
    n = 0
    checker = set()
    length = len(clinicLocations)
    while n<length:
        node = frontier.remove(min(frontier))
        ##goalstate?
        checker.add(node[1])
        frontier = []
        for clinicLocation in clinicLocations:
            if clinicLocation not in checker:
                frontier.append(( clinicAsoc[(node[1], clinicLocation)] , clinicLocation)) 
        n+=1

def new_D(request):
    context_object_name = 'Delivery'
    objects = Delivery.objects.all()

    orders = Order.objects.all()
    
    


    #create delivery and assign stuff
    deliveryNo = 0

    storedValueobj = StoredValues.create(0,0)
    for value in StoredValues.objects.all():
        deliveryNo = value.latestDeliveryNo
        storedValueobj = value


    weight = 1.2 #Shipping cotainer weighs 1.2kgs
    noOfOrders = 0
    delivery = Delivery.create(-1, 0, None, 0)
    i = 0
    while i < len(orders):

        if orders[i].assigned == False:
            if  weight + orders[i].weight < 25.0:

                weight += orders[i].weight
                noOfOrders+=1
                orders[i].assigned = True
                orderAsocdelivery = Order_Asoc_Delivery.create(orderNo = orders[i].orderNo, deliveryNo = deliveryNo)
                orderAsocdelivery.save()
            else:

                now = datetime.datetime.now()
                delivery = Delivery.create(deliveryNo, weight, now, noOfOrders)
                delivery.save()

                delivery = Delivery.create(-1, 0, None, 0)
                deliveryNo+=1
                weight = 1.2
                noOfOrders = 0
                i-=1
            orders[i].save()
        i+=1
        #change this to make it work

    if(noOfOrders != 0):
        now = datetime.datetime.now()
        delivery = Delivery.create(deliveryNo, weight, now, noOfOrders)
        delivery.save()
        deliveryNo+=1

    storedValueobj.latestDeliveryNo = deliveryNo
    storedValueobj.save()
    



    context = {
        'Delivery': objects,
    }
    # Render the HTML template index.html with the data in the context variable
    hi = [1,4,5,6,7]
    travellingSalesmanAlgorithm(hi)
    return render(request, 'db/dispatcher.html', context)


def pdf_generation(request):
    #buffer = io.BytesIO()
    p = canvas.Canvas('db/shipping_label.pdf')
    
    # json =
    
    p.drawString(245, 750, 'SHIPPING LABEL')
    p.drawString(100, 650, 'Order Number:')
    p.drawString(100, 600, 'List of Items:')
    p.drawString(100, 550, 'Final Destination:')
    
    p.showPage()
    p.save()
    
    response = redirect('/dispatcher/')
    return response

class Submit(views.CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        
        form = NameForm(request.POST)
        # Send an email for token value
        
        if form.is_valid():
            print(form.cleaned_data)
            # Verifying the token value with the one sent in HA email
            
            # Verifying that the username is unique
            if Users.objects.filter(username = form.cleaned_data['username']).count() == 0:
                user = Users.create(firstname = form.cleaned_data['firstname'], lastname = form.cleaned_data['lastname'], username = form.cleaned_data['username'], password = form.cleaned_data['password'], role = form.cleaned_data['role'], emailID = 'vanshajchadha05@gmail.com')
                user.save()
                print("New Username")
                    
            else:
                print("Old Username")
                
            # Setting the default email to the HA email
            
        return HttpResponseRedirect('/register/')

class PDF(views.CsrfExemptMixin, View):
    def get(self, request, *args, **kwargs):
        
        p = canvas.Canvas('db/shipping_label.pdf')
        
        order_num = request.META['QUERY_STRING']
        obj = Order.objects.filter(orderNo = int(order_num))

        for i in obj:
            print(i.clinicManager_location.all())
        
        p.drawString(245, 750, 'SHIPPING LABEL')
        p.drawString(100, 650, 'Order Number: ' + order_num)
        p.drawString(100, 600, 'List of Items: ')
        #p.drawString(100, 550, 'Final Destination: ' + obj[0].ClinicLocation.clinicLocation)
        p.showPage()
        p.save()

        context = {
            'Delivery': objects,
        }

        response = FileResponse(open('db/shipping_label.pdf', 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'inline'
        print(response)
                
        return response
    # Render the HTML template index.html with the data in the context variable
    #return render(request, 'db/dequeuedWP.html', context)
    
        
            

        orderNo = 0
        for value in StoredValues.objects.all():
            orderNo = value.latestOrderNo
            value.latestOrderNo +=1
            value.save()

        quantity = 0
        weight = 0
        objects = json.loads(request.body)
        print(objects)
        items = Item.objects.all();
        
        i = 0
        priority = ''
        for obj in objects:
            if i == 0:
                priority = obj['priority']
                i+=1
            else:
                item_asoc_order = Item_Asoc_Order.create(itemNo= int(obj['itemNo']), orderNo = orderNo, qty = obj['quantity'])
                item_asoc_order.save();
                quantity += int(obj['quantity'])
                weight += int(obj['quantity']) * obj['weight']


        now = datetime.datetime.now()
        order = Order.create(orderNo = orderNo, noOfItems = quantity, weight = weight, priority = priority, datetime = now)
        order.save();

class OrderView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
    require_json = True
    def post(self, request, *args, **kwargs):
        
        orderNo = 0
        for value in StoredValues.objects.all():
            orderNo = value.latestOrderNo
            value.latestOrderNo +=1
            value.save()

        quantity = 0
        weight = 0
        objects = json.loads(request.body)
        print(objects)
        items = Item.objects.all();
        
        i = 0
        priority = ''
        for obj in objects:
            if i == 0:
                priority = obj['priority']
                i+=1
            else:
                item_asoc_order = Item_Asoc_Order.create(itemNo= int(obj['itemNo']), orderNo = orderNo, qty = obj['quantity'])
                item_asoc_order.save();
                quantity += int(obj['quantity'])
                weight += int(obj['quantity']) * obj['weight']


        now = datetime.datetime.now()
        order = Order.create(orderNo = orderNo, noOfItems = quantity, weight = weight, priority = priority, datetime = now)
        order.save();

        return self.render_json_response(
            {"message": "Your contact has been sent!"})

class DequeueOrder(views.CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        orderNo = request.body
        print(orderNo)
        
        orders = Order.objects.filter(orderNo=int(orderNo))
        for order in orders:
            print(order.orderStatus)
            order.orderStatus = 'PBW'
            order.save()
            print(order.orderStatus)

        return HttpResponse('')

class CompleteOrder(views.CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        
        orderNo = request.body
        print(orderNo)
        orders = Order.objects.filter(orderNo=int(orderNo))
        for order in orders:
            print(order.orderStatus)
            order.orderStatus = 'QFD'
            order.save()
            print(order.orderStatus)
        return HttpResponse('')
        
def reg(request):
    return render(request, 'db/signup.html')



class Submit(views.CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        
        form = NameForm(request.POST)
        # Send an email for token value
        print("fkw")
        if form.is_valid():
            print(form.cleaned_data)
            # Verifying the token value with the one sent in HA email
            print("fk")
            # Verifying that the username is unique
            if Users.objects.filter(username = form.cleaned_data['username']).count() == 0:
                user = Users.create(firstname = form.cleaned_data['firstname'], lastname = form.cleaned_data['lastname'], username = form.cleaned_data['username'], password = form.cleaned_data['password'])
                user.save()
                print("New Username")
                    
            else:
                print("Old Username")
                
            # Setting the default email to the HA email
            
        return HttpResponseRedirect('/login/')


def login(request):
 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            """correct username and password login the user
            if Users.objects.filter(username=username).role.filter(name='CM').exists():
                return HttpResponseRedirect('/order/')
            elif Users.objects.filter(username=username).role.filter(name='WP').exists():
                return HttpResponseRedirect('/newWP/')
            else: """
            return HttpResponseRedirect('/order/')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'db/login.html')

def register(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'db/forms.html')

def cmorders(request):
    context_object_name = 'Items'
    objects = Item.objects.all()

    context = {
        'Items': objects,
    }

    return render(request, 'db/cmorders.html', context)
class Register(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
    require_json = True
    def post(self, request, *args, **kwargs):

        quantity = 0
        weight = 0
        objects = json.loads(request.body)
        print(objects)

        return self.render_json_response(
            {"message": "Your contact has been sent!"})

