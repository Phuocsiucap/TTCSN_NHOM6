
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, OrderGood, Good
from .serializers import OrderSerializer, OrderGoodSerializer
from good.serializer import GoodSerializer
import datetime
from Cart.models import CartGood
# Đặt hàng (1 hoặc nhiều sản phẩm cùng lúc)
class CreateOrderAPI(APIView):
    
    
    def post(self, request):
        user = request.user  # Lấy thông tin người dùng từ user đang đăng nhập
        print(request.data)
        shipping_address = request.data.get('shipping_address')
        goods_data = request.data.get('goods')

        if not all([user, shipping_address, goods_data]):
            return Response({"error": "Thiếu thông tin bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = 0
        # Kiểm tra số lượng sản phẩm trong kho trước khi tạo đơn hàng
        for good_data in goods_data:
            cartgood = get_object_or_404(CartGood, pk=good_data['id'])
            good = cartgood.good
            quantity = good_data.get('quantity', 1)

            # Kiểm tra số lượng sản phẩm có đủ không
            if good.amount < quantity:
                print(good.amount)
                return Response({"error": f"Sản phẩm {good.goodName} không đủ số lượng trong kho."}, status=status.HTTP_400_BAD_REQUEST)
            print(good.price)
            total_amount += float(good.price) * quantity
        print(total_amount )
        # Tạo đơn hàng
        order = Order.objects.create(
            purchase_date=datetime.date.today(),
            shipping_status='Processing',
            total_amount=total_amount,
            shipping_address=shipping_address,
            user=user
        )

        # Lưu các sản phẩm trong đơn hàng và giảm số lượng trong kho
        for good_data in goods_data:
            cartgood = get_object_or_404(CartGood, pk=good_data['id'])
            good = cartgood.good
            quantity = good_data.get('quantity', 1)

            # Tạo bản ghi trong OrderGood
            OrderGood.objects.create(order=order, good=good, quantity=quantity)

            # Cập nhật lại số lượng sản phẩm trong kho
            good.amount -= quantity
            good.save()
            cartgood.delete()
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)



# Lấy thông tin đơn hàng 
class OrderDetailAPI(APIView):
    print(3)
    
    
    def get(self, request, id):
        # Lấy thông tin đơn hàng dựa trên `pk`
        print(request.data)
        order = get_object_or_404(Order, order_id=id)
        if order.user != request.user:  # Kiểm tra xem đơn hàng có phải của người dùng hiện tại không
            return Response({"error": "Bạn không có quyền truy cập đơn hàng này."}, status=status.HTTP_403_FORBIDDEN)
            
        order_serializer = OrderSerializer(order)
            # Lấy thông tin của các sản phẩm trong đơn hàng
        order_goods = OrderGood.objects.filter(order=order)
        print(order)
        order_goods_serializer = OrderGoodSerializer(order_goods, many=True)
        # Lấy danh sách các sản phẩm (Good) liên quan đến đơn hàng từ OrderGood
        goods_in_order = Good.objects.filter(ordergood__order=order).distinct()

        # Serialize danh sách sản phẩm
        goods_serializer = GoodSerializer(goods_in_order, many=True)
        print(goods_serializer)
            # Trả về thông tin đơn hàng và các sản phẩm kèm theo
        response_data = {
            "order": order_serializer.data,
            "order_good": order_goods_serializer.data,
            "good": goods_serializer.data
        }
        print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)
class OrderListView(APIView):
    def get(self, request):
        # Lấy tất cả đơn hàng của người dùng hiện tại
        orders = Order.objects.filter(user=request.user)
        order_serializer = OrderSerializer(orders, many=True)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
class CancelOrderAPI(APIView):
    def post(self, request, id):
        # Lấy thông tin đơn hàng
        order = get_object_or_404(Order, order_id=id)

        # Kiểm tra quyền sở hữu
        if order.user != request.user:
            return Response({"error": "Bạn không có quyền hủy đơn hàng này."}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra trạng thái đơn hàng (chỉ cho phép hủy khi đang ở trạng thái 'Processing')
        if order.shipping_status != 'Processing':
            return Response({"error": "Không thể hủy đơn hàng đã xử lý."}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy các sản phẩm trong đơn hàng
        order_goods = OrderGood.objects.filter(order=order)

        for order_good in order_goods:
            good = order_good.good
            # Hoàn trả số lượng sản phẩm
            good.amount += order_good.quantity
            good.save()

        # Xóa các sản phẩm liên quan trong bảng OrderGood
        order_goods.delete()

        # Xóa đơn hàng hoặc cập nhật trạng thái đơn hàng
        order.shipping_status = "Cancelled"
        order.save()

        return Response({"success": "Đơn hàng đã được hủy thành công."}, status=status.HTTP_200_OK)
"""

TẠO ĐƠN HÀNG
Dữ liệu nhận được từ font (cần bao gồn cả token)

{
    "shipping_address": "123 Đường ABC, Quận 1, TP.HCM",
    "goods": [
        {
            "good_id": 1,
            "quantity": 2
        },
        {
            "good_id": 3,
            "quantity": 1
        }
    ]
}

BACKEND TRA VÈ THONG TIN CỦA 1 DONA HÀNG CU THE
{
    "order": {
        "order_id": 1,
        "purchase_date": "2024-11-10",
        "shipping_status": "Processing",
        "total_amount": 150.0,
        "shipping_address": "123 Main St",
        "user": 1
        "admin": 2
    }
    "goods": [
        {
            "id": 1,
            "good": {
                id": 3,
                "name": "Sản phẩm C",
                "price": 100000
                ...
                # các tong tin của good
            },
            "quantity": 2
        },
        {
            "id": 2,
            "good": {
                #các thông tin của good
            },
            "quantity": 1
        }
    ]
}



BACKEND TRẢ VỀ THÔNG TIN CỦA TẤT CẢ DƠN HÀNG CÚA USER
[
  {
    "order_id": 1,
    "purchase_date": "2024-11-10",
    "shipping_status": "Processing",
    "total_amount": 150.0,
    "shipping_address": "123 Main St",
    "user": 1
    "admin": 2
  },
  {
    "order_id": 2,
    "purchase_date": "2024-11-12",
    "shipping_status": "Shipped",
    "total_amount": 200.0,
    "shipping_address": "456 Another St",
    "user": 1
    "admin": null
  }
]
"""