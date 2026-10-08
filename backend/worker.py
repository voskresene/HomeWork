import logging
import os
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend.models import Task, User
from dotenv import load_dotenv
from apscheduler.schedulers.background_jobs import BackgroundJobManager
from apscheduler.schedulers.block import BlockingScheduler

load_dotenv()

# Для отправки сообщений будем использовать простой запрос к Telegram API
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_tg_notification(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def check_reminders():
    db = SessionLocal()
    # Ищем задачи, до которых осталось 1 час или меньше
    now = datetime.now()
    upcoming = db.query(Task).filter(
        Task.due_date <= (now + timedelta(hours=1)),
        Task.is_completed == False
    ).all()
    
    for task in upcoming:
        # В реальности нужно матчить ID пользователя и его chat_id
        # Для теста отправим в общую группу или сконфигурированный chat_id
        print(f"Напоминание: {task.title}")
        # send_tg_notification(12345678, f"🔔 Напоминание: {task.title}")
    
    db.close()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(check_reminders, 'interval', minutes=1)
    print("Worker запущен...")
    scheduler.start()
