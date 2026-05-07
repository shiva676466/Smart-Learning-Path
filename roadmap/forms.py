"""Roadmap generation form"""

from django import forms
from .models import Skill


class RoadmapGenerateForm(forms.Form):
    """Form to collect user preferences for roadmap generation"""

    LEVEL_CHOICES = [
        ('beginner', '🟢 Beginner — Starting from scratch'),
        ('intermediate', '🟡 Intermediate — Know the basics'),
        ('advanced', '🔴 Advanced — Want to master it'),
    ]

    DURATION_CHOICES = [
        (15, '15 Days — Sprint Mode'),
        (30, '30 Days — Standard'),
        (60, '60 Days — Deep Dive'),
        (90, '90 Days — Master Track'),
    ]

    HOURS_CHOICES = [
        (0.5, '30 min/day'),
        (1.0, '1 hour/day'),
        (1.5, '1.5 hours/day'),
        (2.0, '2 hours/day'),
        (3.0, '3 hours/day'),
        (4.0, '4+ hours/day'),
    ]

    skill = forms.ModelChoiceField(
        queryset=Skill.objects.filter(is_active=True),
        empty_label='— Select a Skill —',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'skillSelect'})
    )
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'skill-level-radio'})
    )
    daily_hours = forms.ChoiceField(
        choices=HOURS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    duration_days = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'duration-radio'})
    )
