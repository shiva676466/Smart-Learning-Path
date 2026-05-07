"""Dashboard views"""

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from roadmap.models import Roadmap
from progress.models import XPLog, AdaptiveSuggestion


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

        ctx = {
            'active_roadmaps': active_roadmaps,
            'completed_roadmaps': completed_roadmaps,
            'recent_xp': recent_xp,
            'suggestions': suggestions,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'profile': user.profile,
        }
        return render(request, self.template_name, ctx)
