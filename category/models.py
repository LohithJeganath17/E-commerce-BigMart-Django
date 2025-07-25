from django.db import models
from django.urls import reverse

# Create your models here.
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=500,blank=True)
    category_image = models.ImageField(upload_to='photos/categories',blank=True)

    #class Meta:
    #    verbose_name= category  # type: ignore
    #    verbose_name_plural = categories # type: ignore

    def get_url(self):
        return reverse('product_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name