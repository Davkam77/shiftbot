from django.shortcuts import render, redirect
from django.contrib import messages
from bot.models import UserProfile

def stripe_checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Здесь должна быть интеграция с реальным Stripe API
    profile = UserProfile.objects.get(id=user_id)
    profile.is_active = True
    profile.save()
    messages.success(request, "Платёж через Stripe прошёл успешно!")
    return redirect('dashboard')

def paypal_checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Здесь должна быть интеграция с реальным PayPal SDK
    profile = UserProfile.objects.get(id=user_id)
    profile.is_active = True
    profile.save()
    messages.success(request, "Платёж через PayPal прошёл успешно!")
    return redirect('dashboard')
