"""Streak update logic shared by HTMX toggle and DRF API."""

from datetime import timedelta
from django.utils import timezone


def record_activity(profile, progress):
    """Update streak counters on profile + per-roadmap progress.

    Called when a task is freshly marked complete. Idempotent within a
    calendar day.
    """
    today = timezone.localdate()

    last_profile = profile.last_activity.date() if profile.last_activity else None
    if last_profile == today:
        pass
    elif last_profile == today - timedelta(days=1):
        profile.streak_days += 1
    else:
        profile.streak_days = 1
    profile.last_activity = timezone.now()
    profile.save(update_fields=['streak_days', 'last_activity'])

    last_progress = progress.last_activity_date
    if last_progress == today:
        pass
    elif last_progress == today - timedelta(days=1):
        progress.streak += 1
    else:
        progress.streak = 1
    if progress.streak > progress.max_streak:
        progress.max_streak = progress.streak
    progress.last_activity_date = today
    progress.save(update_fields=['streak', 'max_streak', 'last_activity_date', 'updated_at'])
