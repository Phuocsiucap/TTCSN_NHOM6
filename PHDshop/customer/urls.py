from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('register', views.CreateUserView.as_view(), name='create_user'),
    path('update/', views.UpdateUserView.as_view(), name='update_user'),
    path('login/', views.LoginView.as_view(), name='login_user'),
    path('<str:username>/submit-score/', views.submit_score, name='submit_score'),
]

