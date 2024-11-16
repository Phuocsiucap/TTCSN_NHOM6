import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, OrderGood, Good
from .serializers import OrderSerializer, OrderGoodSerializer

# Đặt hàng (1 hoặc nhiều sản phẩm cùng lúc)
class CreateOrderAPI(APIView):
    def post(self, request):
        # Lấy dữ liệu từ request
        user = request.user  # Lấy thông tin người dùng từ user đang đăng nhập
        shipping_address = request.data.get('shipping_address')
        goods_data = request.data.get('goods')

        if not all([user, shipping_address, goods_data]):
            return Response({"error": "Thiếu thông tin bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = 0
        for good_data in goods_data:
            good = get_object_or_404(Good, pk=good_data['good_id'])
            total_amount += good.price * good_data.get('quantity', 1)

        # Tạo đơn hàng
        order = Order.objects.create(
            purchase_date=datetime.date.today(),
            shipping_status='Processing',
            total_amount=total_amount,
            shipping_address=shipping_address,
            user=user
        )

        # Lưu các sản phẩm trong đơn hàng
        for good_data in goods_data:
            good = get_object_or_404(Good, pk=good_data['good_id'])
            quantity = good_data.get('quantity', 1)
            OrderGood.objects.create(order=order, good=good, quantity=quantity)

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

# Lấy thông tin đơn hàng 
class OrderDetailAPI(APIView):
    def get(self, request, pk=None):
        # Lấy thông tin đơn hàng dựa trên `pk`
        if pk:
            order = get_object_or_404(Order, pk=pk)
            order_serializer = OrderSerializer(order)
            # Lấy thông tin của các sản phẩm trong đơn hàng
            order_goods = OrderGood.objects.filter(order=order)
            order_goods_serializer = OrderGoodSerializer(order_goods, many=True)
            
            # Trả về thông tin đơn hàng và các sản phẩm kèm theo
            response_data = {
                "order": order_serializer.data,
                "goods": order_goods_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Lấy tất cả đơn hàng
            orders = Order.objects.filter(user=request.user)
            order_serializer = OrderSerializer(orders, many=True)
            return Response(order_serializer.data, status=status.HTTP_200_OK)
