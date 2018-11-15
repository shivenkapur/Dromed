from django.shortcuts import render
from db.models import Item, Order, Item_Asoc_Order
from django.views.generic import View
from braces import views
from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.shortcuts import redirect

import io
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

def pdf_generation(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    

    p.showPage()
    p.save()
    
    return FileResponse(buffer, as_attachment = True, filename = 'shipping_label.pdf')

class ContactSendView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
	require_json = True
	def post(self, request, *args, **kwargs):
		global orderNo
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
		order.save();

		return self.render_json_response(
            {"message": "Your contact has been sent!"})
