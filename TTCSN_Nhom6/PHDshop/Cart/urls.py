from django.urls import path
from .views import CartAPI, CreateCartGoodAPI, CartGoodAPI, RemoveGoodFromCartAPI

urlpatterns = [
    # Lấy chi tiết giỏ hàng
    path('', CartAPI.as_view(), name='cart-detail'),

    # Thêm sản phẩm vào giỏ hàng
    path('add/', CreateCartGoodAPI.as_view(), name='cart-add-good'),

    # Cập nhật số lượng sản phẩm trong giỏ hàng
    path('update/', CartGoodAPI.as_view(), name='cart-update-good'),

    # Xóa sản phẩm khỏi giỏ hàng
    path('remove/', RemoveGoodFromCartAPI.as_view(), name='cart-remove-good'),
]
