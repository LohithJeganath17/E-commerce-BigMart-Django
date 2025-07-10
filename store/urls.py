
from django.contrib import admin
from django.urls import path
from store.views import storepage,product_detail

urlpatterns = [
    path('',storepage,name = 'our_store'),
    path('<slug:category_slug>/',storepage,name = 'product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',product_detail,name = 'product_detail'),
] 
