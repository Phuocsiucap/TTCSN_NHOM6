from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

# class HomePage(APIView):
     # def get(self, request):
     #     data = {
     #         "title": "Welcome to My Home Page",
     #         "description": "This is the home page of my application."
     #     }
     #     return Response(data)
    # def get(self, request):
    #     # Lấy tất cả người dùng
    #     users = User.objects.all()
    #     # Serialize dữ liệu người dùng
    #     user_serializer = UserSerializer(users, many=True)
    #     # Trả về danh sách người dùng dưới dạng JSON
    #     return Response(user_serializer.data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Đảm bảo rằng người dùng đã được xác thực
    
    def get(self, request):
        # Lấy thông tin người dùng từ request.user (đã xác thực thông qua token)
        user = request.user
        return Response(user, status=status.HTTP_200_OK)
    

class CreateUserView(APIView):
    permission_classes = [AllowAny]  # Cho phép tất cả người dùng truy cập

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUserView(APIView):
    # def put(self, request, pk):
    #     user = get_object_or_404(User, pk=pk)
    #     serializer = UserSerializer(user, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, pk):
    #     user = get_object_or_404(User, pk=pk)
    #     serializer = UserSerializer(user, data=request.data, partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Dữ liệu người dùng đã đăng nhập từ request.user
        user = request.user
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # Dữ liệu người dùng đã đăng nhập từ request.user
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True cho phép cập nhật một phần

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]  # Cho phép tất cả người dùng truy cập
    # def post(self, request):
    #     email = request.data.get("email")
    #     password = request.data.get("password")
    #     try:
    #         user = User.objects.get(email=email)
    #         serializer = UserSerializer(user)
    #         if user.password == password:
    #             return Response({"message": "Login successful!", "user": serializer.data}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
    #     except User.DoesNotExist:
    #         return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)



    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            print("1")
            if user.password == password:
                print(user)
                if isinstance(user, User): 
                    print(4)
                    token, created = Token.objects.get_or_create(user=user)
                    print(3)
                    return Response({"token": token.key, "user": {"id": user.id, "email": user.email}}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid user instance."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)