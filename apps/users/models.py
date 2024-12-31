from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.common.models import CommonModel

# 사용자 관리 기능(생성, 삭제 등)
class UserManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError("이메일 주소는 필수입니다.")
		if not password:
			raise ValueError("비밀번호는 필수입니다.")
		email = self.normalize_email(email) # 이메일 정규화
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		# self._db는 UserManager에서 사용 중인 데이터베이스를 말함
		user.save(using=self._db) # 다중 데이터 베이스를 사용하는 상황에서 정확히 지정해주기 위함이지만 단일에서도 관례적으로 사용
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_admin', True)
		extra_fields.setdefault('is_superuser', True)

		if not extra_fields.get('is_staff'):
			raise ValueError('superuser는 staff여야 합니다.')
		if not extra_fields.get('is_superuser'):
			raise ValueError('superuser는 is_superuser가 True여야 합니다.')

		return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, CommonModel, PermissionsMixin):
	# verbose_name은 admin페이지에서 보이는 이름
	email = models.EmailField(unique=True, verbose_name='이메일 주소')
	name = models.CharField(max_length=50, verbose_name='이름')
	nickname = models.CharField(max_length=50, blank=True, null=True, default=name, verbose_name='별명')
	contact = models.CharField(max_length=255, null=True, verbose_name='연락처')
	is_active = models.BooleanField(default=True, verbose_name='계정 활성화 여부')
	is_staff = models.BooleanField(default=False, verbose_name='스태프 권한 여부')
	is_admin = models.BooleanField(default=False, verbose_name='관리자 권한 여부')

	# 사용자 인증에 필요할 필드 정의!
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] # create_superuser에서 필수로 요구되는 추가 필드

	objects = UserManager()

	class Meta:
		verbose_name = '사용자' # 모델 들어갔을 때 타이틀
		verbose_name_plural = '사용자들' # 모델 이름

	# 이름을 객체 이름이 아니라 email로 변경
	def __str__(self):
		return self.email

