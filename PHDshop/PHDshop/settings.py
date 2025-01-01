"""
Django settings for PHDshop project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z=fzuyb&*q!itxsz@$&mpb=b3t!_#qjtq^p&=9l5@lv*r@6%h-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer',
    'good',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'Cart', 
    'Order',
    'rest_framework_simplejwt',
    'Voucher',
    'Admin',
    'vnpay_python',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',  
    # tạo phuong thức xác thục
    'customer.middlewares.JWTAuthenticationMiddleware',
    'customer.middlewares.DisableCSRFMiddleware',
   
]

# Đảm bảo rằng bạn cấu hình đúng CORS nếu frontend và backend khác domain
CORS_ALLOW_ALL_ORIGINS = True  # Chỉ nên sử dụng trong môi trường phát triển



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


ROOT_URLCONF = 'PHDshop.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PHDshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'PHDShop',        # Tên cơ sở dữ liệu
#         'USER': 'root',           # Tên người dùng MySQL
#         'PASSWORD': 'nguyenphuoc',              # Mật khẩu cho tài khoản MySQL
#         'HOST': '127.0.0.1',                 # Địa chỉ của máy chủ (có thể là 'localhost' hoặc địa chỉ IP)
#         'PORT': '3306',                      # Cổng MySQL, thường là 3306
#     }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Cấu hình SimpleJWT (Optional, có thể thay đổi giá trị theo nhu cầu)
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=150),  # Thời gian sống của Access Token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Thời gian sống của Refresh Token
    'ROTATE_REFRESH_TOKENS': True,  # Có thay thế Refresh Token mỗi khi cấp mới không
    'BLACKLIST_AFTER_ROTATION': True,  # Hủy Refresh Token đã được sử dụng
}


CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Your React app URL
]

CORS_ALLOW_CREDENTIALS = True  # Allows sending cookies with requests



# Cấu hình chi tiết hơn cho CORS
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
]





VNPAY_RETURN_URL = 'http://localhost:8888/order'  # get from config
VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # get from config
VNPAY_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/api/transaction'
VNPAY_TMN_CODE = 'BXZ1FFWP'  # Website ID in VNPAY System, get from config
VNPAY_HASH_SECRET_KEY = 'IQO729Q6MAIXXHLH0QHGIERNXYW6DRB0'  # Secret key for create checksum,get from config
