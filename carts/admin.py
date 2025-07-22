from django.contrib import admin
from .models import CartModel,CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','user','quantity','is_active')


admin.site.register(CartModel,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
