from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path("api/v1/transactions/", include("apps.transaction_history.urls")),
]