"""REST API views for roadmap operations"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from .models import Skill, Roadmap, RoadmapTask
from .serializers import SkillSerializer, RoadmapSerializer
from progress.models import XPLog, Progress


class SkillListAPI(APIView):
    def get(self, request):
        skills = Skill.objects.filter(is_active=True)
        return Response(SkillSerializer(skills, many=True).data)


class RoadmapListAPI(APIView):
    def get(self, request):
        roadmaps = Roadmap.objects.filter(user=request.user)
        return Response(RoadmapSerializer(roadmaps, many=True).data)


class RoadmapDetailAPI(APIView):
    def get(self, request, pk):
        roadmap = get_object_or_404(Roadmap, pk=pk, user=request.user)
        return Response(RoadmapSerializer(roadmap).data)


class CompleteTaskAPI(APIView):
    """Toggle task completion status and award XP"""

    def post(self, request, pk):
        task = get_object_or_404(RoadmapTask, pk=pk, roadmap__user=request.user)
        profile = request.user.profile
        roadmap = task.roadmap

        if task.is_completed:
            # Undo completion
            task.is_completed = False
            task.completed_at = None
            task.save()

            xp_change = -task.xp_reward

            # If roadmap was previously completed, reopen it and remove completion bonus.
            if roadmap.status == 'completed':
                roadmap.status = 'active'
                roadmap.completed_at = None
                roadmap.save(update_fields=['status', 'completed_at'])
                xp_change -= 100

            profile.total_xp = max(0, profile.total_xp + xp_change)
            profile.save(update_fields=['total_xp'])

            progress, _ = Progress.objects.get_or_create(user=request.user, roadmap=roadmap)
            completed_xp = roadmap.tasks.filter(is_completed=True).aggregate(total=Sum('xp_reward'))['total'] or 0
            progress.tasks_completed = roadmap.completed_tasks_count
            progress.total_xp_earned = completed_xp
            progress.save(update_fields=['tasks_completed', 'total_xp_earned', 'updated_at'])

            return Response({
                'status': 'uncompleted',
                'xp_change': xp_change,
                'total_xp': profile.total_xp,
                'progress': roadmap.progress_percentage,
            })
        else:
            # Mark complete
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save()

            # Award XP
            profile.total_xp += task.xp_reward
            xp_change = task.xp_reward

            # Log XP
            XPLog.objects.create(
                user=request.user,
                reason='task_complete',
                xp_amount=task.xp_reward,
                description=f'Completed: {task.title}',
                related_task=task
            )

            # Update progress
            progress, _ = Progress.objects.get_or_create(
                user=request.user, roadmap=roadmap
            )
            completed_xp = roadmap.tasks.filter(is_completed=True).aggregate(total=Sum('xp_reward'))['total'] or 0
            progress.tasks_completed = roadmap.completed_tasks_count
            progress.total_xp_earned = completed_xp
            progress.save(update_fields=['tasks_completed', 'total_xp_earned', 'updated_at'])

            # Check if roadmap is complete
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

            return Response({
                'status': 'completed',
                'xp_change': xp_change,
                'total_xp': profile.total_xp,
                'progress': roadmap.progress_percentage,
            })
