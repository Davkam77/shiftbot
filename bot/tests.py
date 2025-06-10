from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import UserProfile

class BookingTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        self.profile = UserProfile.objects.create(
            user=user,
            email='test@example.com',
            password='pass123',
            zone='Zone 1',
            is_active=True,
            auto_booking_enabled=True
        )
        self.client = Client()

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'pass123'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        })
        self.assertContains(response, "Неверные данные")

    @patch('bot.views.run')  # ← ВАЖНО!
    def test_booking_triggered(self, mock_scraper):
        self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'pass123'
        })
        response = self.client.post(reverse('dashboard'))
        self.assertRedirects(response, reverse('dashboard'))
        mock_scraper.assert_called_once_with('test@example.com', 'pass123', 'Zone 1')
