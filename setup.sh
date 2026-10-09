#!/bin/bash

# Цветовые коды для вывода
GREEN='\033[0;32m'
NC='\033[0m' # No Color
RED='\033[0;31m'

echo -e "${GREEN}>>> Начинаю установку проекта...${NC}"

# 1. Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Ошибка: Python3 не установлен. Пожалуйста, установите его перед запуском скрипта.${NC}"
    echo "Пожалуйста, установите Python3 перед запуском скрипта:"
    echo "  - Ubuntu/Debian: sudo apt update && sudo apt install python3"
    echo "  - macOS: brew install python"
    echo "  - Windows: Скачайте установщик с python.org"
    exit 1
fi

# 2. Создание виртуального окружения
echo ">>> Создание виртуального окружения (venv)..."
python3 -m venv venv --without-pip
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Виртуальное окружение создано.${NC}"
else
    echo -e "${RED}Ошибка при создании venv.${NC}"
    exit 1
fi

# 3. Установка pip и зависимостей
echo ">>> Установка pip и зависимостей..."
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
./venv/bin/python3 get-pip.py
rm get-pip.py

./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Зависимости успешно установлены.${NC}"
else
    echo -e "${RED}Ошибка при установке зависимостей.${NC}"
    exit 1
fi

# 4. Проверка и установка PM2
echo ">>> Проверка PM2..."
if ! command -v pm2 &> /dev/null; then
    echo "PM2 не найден. Попытка установки..."
    if command -v npm &> /dev/null; then
        npm install -g pm2
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}PM2 успешно установлен.${NC}"
        else
            echo -e "${RED}Ошибка при установке PM2 через npm.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Ошибка: NPM не найден. Установите Node.js, чтобы использовать PM2.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}PM2 уже установлен.${NC}"
fi

# 5. Создание файла .env
if [ ! -f .env ]; then
    echo ">>> Создание файла .env..."
    cat <<EOF > .env
# Настройки проекта - ЗАПОЛНИТЕ ИХ:
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь
OPENAI_API_KEY=ваш_ключ_openai_здесь
DATABASE_URL=sqlite:///./tasks.db
EOF
    echo -e "${GREEN}Файл .env создан. Пожалуйста, откройте его и вставьте свои ключи.${NC}"
else
    echo "Файл .env уже существует. Оставьте его как есть."
fi

echo -e "${GREEN}>>> Установка завершена!${NC}"
echo "Чтобы запустить проект, выполните:"
echo "pm2 start_ecosystem ecosystem.config.js"
