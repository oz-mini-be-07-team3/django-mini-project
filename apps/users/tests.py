from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


data = {'email': 'asd@gmail.com', 'password': 'password'}
super_data = {'email': 'as@gmail.com', 'password': 'password'}


class APITestCaseSetUp(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email=data['email'], password=data['password'])
		refresh = RefreshToken.for_user(self.user)
		self.token = str(refresh.access_token)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")


class CreateUserAuthorizedTestCase(APITestCaseSetUp):
	# 일반 유저 생성 시 권한 부여 테스트 함수
	def test_create_user(self):
		self.assertEqual(self.user.email, data['email'])
		self.assertTrue(self.user.check_password(data['password']))
		self.assertTrue(self.user.is_active)
		self.assertFalse(self.user.is_staff)
		self.assertFalse(self.user.is_admin)
		self.assertFalse(self.user.is_superuser)

	# 슈퍼 유저 생성 시 권한 부여 테스트 함수
	def test_create_superuser(self):
		super_user = get_user_model().objects.create_superuser(
			email=super_data['email'], password=super_data['password'], name="superuser"
		)
		self.assertEqual(super_user.email, super_data['email'])
		self.assertTrue(super_user.check_password(super_data['password']))
		self.assertTrue(super_user.is_active)
		self.assertTrue(super_user.is_staff)
		self.assertTrue(super_user.is_admin)
		self.assertTrue(super_user.is_superuser)


class JWTAuthTestCase(APITestCaseSetUp):
	# 로그인 성공 테스트
	def test_login_success(self):
		url = reverse('login')
		response = self.client.post(url, data={'email': data['email'], 'password': data['password']})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)
		self.assertIn('refresh', response.data)

	# 로그아웃 성공 테스트
	def test_logout_success(self):
		refresh = RefreshToken.for_user(self.user)
		url = reverse('logout')
		response = self.client.post(url, data={'refresh': str(refresh)})
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserAPITestCase(APITestCaseSetUp):
	# C


	# R
	def test_get_user_unauthorized(self):
		self.client.logout()
		# reverse: urls에서 설정한 name으로 views를 역추적
		url = reverse('user_detail', kwargs={'pk': self.user.pk})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_get_user_authorized(self):
		self.client.login(email=data['email'], password=data['password'])
		url = reverse('user_detail', kwargs={'pk': self.user.pk})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	# U


	# D