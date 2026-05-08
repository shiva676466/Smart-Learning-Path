from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from roadmap.models import Skill, Roadmap, RoadmapTask
from .models import Progress


class ToggleTaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pass1234')
        self.skill = Skill.objects.create(
            name='Python Programming',
            slug='python-programming',
            description='Python basics and beyond',
            category='programming',
        )
        self.roadmap = Roadmap.objects.create(
            user=self.user,
            skill=self.skill,
            title='Python Beginner Path',
            level='beginner',
            daily_hours=1.0,
            duration_days=15,
        )
        self.task = RoadmapTask.objects.create(
            roadmap=self.roadmap,
            day_number=1,
            title='Intro',
            description='Start here',
            task_details='Complete intro exercises',
            difficulty=1,
            estimated_minutes=60,
            xp_reward=20,
        )
        self.client.force_login(self.user)

    def test_toggle_task_does_not_allow_xp_farming(self):
        toggle_url = reverse('progress:toggle_task', args=[self.task.id])

        self.client.post(toggle_url)
        self.user.profile.refresh_from_db()
        self.roadmap.refresh_from_db()
        progress = Progress.objects.get(user=self.user, roadmap=self.roadmap)
        self.assertEqual(self.user.profile.total_xp, 120)
        self.assertEqual(self.roadmap.status, 'completed')
        self.assertEqual(progress.total_xp_earned, 20)

        self.client.post(toggle_url)
        self.user.profile.refresh_from_db()
        self.roadmap.refresh_from_db()
        self.task.refresh_from_db()
        progress.refresh_from_db()
        self.assertEqual(self.user.profile.total_xp, 0)
        self.assertEqual(self.roadmap.status, 'active')
        self.assertFalse(self.task.is_completed)
        self.assertEqual(progress.total_xp_earned, 0)

        self.client.post(toggle_url)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.total_xp, 120)
