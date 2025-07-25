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
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
variation_category_choice =(('size','size'),('color','color'))

class VariationModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    variation_category= models.CharField(max_length=100, choices = variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()


    def __str__(self):
                return self.variation_value

