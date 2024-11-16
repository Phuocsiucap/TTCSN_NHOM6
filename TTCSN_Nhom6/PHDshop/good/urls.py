from django.urls import path
from .views import GoodListView


urlpatterns = [
    path('list', GoodListView.as_view(), name='good-list'),
]