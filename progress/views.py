"""Progress tracking views"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from .models import XPLog, Progress
from roadmap.models import RoadmapTask
from users.models import UserProfile


@method_decorator(login_required, name='dispatch')
class ToggleTaskView(View):
    """HTMX-friendly task toggle"""

    def post(self, request, task_id):
        task = get_object_or_404(RoadmapTask, pk=task_id, roadmap__user=request.user)
        profile = request.user.profile
        roadmap = task.roadmap

        if task.is_completed:
            task.is_completed = False
            task.completed_at = None
            task.save()

            xp_change = -task.xp_reward

            if roadmap.status == 'completed':
                roadmap.status = 'active'
                roadmap.completed_at = None
                roadmap.save(update_fields=['status', 'completed_at'])
                xp_change -= 100

            profile.total_xp = max(0, profile.total_xp + xp_change)
            profile.save(update_fields=['total_xp'])
        else:
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save()

            profile.total_xp += task.xp_reward
            xp_change = task.xp_reward
            XPLog.objects.create(
                user=request.user,
                reason='task_complete',
                xp_amount=task.xp_reward,
                description=f'Completed: {task.title}',
                related_task=task
            )

            if roadmap.progress_percentage == 100 and roadmap.status != 'completed':
                roadmap.status = 'completed'
                roadmap.completed_at = timezone.now()
                roadmap.save(update_fields=['status', 'completed_at'])
                bonus_xp = 100
                profile.total_xp += bonus_xp
                xp_change += bonus_xp
                XPLog.objects.create(
                    user=request.user,
                    reason='roadmap_complete',
                    xp_amount=bonus_xp,
                    description=f'Completed roadmap: {roadmap.title}'
                )

            profile.save(update_fields=['total_xp'])

        progress, _ = Progress.objects.get_or_create(user=request.user, roadmap=roadmap)
        completed_xp = roadmap.tasks.filter(is_completed=True).aggregate(total=Sum('xp_reward'))['total'] or 0
        progress.tasks_completed = roadmap.completed_tasks_count
        progress.total_xp_earned = completed_xp
        progress.save(update_fields=['tasks_completed', 'total_xp_earned', 'updated_at'])

        return JsonResponse({
            'completed': task.is_completed,
            'progress': roadmap.progress_percentage,
            'xp': profile.total_xp,
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
