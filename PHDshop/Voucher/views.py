# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Voucher, VoucherUser
from .serializers import VoucherSerializer, VoucherUserSerializer
from customer.models import User

@api_view(['GET'])
def get_vouchers(request):
    """
    API để lấy danh sách voucher
    """
    vouchers = Voucher.objects.filter(is_active=True)
    serializer = VoucherSerializer(vouchers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def redeem_voucher(request):
    """
    API để đổi voucher sử dụng điểm của người dùng
    """
    user = request.user  # Lấy người dùng từ request
    points = user.loyaltyPoints
    voucher_id = request.data.get('voucher_id')
    quantity = request.data.get('quantity', 1)

    try:
        voucher = Voucher.objects.get(id=voucher_id)
    except Voucher.DoesNotExist:
        return Response({"detail": "Voucher not found."}, status=status.HTTP_404_NOT_FOUND)

    # Kiểm tra điều kiện đổi voucher
    total_points_required = voucher.points_required * quantity

    if points < total_points_required:
        return Response({"detail": "Not enough points to redeem this voucher."}, status=status.HTTP_400_BAD_REQUEST)
    
    if voucher.quantity < quantity:
        return Response({"detail": "Not enough vouchers available."}, status=status.HTTP_400_BAD_REQUEST)

    # Tiến hành giảm điểm và số lượng voucher
    user.loyaltyPoints -= total_points_required
    voucher.quantity -= quantity
    user.save()
    voucher.save()

    # Tạo bản ghi trong VoucherUser
    voucher_user = VoucherUser.objects.create(
        user=user,
        voucher=voucher,
        points_used=total_points_required,
        quantity=quantity,
        status="redeemed"
    )

    # Trả về thông tin voucher đã đổi
    voucher_user_serializer = VoucherUserSerializer(voucher_user)
    return Response(voucher_user_serializer.data, status=status.HTTP_201_CREATED)
