from django.urls import path
from . import api_views

urlpatterns = [
    path('roadmaps/', api_views.RoadmapListAPI.as_view(), name='api_roadmaps'),
    path('roadmaps/<int:pk>/', api_views.RoadmapDetailAPI.as_view(), name='api_roadmap_detail'),
    path('tasks/<int:pk>/complete/', api_views.CompleteTaskAPI.as_view(), name='api_complete_task'),
    path('skills/', api_views.SkillListAPI.as_view(), name='api_skills'),
]
