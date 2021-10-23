from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics

from applications.shop.models import Category, Product
from applications.shop.serializers import  CartSerializer, ProductSerializer, CategorySerializer
from applications.carts.models import CartProduct
from applications.shop.serializers import OrderSerializer, AmountSerializer
from applications.orders.models import Order
from drf_yasg.utils import swagger_auto_schema


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser, ]


class ProductViewSet(ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(operations_description='Upload thumbnail',
    request_body=AmountSerializer, methods=['post', 'delete',])
    @action(permission_classes=[IsAuthenticated, ],
            methods=['post', 'delete' ], detail=True,
            serializer_class=AmountSerializer)
    
    def cart(self, request, *args, **kwargs):
        cart = request.user.cart
        product = self.get_object()

        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        requested_amount = serializer.validated_data.get('amount')

        if request.method == 'POST':

            if requested_amount > product.quantity:
                return Response({'error': 'Requested amount is larger than product amount'},
                                 status=status.HTTP_400_BAD_REQUEST)
            
            product.quantity -= requested_amount
            product.save()

            cart_product, created = CartProduct.objects.get_or_create(
                cart=cart,
                product=product,
            )
            if created:
                cart_product.amount = requested_amount
            else:
                cart_product.amount += requested_amount
            cart_product.save()

            serializer = CartSerializer(instance=cart)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if CartProduct.objects.filter(cart=cart, product=product).exists():
                cart_product = CartProduct.objects.get(product=product, cart=cart,)

                if requested_amount > cart_product.amount:
                    return Response({'error': 'Requested amount is larger than product amount'},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif requested_amount == cart_product.amount:
                    cart_product.delete()

                    serializer = CartSerializer(instance=cart)
                    return Response(serializer.data)

                cart_product.amount -= requested_amount
                cart_product.save()

                serializer = CartSerializer(instance=cart)
                return Response(serializer.data)

            return Response({'error': 'Current cart does not contain this product'},
                            status=status.HTTP_400_BAD_REQUEST)
    

    
    @action(permission_classes=[IsAuthenticated, ],
            methods=['post'], detail=False)
    def cart_clear(self, request, *args, **kwargs):
        cart = request.user.cart
        cart.products.clear()
        serializer = CartSerializer(instance=cart)
        return Response(serializer.data)
    
    
    # 2вариант
    # @action(methods=['post', 'delete'], permission_classes = [IsAuthenticated, ], detail=True)
    # def cart(self, request, *args, **kwargs):
    #     product = self.get_object()
    #     cart = request.user.cart
        
    #     if request.method == 'POST':
    #         cart.products.add(product)
        
    #     elif request.method == 'DELETE':
    #         cart.products.remove(product)
        
    #     serializer = CartsSerializer(instance=cart)
    #     return Response(serializer.data)

    
    @action(permission_classes=[IsAuthenticated, ],
            methods=['post'], detail=False)
    def add_order(self, request, *args, **kwargs):
        cart = request.user.cart
        cartproducts = cart.cart_products.all()
        product_list = []
        total_quantity = 0
        total_price = 0
        for cartproduct in cartproducts:
            product_list += f'{cartproduct.product.name[:100]}'
            total_price += cartproduct.product.price * cartproduct.amount
            total_quantity += cartproduct.amount
            # cartproduct.product += cartproduct.amount
        
        order = Order.objects.create(cart=cart, total_quantity=total_quantity, 
                         total_price=total_price, product_list=product_list)
        cart.products.clear()
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data)
