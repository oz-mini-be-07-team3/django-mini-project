from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserTestCase(TestCase):
	# 일반 유저 생성 테스트 함수
	def test_create_user(self):
		email = "asd@gmail.com"
		password = "password123"

		user = get_user_model().objects.create_user(email=email, password=password)

		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_admin)
		self.assertFalse(user.is_superuser)

	# 슈퍼 유저 생성 테스트 함수
	def test_create_superuser(self):
		email = "asd@gmail.com"
		password = "password123"

		user = get_user_model().objects.create_superuser(email=email, password=password, name="superuser")

		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))
		self.assertTrue(user.is_active)
		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_admin)
		self.assertTrue(user.is_superuser)


class UserAPITestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='asd@gmail.com', password='password')
		refresh = RefreshToken.for_user(self.user)
		self.token = str(refresh.access_token)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

	def test_get_user_unauthorized(self):
		self.client.logout()
		# reverse: urls에서 설정한 name으로 views를 역추적
		url = reverse('user_detail', kwargs={'pk': self.user.pk})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_get_user_authorized(self):
		self.client.login(email='asd@gmail.com', password='password')
		url = reverse('user_detail', kwargs={'pk': self.user.pk})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)