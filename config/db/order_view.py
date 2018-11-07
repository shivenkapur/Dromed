from django.shortcuts import render
from db.models import Order

def order_view(request):
	context_object_name = 'Order'
	objects = Order.objects.all()

	context = {
		'Order': objects,
	}
	return render(request, 'db/dispatcher.html',context)