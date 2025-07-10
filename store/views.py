from django.shortcuts import render , get_object_or_404
from .models import ProductModel
from category.models import CategoryModel

# Create your views here.

def storepage(request,category_slug = None):

    categories= None
    products = None

    if category_slug != None:
        categories = get_object_or_404(CategoryModel , slug = category_slug)
        products = ProductModel.objects.filter(category = categories, is_available = True)
        products_count = products.count()
    else:
        products = ProductModel.objects.all().filter(is_available = True)
        products_count = products.count() 

    context = {
      'products': products,
      'products_count' : products_count ,
    }
    return render(request ,'store/store.html',context)


def product_detail(request,category_slug,product_slug):

    try:
        single_product = ProductModel.objects.get(category__slug = category_slug,slug = product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }
    return render(request ,'store/product_detail.html',context)
