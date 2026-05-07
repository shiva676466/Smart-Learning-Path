"""
Roadmap App Models
Skill, Topic, Resource, Roadmap, RoadmapTask
"""

from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    """A learnable skill (e.g. DSA, Web Dev, AI/ML)"""

    CATEGORY_CHOICES = [
        ('cs_fundamentals', 'CS Fundamentals'),
        ('web_development', 'Web Development'),
        ('data_science', 'Data Science & AI'),
        ('programming', 'Programming Languages'),
        ('competitive', 'Competitive Programming'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, default='📚')  # emoji icon
    color = models.CharField(max_length=20, default='#6366f1')  # hex color
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name


class Topic(models.Model):
    """A specific topic within a skill"""

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    DIFFICULTY_CHOICES = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Medium'),
        (4, 'Hard'),
        (5, 'Very Hard'),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=2)
    estimated_hours = models.FloatField(default=1.0)
    order = models.IntegerField(default=0)  # ordering within skill+level
    xp_reward = models.IntegerField(default=10)

    class Meta:
        ordering = ['skill', 'level', 'order']
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        return f"{self.skill.name} → {self.name} ({self.level})"


class Resource(models.Model):
    """Learning resource linked to a topic"""

    RESOURCE_TYPES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('documentation', 'Documentation'),
        ('practice', 'Practice Platform'),
        ('book', 'Book / PDF'),
        ('course', 'Online Course'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='article')
    is_free = models.BooleanField(default=True)
    platform = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'

    def __str__(self):
        return f"{self.title} ({self.resource_type})"


class Roadmap(models.Model):
    """A user's generated learning roadmap"""

    DURATION_CHOICES = [
        (15, '15 Days'),
        (30, '30 Days'),
        (60, '60 Days'),
        (90, '90 Days'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmaps')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    daily_hours = models.FloatField(default=1.0)
    duration_days = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField(auto_now_add=True)
    target_end_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Roadmap'
        verbose_name_plural = 'Roadmaps'

    def __str__(self):
        return f"{self.user.username} — {self.skill.name} ({self.level})"

    @property
    def total_tasks(self):
        return self.tasks.count()

    @property
    def completed_tasks_count(self):
        return self.tasks.filter(is_completed=True).count()

    @property
    def progress_percentage(self):
        total = self.total_tasks
        if total == 0:
            return 0
        return round((self.completed_tasks_count / total) * 100, 1)


class RoadmapTask(models.Model):
    """Individual day-wise task in a roadmap"""

    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='tasks')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    day_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    task_details = models.TextField()  # specific tasks to do
    resource_url = models.URLField(blank=True)
    resource_title = models.CharField(max_length=200, blank=True)
    difficulty = models.IntegerField(default=2, choices=[(i, str(i)) for i in range(1, 6)])
    estimated_minutes = models.IntegerField(default=60)
    xp_reward = models.IntegerField(default=10)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['roadmap', 'day_number']
        unique_together = ['roadmap', 'day_number']
        verbose_name = 'Roadmap Task'
        verbose_name_plural = 'Roadmap Tasks'

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"
