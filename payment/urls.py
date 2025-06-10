from django.urls import path
from .views import stripe_checkout, paypal_checkout

urlpatterns = [
    path('stripe/', stripe_checkout, name='stripe_checkout'),
    path('paypal/', paypal_checkout, name='paypal_checkout'),
]
