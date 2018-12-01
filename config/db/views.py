
from django.core.mail import send_mail
import datetime
from django.shortcuts import render
from db.models import Item, Order, Item_Asoc_Order, Users, Delivery, Order_Asoc_Delivery, StoredValues, Clinic_Asoc_Clinic
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
from django.contrib.auth.models import User
# Create your views here.
from django.core.mail import send_mail
from random import randint
import csv


def check(role):
    username = ""
    for value in StoredValues.objects.all():
        username = value.username
    users = Users.objects.filter(username = username)

    flag = False
    for user in users:
        if(user.role == role):
            flag = True
    return flag

def item_view(request):
    if(check('CM')):
        context_object_name = 'Items'
        objects = Item.objects.all()

        context = {
            'Items': objects,
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'db/order.html', context)
    else:
        return HttpResponseRedirect('/login/')

def new_WP(request):

    if(check('WP')):
        context_object_name = 'Items'
        objects = Item.objects.all()

        context = {
            'Items': objects,
        }

        order = Order.objects.filter().order_by('priority')
        print(order)
        context = {
            'Order': order,
        }
        return render(request, 'db/newWP.html', context)
    else:
        return HttpResponseRedirect('/login/')

def dequeue_WP(request):
    if(check('WP')):
        context_object_name = 'Items'
        objects = Item.objects.all()

        context = {
            'Items': objects,
        }
        context_object_name = 'Order'
        objects = Order.objects.all()

        context = {
            'Order': objects,
        }
        # Render the HTML template index.html with the data in the context variable
        return render(request, 'db/dequeuedWP.html', context)
    else:
        return HttpResponseRedirect('/login/');


def new_D(request):
    if(check('DP')):
        context_object_name = 'Items'
        objects = Item.objects.all()

        context = {
            'Items': objects,
        }
        context_object_name = 'Delivery'
        objects = Order.objects.all()

        objects = Order.objects.filter(orderStatus = 'QFD')

        #travellingSalesmanAlgorithm([1,4,6,7])
        context = {
            'Order': objects,
        }
        # Render the HTML template index.html with the data in the context variable
        return render(request, 'db/dispatcher.html', context)
    else:
        return HttpResponseRedirect('/login/');

def travellingSalesmanAlgorithm(clinicLocations):
    clinicAsoc = dict()
    clinics = ClinicLocation.objects.all();

    for clinic in clinics:
        objects = Clinic_Asoc_Clinic.objects.filter(clinicID1 = clinic.clinicID)
        

        for obj in objects:
            clinicAsoc[(clinic.clinicID,obj.clinicID2)] = obj.distance
            clinicAsoc[(obj.clinicID2,clinic.clinicID)] = obj.distance


    frontier = []
    hospitalID = 8 
    checker = set()
    length = 0
    for clinicLocation in clinicLocations:
        if clinicLocation not in checker:
            length+=1
            checker.add(clinicLocation)
            frontier.append((clinicAsoc[(8, clinicLocation)] , clinicLocation))
    print("hiii")
    print(frontier)

    n = 0

    answer = []
    done = set()
    while n<length:
        node = remove(min(frontier, key = lambda x: x[0]), frontier)
        answer.append(node[1])
        frontier = []
        checker = set()
        done.add(node[1])
        for clinicLocation in clinicLocations:
            if clinicLocation not in checker and clinicLocation not in done:
                checker.add(clinicLocation)
                frontier.append((clinicAsoc[(node[1], clinicLocation)] , clinicLocation))
        n+=1
    

    answer.append(8)
    return answer


def remove(n, frontier):
    element = 0
    for i in range(0,len(frontier)):
        if frontier[i][0] == n[0] :
            element = frontier[i]
            for j in range(i,len(frontier)-1):
                frontier[j]=frontier[j+1]
            del frontier[len(frontier)-1]
            return element


