# Task Manager TG 🚀
Система для фиксации дел с авторизацией через Telegram, поддержкой голосовых сообщений, фотографий (билетов/событий) и адаптивным веб-интерфейсом.

## Особенности
- **Авторизация:** Безопасный вход через получение кода в Telegram.
- **Мультимодальность:** Создание задач через текст, голос (Whisper) или фото (GPT-4o Vision).
- **Уведомления:** Автоматические напоминания в Telegram при приближении дедлайна.
- **Адаптивность:** Веб-интерфейс, оптимизированный под мобильные устройства и десктоп.

## Структура проекта
- `backend/`: FastAPI API, модели БД, воркер напоминаний.
- `bot_logic/`: Telegram бот для взаимодействия и обработки медиа.
- `frontend/`: Адаптивный веб-интерфейс.
- `storage/`: Локальное хранилище для временных файлов.

## Пререквизиты
- Python 3.10+
- Telegram Bot Token
- OpenAI API Key

## Установка и запуск

### 1. Клонирование и настройка
```bash
git clone <your-repo-url>
cd task_manager_tg
python3 -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

### 2. Конфигурация
Создайте файл `.env` в корне проекта:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
OPENAI_API_KEY=ваш_ключ_openai
DATABASE_URL=sqlite:///./tasks.db
```

### 3. Запуск приложения
Проект требует запуска четырех компонентов одновременно:

**А. Запуск Backend API:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Б. Запуск Telegram бота:**
```bash
python bot_logic/bot.py
```

**В. Запуск воркера уведомлений:**
```bash
python backend/worker.py
```

**Г. Веб-интерфейс:**
Просто откройте файл `frontend/index.html` в браузере или запустите локальный сервер:
```bash
python3 -m http.server 8000 --directory frontend
```

## Технологический стек
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Bot:** python-telegram-bot
- **AI:** OpenAI (Whisper, GPT-4o)
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Scheduler:** APScheduler
