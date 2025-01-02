from django.urls import path
from .views import AccountListApiView, AccountDeleteAPIView

urlpatterns = [
    path('', AccountListApiView.as_view(), name='account-list-create'),  # 계좌 목록 조회 및 생성
    path('<int:pk>/', AccountDeleteAPIView.as_view(), name='account-delete'),  # 계좌 삭제
]
