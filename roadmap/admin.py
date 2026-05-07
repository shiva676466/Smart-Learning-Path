from django.contrib import admin
from .models import Skill, Topic, Resource, Roadmap, RoadmapTask


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill', 'level', 'difficulty', 'estimated_hours', 'xp_reward']
    list_filter = ['skill', 'level', 'difficulty']
    search_fields = ['name']
    ordering = ['skill', 'level', 'order']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'resource_type', 'platform', 'is_free']
    list_filter = ['resource_type', 'is_free']
    search_fields = ['title', 'platform']


class RoadmapTaskInline(admin.TabularInline):
    model = RoadmapTask
    extra = 0
    fields = ['day_number', 'title', 'difficulty', 'is_completed', 'xp_reward']
    readonly_fields = ['is_completed', 'completed_at']


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'skill', 'level', 'duration_days', 'status', 'progress_percentage', 'created_at']
    list_filter = ['status', 'level', 'skill']
    search_fields = ['user__username', 'skill__name']
    inlines = [RoadmapTaskInline]
    readonly_fields = ['progress_percentage', 'total_tasks', 'completed_tasks_count']


@admin.register(RoadmapTask)
class RoadmapTaskAdmin(admin.ModelAdmin):
    list_display = ['roadmap', 'day_number', 'title', 'difficulty', 'is_completed', 'xp_reward']
    list_filter = ['is_completed', 'difficulty']
    search_fields = ['title', 'roadmap__user__username']
