from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path("api/v1/transactions/", include("apps.transaction_history.urls")),
]
# api가 여러개 생기면서 버전이 바뀌는 경우가 많다
# 개발환경에서는 여러 버전을 관리하고 배포환경에서는 배포할 버전만 urls 경로 설정