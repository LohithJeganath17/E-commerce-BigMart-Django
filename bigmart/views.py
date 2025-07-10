
from django.shortcuts import render
from store.models import ProductModel

def greet(request):
   products = ProductModel.objects.all().filter(is_available = True)

   context = {
      'products': products,
   }
   return render(request,'home.html',context)

