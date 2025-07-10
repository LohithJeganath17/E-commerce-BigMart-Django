from django.contrib import admin
from .models import ProductModel

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','price','stock','category','last_modified','is_available')

admin.site.register(ProductModel,ProductAdmin)
