from django.db import models
from applications.shop.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib.auth import get_user_model


User = get_user_model()

class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartProduct')
    
    


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='cart_products')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    amount = models.IntegerField(default=1)


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)
