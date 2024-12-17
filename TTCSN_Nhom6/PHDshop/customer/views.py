from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer



class UserProfileView(APIView):
    # Không cần thêm `permission_classes` ở đây nếu middleware đã xác thực
    def get(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)

        # Lấy thông tin người dùng từ request.user
        user_data = UserSerializer(request.user)
        print("hello")

        print("hi")
        return Response({'user': user_data.data}, status=200)

class CreateUserView(APIView):
    permission_classes = [AllowAny]  #Cho phép tất cả người dùng truy cập
    print(6)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(APIView):
    
    def put(self, request):
        #Dữ liệu người dùng đã đăng nhập từ request.user
        user = request.user
        print("ahhh")
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
         #Dữ liệu người dùng đã đăng nhập từ request.user
        user = request.user
        print("bad")
        print(user)
        serializer = UserSerializer(user, data=request.data, partial=True)   #partial=True cho phép cập nhật một phần

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            if user.password == password:
                serializer=UserSerializer(user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)  
                refresh_token = str(refresh) 
                print(f"Access Token: {access_token}")
                return Response(
                    {
                    "message": "Login successful!",
                    "user":serializer.data,
                    "access_token": access_token,
                    "refresh_token": refresh_token 
                    }, 
                    status=status.HTTP_200_OK
                    )
            else:
                return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        

