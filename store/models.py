from django.db import models
from category.models import CategoryModel
from django.urls import reverse

# Create your models here.

class ProductModel(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    slug        = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    stock = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.product_name

