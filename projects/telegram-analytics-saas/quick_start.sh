#!/bin/bash

echo "🚀 Запуск Telegram Analytics (SQLite версия)..."
echo ""

# Переходим в директорию backend
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/backend"

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.11+"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo ""

# Создание или активация venv
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Не удалось создать виртуальное окружение"
        exit 1
    fi
fi

# Активация venv
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Не удалось активировать виртуальное окружение"
    exit 1
fi

# Проверка requirements-sqlite.txt
if [ ! -f "requirements-sqlite.txt" ]; then
    echo "❌ Файл requirements-sqlite.txt не найден"
    exit 1
fi

# Установка/обновление зависимостей
echo ""
echo "📦 Установка зависимостей..."
echo "   (Это может занять несколько минут при первом запуске)"
echo ""

pip install --upgrade pip -q
pip install -r requirements-sqlite.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Некоторые пакеты не установились, но продолжаем..."
    echo ""
fi

# Создание .env если его нет
if [ ! -f ".env" ]; then
    echo "⚙️  Создание .env файла..."
    cat > .env << 'EOF'
DATABASE_URL=sqlite+aiosqlite:///./telegram_analytics.db
DATABASE_URL_SYNC=sqlite:///./telegram_analytics.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=development-secret-key-change-in-production-32chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
APP_NAME=Telegram Analytics
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
STRIPE_SECRET_KEY=sk_test_placeholder
STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
STRIPE_WEBHOOK_SECRET=whsec_placeholder
EOF
    echo "✅ .env файл создан"
fi

# Проверка установки alembic
if ! command -v alembic &> /dev/null; then
    echo "❌ alembic не установлен. Попытка установить..."
    pip install alembic
fi

# Создание базы данных
if [ ! -f "telegram_analytics.db" ]; then
    echo ""
    echo "🗄️  Создание базы данных..."
    alembic upgrade head
    if [ $? -ne 0 ]; then
        echo "⚠️  Ошибка при создании БД, но продолжаем..."
    else
        echo "✅ База данных создана"
    fi
else
    echo "✅ База данных уже существует"
fi

# Проверка установки uvicorn
if ! command -v uvicorn &> /dev/null; then
    echo "❌ uvicorn не установлен. Попытка установить..."
    pip install uvicorn[standard]
fi

# Запуск сервера
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Запуск сервера..."
echo ""
echo "📡 API:        http://localhost:8000"
echo "📚 Docs:       http://localhost:8000/docs"
echo "💚 Health:     http://localhost:8000/health"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Нажмите Ctrl+C для остановки"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
