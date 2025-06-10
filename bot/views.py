from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import UserProfile
from django.contrib import messages
from bot.scraper import run

from django.contrib.auth.models import User
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            zone = form.cleaned_data['zone']

            # Проверка уникальности email/username
            if User.objects.filter(username=email).exists():
                messages.error(request, "Такой email уже зарегистрирован.")
                return render(request, 'bot/register.html', {'form': form})

            user = User.objects.create(username=email)
            user.set_password(password)
            user.save()

            profile = UserProfile.objects.create(
                user=user,
                email=email,
                password=password,
                zone=zone,
                is_active=True,
                auto_booking_enabled=True
            )

            # Сохраняем user_id в сессии (автоматически)
            request.session['user_id'] = profile.id

            messages.success(request, "Регистрация успешна! Теперь вы авторизованы.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'bot/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            profile = UserProfile.objects.filter(email=email, password=password).first()
            if profile:
                request.session['user_id'] = profile.id
                return redirect('dashboard')
            else:
                messages.error(request, "Неверные данные")
    else:
        form = LoginForm()
    return render(request, 'bot/login.html', {'form': form})

def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    profile = UserProfile.objects.get(id=user_id)

    if request.method == 'POST':
        run(profile.email, profile.password, profile.zone)
        messages.success(request, "Бронирование выполнено (или попытка сделана).")
        return redirect('dashboard')  # ← ОБЯЗАТЕЛЬНО НУЖЕН ЭТОТ РЕДИРЕКТ!

    return render(request, 'bot/dashboard.html', {'profile': profile})