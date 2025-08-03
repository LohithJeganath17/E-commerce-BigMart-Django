from django.db import models
from category.models import CategoryModel
from accounts.models import Account
from django.urls import reverse
from django.db.models import Avg,Count

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
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(avge=Avg('rating'))
        avg = 0
        if reviews['avge'] is not None:
            avg = float(reviews['avge'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
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
    

class ReviewRating(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
     product = models.ForeignKey(ProductModel,default=None,on_delete=models.CASCADE)
     image = models.ImageField(max_length=255,upload_to='store/products')

     def __str__(self):
          return self.product.product_name

     class Meta:
          verbose_name = 'productgallery'
          verbose_name_plural = 'Product Gallery'