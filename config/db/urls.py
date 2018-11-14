from django.urls import path
from . import views


urlpatterns = [
    path('order/', views.item_view, name = 'items-view'),
    path('order/send/', views.ContactSendView.as_view(), name = 'send'),
    path('dispatcher/', views.order_view, name = 'disptacher')
]