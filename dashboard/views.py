"""Dashboard views"""

import json

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from roadmap.models import Roadmap, RoadmapTask
from progress.models import XPLog, AdaptiveSuggestion

from .retention import compute_retention


class HomeView(View):
    """Public home/landing page"""
    template_name = 'dashboard/home.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        user = request.user
        active_roadmaps = Roadmap.objects.filter(user=user, status='active').order_by('-created_at')
        completed_roadmaps = Roadmap.objects.filter(user=user, status='completed').count()
        recent_xp = XPLog.objects.filter(user=user).order_by('-earned_at')[:5]
        suggestions = AdaptiveSuggestion.objects.filter(user=user, is_read=False)[:3]

        # Stats
        total_tasks = sum(r.total_tasks for r in active_roadmaps)
        completed_tasks = sum(r.completed_tasks_count for r in active_roadmaps)

        # Today's Task: lowest day_number incomplete task from the most
        # recently created active roadmap.
        next_task = (
            RoadmapTask.objects
            .filter(roadmap__user=user, roadmap__status='active', is_completed=False)
            .order_by('-roadmap__created_at', 'day_number')
            .select_related('roadmap', 'roadmap__skill')
            .first()
        )

        ctx = {
            'active_roadmaps': active_roadmaps,
            'completed_roadmaps': completed_roadmaps,
            'recent_xp': recent_xp,
            'suggestions': suggestions,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'profile': user.profile,
            'next_task': next_task,
        }
        return render(request, self.template_name, ctx)


@method_decorator(staff_member_required, name='dispatch')
class RetentionStatsView(View):
    template_name = 'dashboard/retention.html'

    def get(self, request):
        stats = compute_retention()
        ctx = {
            'stats': stats,
            'daily_series_json': json.dumps(stats['daily_series']),
        }
        return render(request, self.template_name, ctx)
