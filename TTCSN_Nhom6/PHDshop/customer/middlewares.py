import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header:
            try:
                # Tách "Bearer" và token
                prefix, token = auth_header.split(' ')
                if prefix != 'Bearer':
                    raise AuthenticationFailed('Invalid token prefix')
                
                # Xác thực token
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                request.user = jwt_auth.get_user(validated_token)
                print(request.user)

            except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError) as e:
                raise AuthenticationFailed(f"JWT Authentication Failed: {e}")
        
        else:
            request.user = None  # Nếu không có token, request.user sẽ là None