#PDF
class PDF(views.CsrfExemptMixin, View):
    def get(self, request, *args, **kwargs):

        p = canvas.Canvas('db/shipping_label.pdf')

        order_num = request.META['QUERY_STRING']
        orders = Order.objects.filter(orderNo = int(order_num))
        #print(obj)

        for i in orders:
            print(i)
            print(i.clinicManager_location)

        p.drawString(245, 750, 'SHIPPING LABEL')
        p.drawString(100, 650, 'Order Number: ' + order_num)

        y = 600
        p.drawString(100, y, 'List of Items: ')
        y-=50

        i = 0
        itemNos = Item_Asoc_Order.objects.filter(orderNo = int(order_num))
        for itemNo in itemNos:
            item = Item.objects.filter(itemNo = itemNo.itemNo)
            i+=1
            p.drawString(100, y, 'Item '+str(i) + " " + item[0].description + " Quantity: " + str(itemNo.qty))
            y-=50
        
        p.drawString(100, y, 'Final Destination: ' + orders[0].clinicManager_location.clinicLocation)
        p.showPage()
        p.save()

        #context = {
        #   'Delivery': objects,
        #}

        response = FileResponse(open('db/shipping_label.pdf', 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment'
        print(response)
        return response


#Orders and WP


class ContactSendView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
    require_json = True
    def post(self, request, *args, **kwargs):
        orderNo = 0
        username = ""
        for value in StoredValues.objects.all():
            orderNo = value.latestOrderNo
            username = value.username
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


        user = Users.objects.filter(username = username)
        now = datetime.datetime.now()
        print(user[0].clinic)
        order = Order.create(orderNo = orderNo, noOfItems = quantity, weight = weight,clinicManager_location =  user[0].clinic, priority = priority, datetime = now, username = username)
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

#Login
def reg(request):
    context_object_name = 'Users'
    objects = Item.objects.all()

    context = {
        'Items': objects,
    }
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
                user = Users.objects.filter(token = form.cleaned_data['token'])
                if user:
                    user[0].firstname = form.cleaned_data['firstname']
                    user[0].lastname = form.cleaned_data['lastname']
                    user[0].username = form.cleaned_data['username']
                    user[0].password = form.cleaned_data['password']
                    clinicLocation = form.cleaned_data['clinicLocation']
                    if clinicLocation and user[0].role == 'CM':
                        print("hiiiiii" + clinicLocation)
                        clinic = ClinicLocation.objects.filter(clinicLocation = clinicLocation)
                        user[0].clinic = clinic[0]
                    user[0].save()
                    print("New Username")
                    return HttpResponseRedirect('/login/')
            else:
                print("Old Username")
        return render(request, 'db/signup.html')
# Setting the default email to the HA email


def authenticate(username, password):
    users = Users.objects.all()
    for user in users:
        if(username == user.username and password == user.password):
            return user

    return False

def check_user(username):
    users = Users.objects.all()
    for user in users:
        if username == user.username:
            return user

    return False

def get_random(x):
    startRandom = 10**(x-1)
    endRandom = (10**x)-1
    return randint(startRandom, endRandom)

def login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if password == '':
            ans = check_user(username)
            if ans:
                token = hex(get_random(32)).split('x')[-1]
                ans.token = token
                ans.save()
                send_mail('Forgot Password', 'http://127.0.0.1:8000/forgot/?'+str(token), '', [ans.emailID], fail_silently=False)
            else:
                messages.error(request, 'Error wrong username/password')
        else:
            user = authenticate(username,password)
            if user:
                objects = StoredValues.objects.all()
                for obj in objects:
                    obj.username = str(username)
                    obj.save()
                if user.role=='CM':
                    return HttpResponseRedirect('/order/')
                elif user.role=='WP':
                    return HttpResponseRedirect('/newWP/')
                else:
                    return HttpResponseRedirect('/dispatcher/')
            else:
                messages.error(request, 'Error wrong username/password')

    return render(request, 'db/login.html')

def forgot(request):
    
    context = {
       'Token': request.META['QUERY_STRING'],
    }
    return render(request, 'db/forgot_password.html', context)

def new_password(request):
    
    if request.method == 'POST':
        NewPassword = request.POST.get('new_password')
        users = Users.objects.filter(token = request.META['QUERY_STRING'])
        for user in users:
            print(user.firstname)
            user.password = NewPassword
            user.save()
        
    return HttpResponse('<h3>Successfully Updated Password! Close this window please</h3>')

def change_details(request):
    context = {
        'User': Users.objects.filter(username = StoredValues.objects.all()[0].username)
    }

    return render(request, 'db/change_details.html', context)

def changed(request):
    user_query = request.META['QUERY_STRING']
    user = Users.objects.filter(username = user_query)
    if request.method == 'POST':
        for u in user:
            u.firstname = request.POST.get('first_name')
            u.lastname = request.POST.get('last_name')
            u.emailID = request.POST.get('emailID')
            u.password = request.POST.get('password')
            u.save()
    return HttpResponseRedirect('/order/')


def cmorders(request):
    if(check('CM')):
        context_object_name = 'Orders'

        objects = StoredValues.objects.all()
            
        clinic = ""
        orders = Order.create(0, None, None)
        for obj in objects:
            user = Users.objects.filter(username = obj.username)
            orders = Order.objects.filter(username = obj.username).exclude(orderStatus = 'CAN').exclude(orderStatus = 'DEL')

        context = {
            'Orders': orders,
        }
        print(orders)
        return render(request, 'db/cmorders.html', context)
    else:
        return HttpResponseRedirect('/login/')

class DeliveredOrder(views.CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        orderNo = request.body
        print(orderNo)
        
        orders = Order.objects.filter(orderNo=int(orderNo))
        for order in orders:
            if(order.orderStatus == 'DIS'):
                print(order.orderStatus)
                order.orderStatus = 'DEL'
                order.save()
        

        return HttpResponse('')
class CancelOrder(views.CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        orderNo = request.body
        print(orderNo)
        
        orders = Order.objects.filter(orderNo=int(orderNo))
        for order in orders:
            if(order.orderStatus == 'QFP'):
                order.orderStatus = 'CAN'
                order.save()
        

        return HttpResponse('')

class Dispatch(views.CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        deliveryNo = request.body
        delivery = Delivery.objects.filter(deliveryNo=int(deliveryNo))
        orderAsocdelivery = Order_Asoc_Delivery.objects.filter(deliveryNo=int(deliveryNo))
        for order in orderAsocdelivery:
            selectedorders = Order.objects.filter(orderNo=int(order.orderNo))
            for selectedorder in selectedorders:
                selectedorder.orderStatus = 'DIS'
                selectedorder.save()
                print(selectedorder.orderStatus)
        delivery.delete()

        return HttpResponse('')

class CSV(views.CsrfExemptMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="db/itinerary.csv"'
        writer = csv.writer(response)

        delivery_num = request.META['QUERY_STRING']

        obj = Order_Asoc_Delivery.objects.filter(deliveryNo = int(delivery_num))

        location = []


        for i in obj:
            if Order.objects.filter(orderNo=i.orderNo)[0].clinicManager_location.clinicID not in location:
                location.append(Order.objects.filter(orderNo=i.orderNo)[0].clinicManager_location.clinicID)

        answer = travellingSalesmanAlgorithm(location)
        

        for i in answer:
            temp = ClinicLocation.objects.filter(clinicID = i)[0]
            clinic_loc = temp.clinicLocation
            lat = temp.latitude
            lon = temp.longitude
            alt = temp.altitude
            writer.writerow([clinic_loc, lat, lon, alt])

        return response
 
class Makeorder(views.CsrfExemptMixin, View):
    
    def post(self, request, *args, **kwargs):
        orderNos = request.body

        orders = json.loads(request.body)
        print(orders)
        

        #create delivery and assign stuff
        deliveryNo = 0

        storedValueobj = None
        for value in StoredValues.objects.all():
            deliveryNo = value.latestDeliveryNo
            storedValueobj = value
            value.latestDeliveryNo+=1
            value.save()


        weight = 1.2 #Shipping cotainer weighs 1.2kgs
        noOfOrders = 0
        delivery = Delivery.create(deliveryNo, 0, None, 0)
        
        n = 0
        for order in orders:
            orderobj = Order.objects.filter(orderNo = int(order['orderNo']))
            for o in orderobj:
                n+=1
                o.orderStatus = 'QFD2'
                weight += o.weight
                o.save()
                orderasocdelivery = Order_Asoc_Delivery.create(o.orderNo, deliveryNo)
                orderasocdelivery.save()
        delivery.weight = weight
        delivery.noOfOrders = n
        delivery.save()
        return HttpResponse('')

def dispatcher_deliveries(request):

    if(check('DP')):
        context_object_name = 'Delivery'
        objects = Delivery.objects.all()

        context = {
            'Delivery': objects,
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'db/dispatcherdelivery.html', context)
    else:
        return HttpResponseRedirect('/login/')

