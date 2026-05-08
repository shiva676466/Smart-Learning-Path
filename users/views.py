"""Users app views — registration, login, logout, profile"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import UserProfile
from progress.models import XPLog


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Welcome {user.first_name}! Your learning journey begins now.')
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'👋 Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'You have been logged out. See you soon! 👋')
        return redirect('dashboard:home')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        profile = request.user.profile
        xp_history = XPLog.objects.filter(user=request.user).order_by('-earned_at')[:10]
        roadmaps = request.user.roadmaps.all().order_by('-created_at')[:5]
        form = ProfileUpdateForm(instance=profile)
        ctx = {
            'profile': profile,
            'xp_history': xp_history,
            'roadmaps': roadmaps,
            'form': form,
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update User model fields
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()
            form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('users:profile')
        return render(request, self.template_name, {'form': form, 'profile': profile})
