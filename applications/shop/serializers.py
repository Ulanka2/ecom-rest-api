from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category
from .models import Product
from applications.carts.models import Cart, CartProduct
from applications.orders.models import Order

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = User
        fields = ['id', 'username']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id',  'category', 'name', 'description', 'rating', 'quantity', 'price', 
        'image', 'available', 'created_at', 'updated']


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['amount']


# class ProductInCartSerializer(serializers.Serializer):

#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     amount = serializers.IntegerField()

class ProductInCart(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = CartProduct
        fields = ['id', 'name', 'amount']

class CartsSerializer(serializers.ModelSerializer):

    # products = serializers.SerializerMethodField()
    products = ProductInCart(source='cart_products', many=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'owner', 'products',]
    
    # def get_products(self, instance):
    #     cartproducts = instance.cart_products.all()
    #     products = []
    #     for cartproduct in cartproducts:
    #         product = {}
    #         product['name'] = cartproduct.product.name
    #         product['id'] = cartproduct.product_id
    #         product['amount'] = cartproduct.amount
    #         products.append(product)
    #     serializer = ProductInCartSerializer(products, many=True)
    #     return serializer.data





class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class AmountSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
