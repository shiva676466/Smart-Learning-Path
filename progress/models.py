"""
Progress App Models
Progress tracking, XP log, streak management
"""

from django.db import models
from django.contrib.auth.models import User
from roadmap.models import Roadmap, RoadmapTask


class Progress(models.Model):
    """Tracks overall progress per roadmap per user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    roadmap = models.OneToOneField(Roadmap, on_delete=models.CASCADE, related_name='progress')
    tasks_completed = models.IntegerField(default=0)
    total_xp_earned = models.IntegerField(default=0)
    current_day = models.IntegerField(default=1)
    streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Progress'
        verbose_name_plural = 'Progress Records'

    def __str__(self):
        return f"{self.user.username} — {self.roadmap.skill.name} Progress"

    @property
    def completion_percentage(self):
        return self.roadmap.progress_percentage


class XPLog(models.Model):
    """Log of XP earning events"""

    XP_REASONS = [
        ('task_complete', 'Task Completed'),
        ('streak_bonus', 'Streak Bonus'),
        ('roadmap_complete', 'Roadmap Completed'),
        ('daily_login', 'Daily Login'),
        ('perfect_day', 'Perfect Day'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xp_logs')
    reason = models.CharField(max_length=30, choices=XP_REASONS)
    xp_amount = models.IntegerField()
    description = models.CharField(max_length=200)
    earned_at = models.DateTimeField(auto_now_add=True)
    related_task = models.ForeignKey(RoadmapTask, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-earned_at']
        verbose_name = 'XP Log'
        verbose_name_plural = 'XP Logs'

    def __str__(self):
        return f"{self.user.username} +{self.xp_amount} XP ({self.reason})"


class AdaptiveSuggestion(models.Model):
    """Adaptive suggestions when user misses tasks"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    suggestion_text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Suggestion for {self.user.username}"
