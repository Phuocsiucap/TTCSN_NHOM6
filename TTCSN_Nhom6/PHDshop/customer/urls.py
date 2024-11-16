from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="homePage"),
    path('register', views.CreateUserView.as_view(), name='create_user'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(), name='update_user'),
    path('login/', views.LoginView.as_view(), name='login_user'),
]