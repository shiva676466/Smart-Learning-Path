"""Management command to seed initial skills. Run: python manage.py seed_skills"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from roadmap.models import Skill

class Command(BaseCommand):
    help = 'Seed initial skills data'

    def handle(self, *args, **options):
        skills_data = [
            {'name': 'Data Structures & Algorithms', 'description': 'Master arrays, linked lists, trees, graphs, sorting, searching, and dynamic programming.', 'category': 'cs_fundamentals', 'icon': '🧠', 'color': '#f59e0b'},
            {'name': 'Python Programming', 'description': 'Learn Python from scratch to advanced OOP, decorators, generators, and real-world projects.', 'category': 'programming', 'icon': '🐍', 'color': '#8b5cf6'},
            {'name': 'Web Development', 'description': 'Build modern full-stack apps with HTML, CSS, JavaScript, React, Node.js, and databases.', 'category': 'web_development', 'icon': '🌐', 'color': '#3b82f6'},
            {'name': 'Artificial Intelligence / Machine Learning', 'description': 'From NumPy/Pandas to deep learning with TensorFlow and Keras.', 'category': 'data_science', 'icon': '🤖', 'color': '#10b981'},
            {'name': 'Competitive Programming', 'description': 'Train for Codeforces, ICPC, LeetCode contests with advanced algorithms.', 'category': 'competitive', 'icon': '🏆', 'color': '#ef4444'},
            {'name': 'Blockchain & Web3', 'description': 'Master blockchain technology, smart contracts, Solidity, DeFi protocols, and decentralized applications.', 'category': 'blockchain', 'icon': '⛓️', 'color': '#f97316'},
            {'name': 'Ethical Hacking & Security', 'description': 'Learn penetration testing, vulnerability assessment, network security, and cybersecurity defense strategies.', 'category': 'ethical_hacking', 'icon': '🔐', 'color': '#dc2626'},
        ]
        created = 0 
        for data in skills_data:
            skill, flag = Skill.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'slug': slugify(data['name']), 'is_active': True}
            )
            if flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {skill.name}'))
        self.stdout.write(self.style.SUCCESS(f'Done! {created} skills created.'))
