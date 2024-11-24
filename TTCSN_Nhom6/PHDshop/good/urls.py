from django.urls import path
from .views import GoodListView, GoodDetailView


urlpatterns = [
    path('list', GoodListView.as_view(), name='good-list'),
    path('list/<int:id>/', GoodDetailView.as_view(), name='good-detail'),  # <int:id> captures the product ID
]