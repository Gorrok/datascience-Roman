#!/bin/bash
# Скрипт запуска бота на Beget

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Запуск Invite Bot ===${NC}"

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Виртуальное окружение не найдено. Создаю...${NC}"
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Проверка зависимостей
echo -e "${YELLOW}Проверка зависимостей...${NC}"
pip install -r requirements.txt --quiet

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${RED}ОШИБКА: Файл .env не найден!${NC}"
    echo -e "${YELLOW}Скопируйте env.example в .env и заполните настройки${NC}"
    exit 1
fi

# Проверка credentials.json
if [ ! -f "credentials.json" ]; then
    echo -e "${RED}ОШИБКА: Файл credentials.json не найден!${NC}"
    echo -e "${YELLOW}Загрузите файл credentials.json для Google Sheets API${NC}"
    exit 1
fi

# Создание директории для логов
mkdir -p logs

# Проверка, не запущен ли уже бот
if [ -f "bot.pid" ]; then
    PID=$(cat bot.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Бот уже запущен (PID: $PID)${NC}"
        echo -e "${YELLOW}Используйте ./stop_bot.sh для остановки${NC}"
        exit 1
    else
        rm bot.pid
    fi
fi

# Запуск бота в фоновом режиме
echo -e "${GREEN}Запуск бота...${NC}"
nohup python3 invite_bot.py > logs/bot_output.log 2>&1 &
BOT_PID=$!

# Сохранение PID
echo $BOT_PID > bot.pid

# Проверка запуска
sleep 2
if ps -p $BOT_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Бот успешно запущен (PID: $BOT_PID)${NC}"
    echo -e "${YELLOW}Логи: tail -f logs/bot_output.log${NC}"
    echo -e "${YELLOW}Остановка: ./stop_bot.sh${NC}"
else
    echo -e "${RED}✗ Ошибка запуска бота${NC}"
    echo -e "${YELLOW}Проверьте логи: cat logs/bot_output.log${NC}"
    rm bot.pid
    exit 1
fi
