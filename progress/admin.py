from django.contrib import admin
from .models import Progress, XPLog, AdaptiveSuggestion


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'roadmap', 'tasks_completed', 'total_xp_earned', 'streak', 'updated_at']
    list_filter = ['streak']
    search_fields = ['user__username']


@admin.register(XPLog)
class XPLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'xp_amount', 'description', 'earned_at']
    list_filter = ['reason']
    search_fields = ['user__username', 'description']


@admin.register(AdaptiveSuggestion)
class AdaptiveSuggestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'roadmap', 'is_read', 'created_at']
    list_filter = ['is_read']
