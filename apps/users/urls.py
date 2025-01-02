from django.urls import path
from apps.users.views import UserView, UserDetailView, JWTLoginView, JWTLogoutView
from rest_framework_simplejwt.views import (
	TokenVerifyView, TokenRefreshView, TokenObtainPairView
)

urlpatterns = [
	path('verify/', TokenVerifyView.as_view(), name='verify'),
	path('refresh/', TokenRefreshView.as_view(), name='refresh'),
	path('obtain/', TokenObtainPairView.as_view(), name='obtain'),
	path('', UserView.as_view(), name='users'),
	path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
	path('login/', JWTLoginView.as_view(), name='login'),
	path('logout/', JWTLogoutView.as_view(), name='logout'),
]