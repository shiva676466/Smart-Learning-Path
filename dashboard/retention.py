"""Compute lightweight retention + engagement stats.

Activity signal = XPLog entries. Every task completion creates one, so
this is the most reliable "did the user actually do something" signal
we have.
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from progress.models import XPLog


def _active_user_ids_between(start, end):
    return set(
        XPLog.objects
        .filter(earned_at__gte=start, earned_at__lt=end)
        .values_list('user_id', flat=True)
        .distinct()
    )


def compute_retention():
    now = timezone.now()
    today = timezone.localdate()
    day = timedelta(days=1)

    dau = len(_active_user_ids_between(now - day, now))
    wau = len(_active_user_ids_between(now - 7 * day, now))
    mau = len(_active_user_ids_between(now - 30 * day, now))

    # Daily active series, last 30 days (oldest -> newest).
    daily_series = []
    for i in range(29, -1, -1):
        start = timezone.make_aware(
            timezone.datetime.combine(today - i * day, timezone.datetime.min.time())
        )
        end = start + day
        daily_series.append({
            'date': (today - i * day).isoformat(),
            'count': len(_active_user_ids_between(start, end)),
        })

    # Signups
    total_users = User.objects.count()
    signups_last_7 = User.objects.filter(date_joined__gte=now - 7 * day).count()
    signups_last_30 = User.objects.filter(date_joined__gte=now - 30 * day).count()

    # Rolling cohort retention. Of users who joined between [N+window, N]
    # days ago, what % had any XPLog entry at or after their signup+N day?
    def rolling_retention_py(day_n: int, window_days: int = 30) -> dict:
        cohort_end = now - day_n * day
        cohort_start = cohort_end - window_days * day
        users = User.objects.filter(
            date_joined__gte=cohort_start, date_joined__lt=cohort_end,
        ).values_list('id', 'date_joined')
        users = list(users)
        if not users:
            return {'cohort_size': 0, 'retained': 0, 'pct': 0.0}
        # Pull XPLog earned_at per user for those users only.
        logs = XPLog.objects.filter(user_id__in=[u[0] for u in users]) \
            .values_list('user_id', 'earned_at')
        by_user = {}
        for uid, ts in logs:
            by_user.setdefault(uid, []).append(ts)
        retained = 0
        for uid, joined in users:
            cutoff = joined + day_n * day
            if any(t >= cutoff for t in by_user.get(uid, [])):
                retained += 1
        pct = round((retained / len(users)) * 100, 1)
        return {'cohort_size': len(users), 'retained': retained, 'pct': pct}

    d1 = rolling_retention_py(1)
    d7 = rolling_retention_py(7)
    d30 = rolling_retention_py(30)

    return {
        'dau': dau, 'wau': wau, 'mau': mau,
        'total_users': total_users,
        'signups_last_7': signups_last_7,
        'signups_last_30': signups_last_30,
        'daily_series': daily_series,
        'retention': {'d1': d1, 'd7': d7, 'd30': d30},
        'generated_at': now,
    }
