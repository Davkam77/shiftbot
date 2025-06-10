# bot/referral.py

from bot.models import UserProfile

def apply_referral(ref_code, new_user):
    try:
        referrer = UserProfile.objects.get(referral_code=ref_code)
        referrer.bonus_count += 1
        referrer.save()
        print(f"[INFO] Пользователь {new_user.email} зарегистрировался по рефералке.")
    except UserProfile.DoesNotExist:
        print("[WARNING] Неверный реферальный код.")
