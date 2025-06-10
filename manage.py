#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Is it installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc

    # Запускаем фоновый grabber (если доступен)
    try:
        from bot.runs_process import start_background_grabber
        start_background_grabber()
    except Exception as e:
        print(f"[WARNING] Не удалось запустить grabber: {e}")

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
