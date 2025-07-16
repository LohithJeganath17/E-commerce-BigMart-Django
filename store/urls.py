
from django.contrib import admin
from django.urls import path
from store.views import storepage,product_detail,search

urlpatterns = [
    path('',storepage,name = 'our_store'),
    path('category<slug:category_slug>/',storepage,name = 'product_by_category'),
    path('category<slug:category_slug>/<slug:product_slug>/',product_detail,name = 'product_detail'),
    path('search/',search,name = 'search'),
] 
