from django.shortcuts import render
from db.models import Item, Order, Item_Asoc_Order, Users
from django.views.generic import View
from braces import views
from django.http import FileResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from django.shortcuts import redirect
from .forms import NameForm

import json
# Create your views here.

orderNo = 0

def item_view(request):
	context_object_name = 'Items'
	objects = Item.objects.all()

	context = {
		'Items': objects,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'db/order.html', context)

def order_view(request):
	context_object_name = 'Order'
	objects = Order.objects.all()

	context = {
		'Order': objects,
	}
	return render(request, 'db/dispatcher.html', context)

def reg(request):
    return render(request, 'db/login.html')

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
    
        response = FileResponse(open('db/shipping_label.pdf', 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'inline'
        print(response)
        
        return response

class ContactSendView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
	require_json = True
	def post(self, request, *args, **kwargs):
		global orderNo

		orderNo = Order.lastorder + 1
		Order.lastorder += 1
		orderNo = Order.lastorder +1
		Order.lastorder+=1

		quantity = 0
		weight = 0
		print(orderNo)
		objects = json.loads(request.body)
		print(objects)
		items = Item.objects.all();
		
		for obj in objects:
			item_asoc_order = Item_Asoc_Order.create(itemNo= int(obj['itemNo']), orderNo = orderNo, qty = obj['quantity'])
			item_asoc_order.save();
			quantity += obj['quantity']
			weight += obj['quantity'] * obj['weight']


		order = Order.create(orderNo = orderNo, noOfItems = quantity, weight = weight)
		order.save()

		return self.render_json_response(
            {"message": "Your contact has been sent!"})
