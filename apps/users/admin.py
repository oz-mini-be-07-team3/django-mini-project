from django.contrib import admin
from apps.users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	# 표시할 컬럼
	list_display = ('email', 'nickname', 'contact', 'is_staff', 'is_active')
	# 검색 기능 설정
	search_fields = ('email', 'nickname', 'contact')
	# 필터링 조건
	list_filter = ('is_active', 'is_staff', 'is_admin', 'is_superuser')

	# 읽기 오버라이드
	def get_readonly_fields(self, request, obj=None):
		readonly_fields = super().get_readonly_fields(request, obj)
		# staff랑 admin은 아래 필드 읽기만 가능
		if not request.user.is_superuser:
			readonly_fields += ('is_admin', 'is_superuser',)

		# staff는 아래 필드 읽기만 가능
		if not request.user.is_admin:
			readonly_fields += ('is_staff',)

		return readonly_fields