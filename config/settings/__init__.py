from .base import *

environment = env('DJANGO_ENV', default='development')

if environment == 'production':
    from .production import *
else:
    from .development import *