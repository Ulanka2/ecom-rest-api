from django.db import models
from applications.carts.models import Cart
from applications.shop.models import Product


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True,
                             related_name='orders')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Обшая цена')
    total_quantity = models.PositiveIntegerField(default=1, verbose_name='Обшая колличество')
    product_list = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'Номер заказа - {self.id}'

