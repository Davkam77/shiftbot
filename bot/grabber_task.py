# bot/grabber_task.py

import time
import logging
from django.conf import settings
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

from bot.models import UserProfile  # предполагаем, что логин и зона хранятся тут
from bot.scraper import run

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/bot.log', level=logging.INFO)

def grab_all_shifts():
    logger.info("Запуск задачи автоматического бронирования")
    users = UserProfile.objects.filter(is_active=True, auto_booking_enabled=True)

    for user in users:
        logger.info(f"Проверка для пользователя: {user.email} | Зона: {user.zone}")
        try:
            run(user.email, user.password, user.zone)
        except Exception as e:
            logger.error(f"Ошибка при бронировании для {user.email}: {e}")

def start_loop(interval_minutes=10):
    while True:
        grab_all_shifts()
        logger.info(f"Ожидание {interval_minutes} минут до следующей итерации...\n")
        time.sleep(interval_minutes * 60)
