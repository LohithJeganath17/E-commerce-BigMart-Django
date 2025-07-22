from django.db import models
from store.models import ProductModel,VariationModel
from accounts.models import Account

# Create your models here.

class CartModel(models.Model):
    cart_id = models.CharField(max_length=255,unique=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id 
    


class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null = True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    variations = models.ManyToManyField(VariationModel, blank= True)
    cart = models.ForeignKey(CartModel,on_delete=models.CASCADE,null = True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

