from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartGood
from .serializers import CartSerializer, CartGoodSerializer
from django.shortcuts import get_object_or_404
from good.models import Good
from rest_framework.permissions import IsAuthenticated


class CartAPI(APIView):
    permission_classes = [IsAuthenticated]

    # Lấy chi tiết giỏ hàng (mỗi người chỉ có một giỏ hàng)
    def get(self, request):
        try:
            cart = get_object_or_404(Cart, user=request.user)  # Lấy giỏ hàng của người dùng hiện tại
            cart_goods = CartGood.objects.filter(cart=cart)  # Lấy tất cả sản phẩm trong giỏ
            cart_serializer = CartSerializer(cart)  # Serialize giỏ hàng
            cart_goods_serializer = CartGoodSerializer(cart_goods, many=True)  # Serialize các sản phẩm trong giỏ

            # Trả về dữ liệu giỏ hàng cùng với các sản phẩm trong giỏ
            return Response({
                'cart': cart_serializer.data,
                'cart_goods': cart_goods_serializer.data
            })
        except Cart.DoesNotExist:
            return Response({"detail": "Giỏ hàng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)


"""
lấy thông tin giỏ hàng(gửi token)
{
  "cart": {
        "id": 1,
        "user": 5,
        "note": "asdflaksd"
  },
  "cart_goods": [
    {
      "id": 1,
      "cart": 1,
      "good": {
            #thong tin các thuoc tinh của good
      }
      "quantity": 2
    },
    {
      "id": 2,
      "cart": 1,
      "good": {
            #thong tin các thuoc tinh của good
      }
      "quantity": 1
    }
  ]
}
"""


class CreateCartGoodAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    # Thêm sản phẩm vào giỏ hàng
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)  # Lấy giỏ hàng của người dùng hiện tại
        good_id = request.data.get('good_id')  # ID của sản phẩm cần thêm vào giỏ
        quantity = request.data.get('quantity', 1)  # Số lượng mặc định là 1 nếu không cung cấp

        if quantity <= 0:
            return Response({"detail": "Số lượng sản phẩm phải lớn hơn 0."}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy sản phẩm từ cơ sở dữ liệu
        good = get_object_or_404(Good, id=good_id)

        # Kiểm tra xem sản phẩm có còn trong kho không
        if good.amount == 0:
            return Response({"detail": "Sản phẩm này đã hết hàng."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem sản phẩm đã có trong giỏ hàng của người dùng chưa
        try:
            cart_good = CartGood.objects.get(cart=cart, good=good)
            # Nếu sản phẩm đã có trong giỏ, cập nhật số lượng
            cart_good.quantity += quantity
            cart_good.save()
            return Response({"messege": "Thêm thành công"}, status=status.HTTP_200_OK)
        except CartGood.DoesNotExist:
            # Nếu sản phẩm chưa có trong giỏ, tạo mới
            serializer = CartGoodSerializer(data={'cart': cart.id, 'good': good.id, 'quantity': quantity})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
"""
thêm vào giỏ cần gửi
{
  "good_id": 10,
  "quantity": 2
}
kèm token

"""


class CartGoodAPI(APIView):
    permission_classes = [IsAuthenticated]

    # Cập nhật số lượng sản phẩm trong giỏ hàng
    def patch(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        good_id = request.data.get('good_id')
        new_quantity = request.data.get('quantity')

        if not good_id or new_quantity is None:
            return Response({"detail": "Cần cung cấp mã sản phẩm và số lượng."}, status=status.HTTP_400_BAD_REQUEST)

        cart_good = get_object_or_404(CartGood, cart=cart, good_id=good_id)

        # Kiểm tra tồn kho trước khi thay đổi số lượng
        good = get_object_or_404(Good, id=good_id)
        if good.amount == 0:  # Nếu sản phẩm đã hết hàng
            return Response({"detail": "Sản phẩm này hiện đã hết hàng."}, status=status.HTTP_400_BAD_REQUEST)

        if good.amount < new_quantity:
            return Response({"detail": "Sản phẩm này không đủ số lượng trong kho."}, status=status.HTTP_400_BAD_REQUEST)

        # Nếu số lượng mới hợp lệ, cập nhật giỏ hàng
        if new_quantity <= 0:
            cart_good.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        cart_good.quantity = new_quantity
        cart_good.save()
        serializer = CartGoodSerializer(cart_good)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
CẬP NHẬT CẦN GỬI
{
  "good_id": 10,
  "quantity": 2
}
kèm token

"""

class RemoveGoodFromCartAPI(APIView):
    permission_classes = [IsAuthenticated]

    # Xóa sản phẩm khỏi giỏ hàng
    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        good_id = request.data.get('good_id')
        cart_good = get_object_or_404(CartGood, cart=cart, good_id=good_id)
        cart_good.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
gửi tokent
'''