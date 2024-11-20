from django.urls import path
from . import views
from django.urls import path
from .views import get_csrf_token




urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('register', views.CreateUserView.as_view(), name='create_user'),
    path('update/', views.UpdateUserView.as_view(), name='update_user'),
    path('login/', views.LoginView.as_view(), name='login_user'),
    path('get_csrf/', get_csrf_token),

]

