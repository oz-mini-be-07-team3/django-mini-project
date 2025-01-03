from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # 로컬만 허용

INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'apps.users.apps.UsersConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.transaction_history.apps.TransactionHistoryConfig',
    'drf_spectacular',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': env('DB_PORT', default='5432'),
    }
}