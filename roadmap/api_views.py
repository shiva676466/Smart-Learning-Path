"""REST API views for roadmap operations"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Skill, Roadmap, RoadmapTask
from .serializers import SkillSerializer, RoadmapSerializer
from progress.models import XPLog, Progress
from users.models import UserProfile


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

        if task.is_completed:
            # Undo completion
            task.is_completed = False
            task.completed_at = None
            task.save()
            # Deduct XP
            profile = request.user.profile
            profile.total_xp = max(0, profile.total_xp - task.xp_reward)
            profile.save()
            return Response({'status': 'uncompleted', 'xp_change': -task.xp_reward})
        else:
            # Mark complete
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save()

            # Award XP
            profile = request.user.profile
            profile.total_xp += task.xp_reward
            profile.save()

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
                user=request.user, roadmap=task.roadmap
            )
            progress.tasks_completed = task.roadmap.completed_tasks_count
            progress.total_xp_earned += task.xp_reward
            progress.save()

            # Check if roadmap is complete
            if task.roadmap.progress_percentage == 100:
                task.roadmap.status = 'completed'
                task.roadmap.completed_at = timezone.now()
                task.roadmap.save()
                bonus_xp = 100
                profile.total_xp += bonus_xp
                profile.save()
                XPLog.objects.create(
                    user=request.user,
                    reason='roadmap_complete',
                    xp_amount=bonus_xp,
                    description=f'Completed roadmap: {task.roadmap.title}'
                )

            return Response({
                'status': 'completed',
                'xp_change': task.xp_reward,
                'total_xp': profile.total_xp,
                'progress': task.roadmap.progress_percentage,
            })
