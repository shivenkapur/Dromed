from django.shortcuts import render
from db.models import Item, Order, Item_Asoc_Order
from django.views.generic import View
from braces import views

from django.shortcuts import redirect

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



class ContactSendView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
	require_json = True
	def post(self, request, *args, **kwargs):
		global orderNo
		orderNo = Order.lastorder + 1
		Order.lastorder += 1
		quantity = 0
		weight = 0
		print(orderNo)
		objects = json.loads(request.body)

		items = Item.objects.all();
		
		for obj in objects:
			item_asoc_order = Item_Asoc_Order.create(itemNo= int(obj['itemNo']), orderNo = orderNo, qty = obj['quantity'])
			item_asoc_order.save();
			quantity += obj['quantity']


		order = Order.create(orderNo = orderNo, noOfItems = quantity, weight = weight)
		order.save();

		return self.render_json_response(
            {"message": "Your contact has been sent!"})
