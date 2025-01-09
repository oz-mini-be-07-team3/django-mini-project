from django.test import TestCase
from django.contrib.auth import get_user_model

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