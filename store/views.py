from django.shortcuts import render , get_object_or_404
from .models import ProductModel
from category.models import CategoryModel
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

def storepage(request,category_slug = None):

    categories= None
    products = None

    if category_slug != None:
        categories = get_object_or_404(CategoryModel , slug = category_slug)
        products = ProductModel.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products,1)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
        products_count = products.count()
    else:
        products = ProductModel.objects.all().filter(is_available = True)
        paginator = Paginator(products,3)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
        products_count = products.count() 

    context = {
      'products': paged_products,
      'products_count' : products_count ,
    }
    return render(request ,'store/store.html',context)


def product_detail(request,category_slug,product_slug):

    try:
        single_product = ProductModel.objects.get(category__slug = category_slug,slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart' : in_cart ,
    }
    return render(request ,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = ProductModel.objects.order_by('-created_date').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword))
            products_count = products.count() 

    context = {
        'products' : products ,
        'products_count' : products_count,
    }
    return render(request,'store/store.html',context)
