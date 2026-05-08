from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from progress.models import Progress
from .models import Skill, Roadmap, RoadmapTask


class CompleteTaskAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cara', password='pass1234')
        self.skill = Skill.objects.create(
            name='Data Structures & Algorithms',
            slug='dsa',
            description='DSA track',
            category='cs_fundamentals',
        )
        self.roadmap = Roadmap.objects.create(
            user=self.user,
            skill=self.skill,
            title='DSA Beginner Path',
            level='beginner',
            daily_hours=1.0,
            duration_days=15,
        )
        self.task = RoadmapTask.objects.create(
            roadmap=self.roadmap,
            day_number=1,
            title='Arrays',
            description='Learn arrays',
            task_details='Solve five easy problems',
            difficulty=1,
            estimated_minutes=60,
            xp_reward=20,
        )
        self.client.force_login(self.user)

    def test_complete_task_api_keeps_progress_and_xp_consistent(self):
        url = reverse('api_complete_task', args=[self.task.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.roadmap.refresh_from_db()
        progress = Progress.objects.get(user=self.user, roadmap=self.roadmap)
        self.assertEqual(self.user.profile.total_xp, 120)
        self.assertEqual(self.roadmap.status, 'completed')
        self.assertEqual(progress.total_xp_earned, 20)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.roadmap.refresh_from_db()
        progress.refresh_from_db()
        self.assertEqual(self.user.profile.total_xp, 0)
        self.assertEqual(self.roadmap.status, 'active')
        self.assertEqual(progress.total_xp_earned, 0)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.total_xp, 120)
