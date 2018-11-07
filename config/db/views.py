from django.shortcuts import render
from models import Item
# Create your views here.

class ListItems():

	model = Item

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        #used to add extra information
        #context['book_list'] = Book.objects.all()
        return context

	context_object_name = 'Items'
	objects = Item.objects.all()

	context = {
        'Items': objects,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)