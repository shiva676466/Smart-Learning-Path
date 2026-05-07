from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('generate/', views.GenerateRoadmapView.as_view(), name='generate'),
    path('my-roadmaps/', views.MyRoadmapsView.as_view(), name='my_roadmaps'),
    path('<int:pk>/', views.RoadmapDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.DeleteRoadmapView.as_view(), name='delete'),
]
