#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Запуск Couples Planner Bot${NC}\n"

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env файл не найден!${NC}"
    echo "Скопируйте .env.example в .env и заполните переменные:"
    echo "cp .env.example .env"
    exit 1
fi

echo -e "${GREEN}✅ .env файл найден${NC}\n"

# Функция для запуска в новом окне терминала (macOS)
run_in_new_terminal() {
    local title=$1
    local command=$2
    
    osascript <<EOF
tell application "Terminal"
    do script "cd $(pwd) && echo '${title}' && ${command}"
    set custom title of front window to "${title}"
end tell
EOF
}

# Запуск Backend
echo -e "${BLUE}📦 Запуск Backend...${NC}"
run_in_new_terminal "Backend API" "cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
sleep 2

# Запуск Bot
echo -e "${BLUE}🤖 Запуск Telegram Bot...${NC}"
run_in_new_terminal "Telegram Bot" "cd bot && source venv/bin/activate && python bot.py"
sleep 2

# Запуск Mini App
echo -e "${BLUE}💻 Запуск Mini App...${NC}"
run_in_new_terminal "Mini App" "cd mini-app && npm run dev"
sleep 2

echo ""
echo -e "${GREEN}✅ Все компоненты запущены!${NC}"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Mini App: http://localhost:5173"
echo ""
echo "🤖 Откройте вашего бота в Telegram и отправьте /start"
echo ""
echo -e "${BLUE}Для остановки закройте все окна терминала или нажмите Ctrl+C в каждом${NC}"
