#!/bin/bash

# 🔥 Автоматический деплой на Beget - ПОЛНЫЙ ГААААЗ! 🚀

set -e

echo "🚀 Начинаем деплой на Beget..."

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Конфигурация (замените на свои данные)
SERVER_USER="${BEGET_USER:-username}"
SERVER_HOST="${BEGET_HOST:-yourserver.beget.tech}"
DEPLOY_PATH="${BEGET_PATH:-~/telegram-analytics}"

echo -e "${BLUE}📦 Шаг 1: Подготовка файлов...${NC}"

# Создаём временную папку для деплоя
DEPLOY_TMP="deploy_tmp"
rm -rf $DEPLOY_TMP
mkdir -p $DEPLOY_TMP

# Копируем backend
echo "Копируем backend..."
cp -r backend $DEPLOY_TMP/
rm -rf $DEPLOY_TMP/backend/__pycache__
rm -rf $DEPLOY_TMP/backend/**/__pycache__
rm -rf $DEPLOY_TMP/backend/venv
rm -rf $DEPLOY_TMP/backend/*.db
rm -f $DEPLOY_TMP/backend/.env

# Копируем frontend
echo "Копируем frontend..."
cp -r frontend $DEPLOY_TMP/
rm -rf $DEPLOY_TMP/frontend/node_modules
rm -rf $DEPLOY_TMP/frontend/.next

# Создаём архив
echo -e "${BLUE}📦 Шаг 2: Создание архива...${NC}"
tar -czf telegram-analytics-deploy.tar.gz -C $DEPLOY_TMP .
rm -rf $DEPLOY_TMP

echo -e "${GREEN}✅ Архив создан: telegram-analytics-deploy.tar.gz${NC}"
echo -e "${BLUE}📤 Шаг 3: Загрузка на сервер...${NC}"

# Загружаем на сервер
scp telegram-analytics-deploy.tar.gz $SERVER_USER@$SERVER_HOST:~/

echo -e "${BLUE}🔧 Шаг 4: Настройка на сервере...${NC}"

# Выполняем команды на сервере
ssh $SERVER_USER@$SERVER_HOST << 'ENDSSH'
set -e

echo "🔥 Распаковка архива..."
mkdir -p ~/telegram-analytics
cd ~/telegram-analytics
tar -xzf ~/telegram-analytics-deploy.tar.gz
rm ~/telegram-analytics-deploy.tar.gz

echo "🐍 Настройка Backend..."
cd backend

# Создаём venv если его нет
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements-sqlite.txt
pip install gunicorn

# Создаём .env если его нет
if [ ! -f ".env" ]; then
    echo "⚙️ Создаём .env файл..."
    cat > .env << 'EOF'
DATABASE_URL=sqlite+aiosqlite:///./telegram_analytics.db
DATABASE_URL_SYNC=sqlite:///./telegram_analytics.db
SECRET_KEY=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -base64 32 | head -c 32)
CORS_ORIGINS=["http://localhost:3000"]
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
EOF
fi

# Запускаем миграции
alembic upgrade head

echo "📦 Настройка Frontend..."
cd ../frontend

# Устанавливаем зависимости
if [ ! -d "node_modules" ]; then
    npm install
fi

# Создаём .env.production если его нет
if [ ! -f ".env.production" ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.production
fi

# Собираем production build
npm run build

echo "✅ Деплой завершён!"
echo "🚀 Для запуска выполните:"
echo "   Backend: cd ~/telegram-analytics/backend && source venv/bin/activate && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
echo "   Frontend: cd ~/telegram-analytics/frontend && npm start"

ENDSSH

echo -e "${GREEN}✅ Деплой завершён успешно!${NC}"
echo -e "${BLUE}📝 Следующие шаги:${NC}"
echo "1. Подключитесь к серверу: ssh $SERVER_USER@$SERVER_HOST"
echo "2. Настройте .env файлы (домен, секретные ключи)"
echo "3. Запустите backend и frontend"
echo "4. Настройте nginx/supervisor для автозапуска"
echo ""
echo -e "${GREEN}🎉 Готово! ПОЛНЫЙ ГААААЗ!${NC}"
