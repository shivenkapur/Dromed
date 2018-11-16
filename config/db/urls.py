from django.urls import path, re_path
from . import views


urlpatterns = [
    path('order/', views.item_view, name = 'items-view'),
    path('order/send/', views.ContactSendView.as_view(), name = 'send'),
    path('newWP/', views.new_WP, name = 'newWP'),
    path('dequeueWP/', views.dequeue_WP, name = 'dequeuedWP'),
    path('dispatcher/', views.new_D, name = 'dequeuedWP'),
	re_path(r'^dispatcher/warehouse/pdf/', views.PDF.as_view(), name = 'pdf-creation'),
	path('newWP/change/', views.DequeueOrder.as_view(), name = 'dequeue'),
    path('dequeueWP/complete/', views.CompleteOrder.as_view(), name = 'dequeue'),
    path('login/', views.login, name='login'),
	path('register/', views.reg, name = 'register'),
    path('register/submit/', views.Submit.as_view(), name = 'submission'),
]
