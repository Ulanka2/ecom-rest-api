
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from applications.shop.serializers import OrderSerializer
from applications.orders.models import Order
from .permissions import IsOwner
from rest_framework import  permissions







class OrderView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,]
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly, IsOwner
    # ]
    def get_queryset(self):
        """
        Это представление должно возвращать 
        список всех покупок для текущего аутентифицированного пользователя.
        """
        cart = self.request.user.cart
        return Order.objects.filter(cart=cart)


class DetailOrderView(RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        """
        Это представление должно возвращать 
        список всех покупок для текущего аутентифицированного пользователя.
        """
        cart = self.request.user.cart
        return Order.objects.filter(cart=cart)
    


    
    
    
    # @action(permission_classes=[IsAuthenticated, ],
    #         methods=['post'], detail=False)
    # def add_order(self, request, *args, **kwargs):
    #     cart = request.user.cart
    #     cartproducts = cart.cart_products.all()
    #     product_list = ''
    #     total_quantity = 0
    #     total_price = 0
    #     for cartproduct in cartproducts:
    #         product_list += f'{cartproduct.product.name}'
    #         total_price += cartproduct.product.price * cartproduct.amount
    #         total_quantity += cartproduct.amount
    #         # cartproduct.product += cartproduct.amount
        
    #     order = Order.objects.create(cart=cart, total_quantity=total_quantity, 
    #                      total_price=total_price, product_list=product_list)
    #     cart.products.clear()
    #     serializer = OrderSerializer(instance=order)
    #     return Response(serializer.data)
