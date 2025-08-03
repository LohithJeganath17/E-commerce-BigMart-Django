
from django.shortcuts import render
from store.models import ProductModel,ReviewRating

def greet(request):
   products = ProductModel.objects.all().filter(is_available = True)

   for product in products:
      reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

   context = {
      'products': products,
   }
   return render(request,'home.html',context)

