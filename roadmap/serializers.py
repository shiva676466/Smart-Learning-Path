"""DRF Serializers for Roadmap API"""

from rest_framework import serializers
from .models import Skill, Roadmap, RoadmapTask


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'slug', 'description', 'category', 'icon', 'color']


class RoadmapTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapTask
        fields = ['id', 'day_number', 'title', 'description', 'task_details',
                  'resource_url', 'resource_title', 'difficulty', 'estimated_minutes',
                  'xp_reward', 'is_completed', 'completed_at']


class RoadmapSerializer(serializers.ModelSerializer):
    tasks = RoadmapTaskSerializer(many=True, read_only=True)
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    total_tasks = serializers.IntegerField(read_only=True)
    completed_tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Roadmap
        fields = ['id', 'title', 'skill_name', 'level', 'daily_hours', 'duration_days',
                  'status', 'start_date', 'target_end_date', 'progress_percentage',
                  'total_tasks', 'completed_tasks_count', 'tasks', 'created_at']
