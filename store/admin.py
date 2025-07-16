from django.contrib import admin
from .models import ProductModel,VariationModel

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','price','stock','category','last_modified','is_available')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

admin.site.register(ProductModel,ProductAdmin)
admin.site.register(VariationModel,VariationAdmin)
