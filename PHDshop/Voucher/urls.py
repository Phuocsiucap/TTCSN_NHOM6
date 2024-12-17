from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_vouchers, name='get_vouchers'),
    path('redeem/', views.redeem_voucher, name='redeem_voucher'),
]
