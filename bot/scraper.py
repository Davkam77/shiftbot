# bot/scraper.py

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Настройка логгера
logger = logging.getLogger('shiftbot')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/bot.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

LOGIN_URL = "https://example.com/login"
DASHBOARD_URL = "https://example.com/dashboard"

def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)

def login(driver, email, password):
    logger.info(f"Попытка входа как {email}")
    try:
        driver.get(LOGIN_URL)
        time.sleep(2)

        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        if DASHBOARD_URL not in driver.current_url:
            raise Exception("Невозможно войти — проверьте email/пароль")
        logger.info("Успешный вход.")
        return True
    except Exception as e:
        logger.error(f"Ошибка входа: {e}")
        return False

def book_shift(driver, zone="Zone 1"):
    logger.info(f"Поиск смены для зоны: {zone}")
    try:
        driver.get(DASHBOARD_URL)
        time.sleep(2)

        shift_button = driver.find_element(By.XPATH, f"//button[contains(text(), '{zone}')]")
        shift_button.click()
        time.sleep(1)

        confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
        confirm.click()
        logger.info(f"Смена успешно забронирована в зоне {zone}")
        return True
    except NoSuchElementException:
        logger.warning("Смен нет или кнопка не найдена.")
        return False

def run(email, password, zone="Zone 1"):
    driver = start_browser()
    try:
        if login(driver, email, password):
            book_shift(driver, zone)
    finally:
        driver.quit()
