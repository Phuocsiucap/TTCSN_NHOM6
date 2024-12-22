from django.http import JsonResponse
from customer.models import User
import jwt
from datetime import datetime
from PHDshop.settings import SECRET_KEY

# Giải mã token và kiểm tra tính hợp lệ
def verify_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Kiểm tra thời gian hết hạn của token
        exp_timestamp = decoded_token.get('exp')
        if exp_timestamp and exp_timestamp < datetime.now().timestamp():
            return None  # Token đã hết hạn

        # Nếu token hợp lệ, trả về thông tin người dùng
        return decoded_token

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


# Lấy thông tin người dùng từ user_id trong token
def get_user_from_token(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None


# Middleware xác thực JWT
class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kiểm tra xem request có phải là admin hay không, nếu là admin thì bỏ qua xác thực
        if request.path.startswith('/api/admin/'):
            return self.get_response(request)
        print(2)
        # Kiểm tra token trong header Authorization
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(' ')[1]  # Lấy token từ "Bearer <token>"

            user_data = verify_jwt(token)
            if user_data:
                user = get_user_from_token(user_data['user_id'])
                if user:
                    request.user = user  # Gán thông tin người dùng vào request
                    return self.get_response(request)
                else:
                    return JsonResponse({'detail': 'User not found'}, status=404)
            else:
                return JsonResponse({'detail': 'Invalid or expired token'}, status=401)

        # Nếu không có token hoặc token không hợp lệ, bỏ qua xác thực
        return JsonResponse({'detail': 'Authorization header missing or invalid'}, status=401)

class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)
