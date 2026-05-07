from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['experience_level', 'daily_study_hours', 'total_xp', 'streak_days', 'bio']


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Customize admin header
admin.site.site_header = "LearnPathAI Admin"
admin.site.site_title = "LearnPathAI"
admin.site.index_title = "Learning Platform Administration"
