"""Roadmap app views"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from .forms import RoadmapGenerateForm
from .models import Roadmap, RoadmapTask, Skill
from .generator import generate_roadmap
from progress.models import Progress


@method_decorator(login_required, name='dispatch')
class GenerateRoadmapView(View):
    template_name = 'roadmap/generate.html'

    def get(self, request):
        form = RoadmapGenerateForm()
        skills = Skill.objects.filter(is_active=True)
        return render(request, self.template_name, {'form': form, 'skills': skills})

    def post(self, request):
        form = RoadmapGenerateForm(request.POST)
        if form.is_valid():
            skill = form.cleaned_data['skill']
            level = form.cleaned_data['level']
            daily_hours = float(form.cleaned_data['daily_hours'])
            duration_days = int(form.cleaned_data['duration_days'])

            # Generate the roadmap
            roadmap = generate_roadmap(request.user, skill, level, daily_hours, duration_days)

            # Create progress tracking record
            Progress.objects.get_or_create(
                user=request.user,
                roadmap=roadmap,
                defaults={'current_day': 1}
            )

            messages.success(request, f'🗺️ Your {skill.name} roadmap has been generated! Time to start learning!')
            return redirect('roadmap:detail', pk=roadmap.pk)

        skills = Skill.objects.filter(is_active=True)
        return render(request, self.template_name, {'form': form, 'skills': skills})


@method_decorator(login_required, name='dispatch')
class RoadmapDetailView(View):
    template_name = 'roadmap/detail.html'

    def get(self, request, pk):
        roadmap = get_object_or_404(Roadmap, pk=pk, user=request.user)
        tasks = roadmap.tasks.all().order_by('day_number')
        progress = getattr(roadmap, 'progress', None)

        # Group tasks by week
        weeks = {}
        for task in tasks:
            week = ((task.day_number - 1) // 7) + 1
            if week not in weeks:
                weeks[week] = []
            weeks[week].append(task)

        ctx = {
            'roadmap': roadmap,
            'tasks': tasks,
            'weeks': weeks,
            'progress': progress,
        }
        return render(request, self.template_name, ctx)


@method_decorator(login_required, name='dispatch')
class MyRoadmapsView(View):
    template_name = 'roadmap/my_roadmaps.html'

    def get(self, request):
        roadmaps = request.user.roadmaps.all().order_by('-created_at')
        active = roadmaps.filter(status='active')
        completed = roadmaps.filter(status='completed')
        return render(request, self.template_name, {
            'roadmaps': roadmaps,
            'active': active,
            'completed': completed,
        })


@method_decorator(login_required, name='dispatch')
class DeleteRoadmapView(View):
    def post(self, request, pk):
        roadmap = get_object_or_404(Roadmap, pk=pk, user=request.user)
        roadmap.delete()
        messages.success(request, '🗑️ Roadmap deleted successfully.')
        return redirect('roadmap:my_roadmaps')
