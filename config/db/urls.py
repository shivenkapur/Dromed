from django.urls import path
from . import views


urlpatterns = [
    path('order/', views.item_view, name = 'items-view'),
    path('order/send/', views.ContactSendView.as_view(), name = 'send'),
    path('newWP/', views.new_WP, name = 'newWP'),
    path('dequeueWP/', views.dequeue_WP, name = 'dequeuedWP'),
    path('dispatcher/', views.new_D, name = 'dequeuedWP'),
    path('warehouse/pdf/', views.pdf_generation, name = 'pdf-creation'),
    path('newWP/change/', views.DequeueOrder.as_view(), name = 'dequeue'),
    path('dequeueWP/complete/', views.CompleteOrder.as_view(), name = 'dequeue'),
    path('login/', views.login, name='login')

]
