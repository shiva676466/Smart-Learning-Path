# ⚡ Smart Learning Path Generator — LearnPathAI

A production-quality Django web application that generates personalized, day-by-day learning roadmaps for tech skills.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate

# 3. Seed skills data
python manage.py seed_skills

# 4. Create superuser (admin panel)
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver
```

Then open: http://127.0.0.1:8000

**Admin Panel:** http://127.0.0.1:8000/admin/
Default admin: `admin` / `admin123`

---

## 📁 Project Structure

```
smart_learning_path/
├── smart_learning/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                   # Auth, profiles
│   ├── models.py            # UserProfile
│   ├── views.py             # Register, Login, Profile
│   ├── forms.py
│   └── urls.py
├── roadmap/                 # Core roadmap engine
│   ├── models.py            # Skill, Topic, Roadmap, RoadmapTask
│   ├── generator.py         # ⭐ Rule-based roadmap generation
│   ├── views.py
│   ├── serializers.py       # DRF serializers
│   ├── api_views.py         # REST API endpoints
│   ├── forms.py
│   ├── urls.py
│   ├── api_urls.py
│   └── management/commands/seed_skills.py
├── progress/                # XP, streaks, progress tracking
│   ├── models.py            # Progress, XPLog, AdaptiveSuggestion
│   ├── views.py
│   └── urls.py
├── dashboard/               # Home & dashboard views
│   ├── views.py
│   ├── urls.py
│   └── templatetags/
├── templates/               # All HTML templates
│   ├── base.html            # Navigation, footer, messages
│   ├── dashboard/
│   ├── users/
│   ├── roadmap/
│   └── progress/
└── static/
    ├── css/main.css         # Full dark theme stylesheet
    └── js/main.js           # Interactive JS
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗺️ Roadmap Generator | Rule-based day-wise plans for 5 skills × 3 levels |
| 📊 Dashboard | Active roadmaps, XP, streak, progress bars |
| ✅ Task Tracking | Mark complete via REST API, real-time progress |
| ⚡ XP System | Earn XP per task, level up, view XP log |
| 🏆 Leaderboard | All users ranked by XP |
| 👤 User Profiles | Avatar, bio, stats, XP history |
| 🔐 Auth | Register, Login, Logout with Django auth |
| 🛠 Admin Panel | Full Django admin for all models |
| 📱 Responsive | Mobile-first, works on all devices |
| 🌙 Dark Theme | Professional dark UI |

---

## 🔌 REST API Endpoints

```
GET  /api/skills/                    # List all skills
GET  /api/roadmaps/                  # User's roadmaps
GET  /api/roadmaps/<id>/             # Roadmap detail with tasks
POST /api/tasks/<id>/complete/       # Toggle task completion
```

---

## 🧠 Roadmap Generation Logic

The generator in `roadmap/generator.py` works as follows:

```
User selects: Skill + Level + Daily Hours + Duration Days
    ↓
Load curated topic list for (Skill, Level)
    ↓
Calculate topics_per_day = max(1, round(daily_hours / 1.5))
    ↓
Scale/compress topic list to fit duration
    ↓
Create RoadmapTask for each day with:
  - Title, description, task details
  - Resource URL & title
  - Difficulty (1-5), estimated minutes
  - XP reward (scaled by workload factor)
```

---

## 🗃️ Database Models

- **UserProfile** — extends User with XP, streak, level, avatar
- **Skill** — 5 learnable skills with icon, color, category
- **Topic** — specific topic within a skill/level
- **Resource** — learning resource linked to a topic
- **Roadmap** — user's generated plan with metadata
- **RoadmapTask** — individual day task with completion tracking
- **Progress** — per-roadmap progress record
- **XPLog** — log of all XP-earning events
- **AdaptiveSuggestion** — system suggestions for missed tasks

---

## 🔧 Production Deployment

1. Set `DEBUG = False` in settings.py
2. Set a strong `SECRET_KEY`
3. Configure PostgreSQL (see commented section in settings.py)
4. Run `python manage.py collectstatic`
5. Deploy with Gunicorn + Nginx

---

## 👤 Default Credentials

| Role | Username | Password |
|---|---|---|
| Admin | admin | admin123 |

**Change these immediately in production!**
