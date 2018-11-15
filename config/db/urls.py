from django.urls import path, re_path
from . import views


urlpatterns = [
    path('order/', views.item_view, name = 'items-view'),
    path('register/', views.reg, name = 'register'),
    path('register/submit/', views.Submit.as_view(), name = 'submission'),
    path('order/send/', views.ContactSendView.as_view(), name = 'send'),
    path('dispatcher/', views.order_view, name = 'disptacher'),
    re_path(r'^dispatcher/warehouse/pdf/', views.PDF.as_view(), name = 'pdf-creation')
]
