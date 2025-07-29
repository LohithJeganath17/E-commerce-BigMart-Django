from django.contrib import admin
from django.urls import path
from .views import placeorder,payments,order_complete


urlpatterns = [
    path('placeorder/',placeorder,name = 'placeorder'),
    path('payments/',payments,name = 'payments'),
    path('order_complete/',order_complete,name = 'order_complete'),
]