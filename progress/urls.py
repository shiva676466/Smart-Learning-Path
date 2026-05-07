from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('task/<int:task_id>/toggle/', views.ToggleTaskView.as_view(), name='toggle_task'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
]
