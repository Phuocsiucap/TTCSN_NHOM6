import requests
import jwt

SECRET_KEY = 'django-insecure-z=fzuyb&*q!itxsz@$&mpb=b3t!_#qjtq^p&=9l5@lv*r@6%h-'

def decode_jwt(token):
    try:
        # Giải mã mà không xác minh chữ ký để tránh cần SECRET_KEY
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

# URL của API backend để đăng nhập và nhận token
login_url = "http://127.0.0.1:8888/api/user/login/"

# Thông tin đăng nhập
login_data = {
    "email": "duynguyen@gmail.com",
    "password": "123456"
}

# Gửi yêu cầu POST để đăng nhập và lấy token
response = requests.post(login_url, json=login_data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
else:
    print("Error:", response.status_code)
    print(response.json())
    exit()



import requests

# URL để lấy CSRF token (thường là trang chính hoặc API nào đó)
csrf_url = "http://127.0.0.1:8888/api/user/get_csrf/"

# Gửi yêu cầu GET để lấy CSRF token
session = requests.Session()  # Sử dụng session để duy trì cookie
csrf_response = session.get(csrf_url)

# Lấy token từ cookie
csrf_token = csrf_response.cookies.get('csrftoken')

print("CSRF Token:", csrf_token)


# URL để thêm sản phẩm vào giỏ hàng
post_url = "http://127.0.0.1:8888/api/cart/"

# Headers với CSRF token và Access Token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token,  # Thêm CSRF token vào đây
}

# # Dữ liệu gửi đến API
# body = {
#     "good_id": 10,
#     "quantity": 2
# }

# Gửi yêu cầu POST
response = session.get(post_url, headers=headers)

# Kiểm tra kết quả
if response.status_code == 200:
    print("Thành công:", response.json())
else:
    print("Lỗi:", response.status_code)
    print(response.json())
