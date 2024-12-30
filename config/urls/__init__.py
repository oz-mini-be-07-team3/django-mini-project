import os

env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    from .production import urlpatterns
else:
    from .development import urlpatterns
