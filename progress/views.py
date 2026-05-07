"""Progress tracking views"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from .models import XPLog
from roadmap.models import RoadmapTask
from users.models import UserProfile


@method_decorator(login_required, name='dispatch')
class ToggleTaskView(View):
    """HTMX-friendly task toggle"""

    def post(self, request, task_id):
        task = get_object_or_404(RoadmapTask, pk=task_id, roadmap__user=request.user)
        task.is_completed = not task.is_completed
        task.completed_at = timezone.now() if task.is_completed else None
        task.save()

        if task.is_completed:
            profile = request.user.profile
            profile.total_xp += task.xp_reward
            profile.save()
            XPLog.objects.create(
                user=request.user,
                reason='task_complete',
                xp_amount=task.xp_reward,
                description=f'Completed: {task.title}',
                related_task=task
            )

        return JsonResponse({
            'completed': task.is_completed,
            'progress': task.roadmap.progress_percentage,
            'xp': request.user.profile.total_xp,
        })


@method_decorator(login_required, name='dispatch')
class LeaderboardView(View):
    template_name = 'progress/leaderboard.html'

    def get(self, request):
        profiles = UserProfile.objects.select_related('user').order_by('-total_xp')[:20]
        return render(request, self.template_name, {
            'profiles': profiles,
            'user_rank': self._get_user_rank(request.user),
        })

    def _get_user_rank(self, user):
        higher = UserProfile.objects.filter(total_xp__gt=user.profile.total_xp).count()
        return higher + 1
