from django.contrib import admin
from apps.users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('email', 'name', 'is_staff', 'is_active')
	list_filter = ('is_active', 'is_staff', 'is_superuser')
	search_fields = ('email', 'name')
	ordering = ('email',)