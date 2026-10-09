# Task Manager TG 🚀
Система для фиксации дел с авторизацией через Telegram, поддержкой голосовых сообщений, фотографий (билетов/событий) и адаптивным веб-интерфейсом.

## ⚡ Быстрая установка (Quick Start)

Вы можете развернуть проект одной командой (замените `<your-repo-url>` на реальную ссылку на ваш репозиторий):

```bash
git clone <your-repo-url> && cd task_manager_tg && chmod +x setup.sh && ./setup.sh
```

---

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

### 1. Быстрая установка
Используйте автоматический скрипт для настройки окружения:
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Конфигурация
Откройте созданный файл `.env` в корне проекта и вставьте свои ключи:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
OPENAI_API_KEY=ваш_ключ_openai
DATABASE_URL=sqlite:///./tasks.db
```

### 3. Развертывание (Production)

#### Вариант А: PM2 (Рекомендуется)
Самый простой способ запустить все сервисы одновременно с автоперезагрузкой (требуется установленный Node.js и PM2):
```bash
# Установка PM2 если нет
npm install -g pm2

# Запуск проекта
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

#### Вариант Б: Systemd (Системные службы)
Если вы хотите использовать стандартные службы Linux:
```bash
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now backend bot worker
```

### 4. Запуск приложения (Development)
Если вы запускаете локально без PM2, откройте три терминала:
```bash
# Терминал 1: Backend
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Терминал 2: Bot
source venv/bin/activate
python bot_logic/bot.py

# Терминал 3: Worker
source venv/bin/activate
python backend/worker.py
```

**Веб-интерфейс** будет доступен по адресу `http://<ваш_ip>:8000`.

## Технологический стек
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Bot:** python-telegram-bot
- **AI:** OpenAI (Whisper, GPT-4o)
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Scheduler:** APScheduler
