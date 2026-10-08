import os
import logging
import asyncio
import json
import base64
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from backend.database import SessionLocal, engine
from backend.models import User, Task, AuthCode
from openai import OpenAI

load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Инициализация БД
Base.metadata.create_all(bind=engine)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я помогу тебе фиксировать дела. Пришли мне номер телефона для входа.")

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    db = SessionLocal()
    
    # В простом примере генерируем 6-значный код
    import random
    code = str(random.randint(100000, 999999))
    
    new_code = AuthCode(
        phone=phone,
        code=code,
        expires_at=datetime.now().replace(hour=23, minute=59, second=59)
    )
    db.add(new_code)
    db.commit()
    
    await update.message.reply_text(f"Ваш код для входа: {code}")
    db.close()

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    file_path = f"storage/voice_{update.message.voice.file_id}.ogg"
    os.makedirs("storage", exist_ok=True)
    await file.download_to_drive(file_path)

    # Транскрипция через Whisper
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    text = transcript.text
    await update.message.reply_text(f"Услышал: '{text}'. Создаю задачу...")
    
    # Логика создания задачи (упрощенно)
    db = SessionLocal()
    new_task = Task(
        title=text[:30] + "..." if len(text) > 30 else text,
        description=text,
        due_date=datetime.now().replace(day=datetime.now().day + 1) # Завтра
    )
    db.add(new_task)
    db.commit()
    db.close()
    
    os.remove(file_path)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"storage/photo_{photo.file_id}.jpg"
    os.makedirs("storage", exist_ok=True)
    await file.download_to_drive(file_path)

    # Vision анализ
    with open(file_path, "rb") as image_file:
        content = base64.b64encode(image_file.read()).decode('utf-8')
        
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Распознай билет или мероприятие. Верни только JSON: {'title': '...', 'due_date': 'YYYY-MM-DD', 'description': '...'}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{content}"}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )
    
    data = json.loads(response.choices[0].message.content)
    
    # Парсинг даты из JSON
    try:
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    except:
        due_date = datetime.now().replace(day=datetime.now().day + 1)

    db = SessionLocal()
    new_task = Task(
        title=data['title'],
        description=data['description'],
        due_date=due_date
    )
    db.add(new_task)
    db.commit()
    db.close()

    await update.message.reply_text(f"Задача создана: {data['title']} на {data['due_date']}")
    os.remove(file_path)

def main():
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    application.run_polling()

if __name__ == "__main__":
    main()
