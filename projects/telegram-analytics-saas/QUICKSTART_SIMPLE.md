# ⚡ Самый простой запуск (SQLite, без Redis)

Для быстрого тестирования API без установки PostgreSQL и Redis.

## 🎯 Что это даёт

- ✅ Быстрый запуск за 2 минуты
- ✅ Работает API и все эндпоинты
- ✅ SQLite вместо PostgreSQL (не нужна установка)
- ⚠️ Без Celery/Redis (боты не будут работать в фоне)

## 🚀 Быстрый старт

### 1. Откройте терминал и перейдите в папку проекта

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
```

### 2. Создайте виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Создайте упрощенный .env файл

```bash
cat > .env << 'EOF'
# SQLite Database (локальный файл)
DATABASE_URL=sqlite+aiosqlite:///./telegram_analytics.db
DATABASE_URL_SYNC=sqlite:///./telegram_analytics.db

# Redis (не обязательно для тестирования)
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=development-secret-key-change-in-production-32chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# App
APP_NAME=Telegram Analytics
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development

# Stripe (пока не обязательно)
STRIPE_SECRET_KEY=sk_test_placeholder
STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
STRIPE_WEBHOOK_SECRET=whsec_placeholder
EOF
```

### 5. Установите дополнительно aiosqlite

```bash
pip install aiosqlite
```

### 6. Примените миграции

```bash
alembic upgrade head
```

### 7. Запустите backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Проверка

Откройте в браузере:

- **API Health**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs ← Здесь можно тестировать все API!

## 📝 Тестирование через Swagger UI

1. Откройте http://localhost:8000/docs
2. Найдите раздел **auth**
3. Раскройте **POST /api/v1/auth/register**
4. Нажмите **Try it out**
5. Введите данные:

```json
{
  "email": "test@example.com",
  "password": "testpassword123",
  "full_name": "Test User"
}
```

6. Нажмите **Execute**
7. Вы создали пользователя! 🎉

### Вход в систему

1. Найдите **POST /api/v1/auth/login**
2. **Try it out**
3. Введите:
   - username: `test@example.com`
   - password: `testpassword123`
4. **Execute**
5. Скопируйте `access_token` из ответа

### Использование токена

1. Вверху страницы нажмите **Authorize** 🔓
2. Введите: `Bearer ВАШ_ACCESS_TOKEN`
3. **Authorize**
4. Теперь можете вызывать защищенные эндпоинты!

## 🤖 Добавление бота

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Скопируйте токен
3. В Swagger UI найдите **POST /api/v1/bots**
4. **Try it out**, введите:

```json
{
  "bot_token": "ВАШ_ТОКЕН_ОТ_BOTFATHER"
}
```

5. **Execute**

## ⚠️ Ограничения SQLite версии

- ✅ API работает полностью
- ✅ Регистрация, вход, управление ботами
- ✅ Аналитика (когда будут данные)
- ⚠️ Celery workers не работают (нужен Redis)
- ⚠️ Боты не мониторят каналы автоматически

## 🔄 Переход на полную версию

Когда захотите полный функционал:

1. Установите PostgreSQL и Redis (см. QUICKSTART_NO_DOCKER.md)
2. Или установите Docker (см. QUICKSTART.md)

## 📊 Просмотр базы данных

```bash
# Установите sqlite3 браузер
brew install sqlite3

# Откройте БД
sqlite3 telegram_analytics.db

# Посмотрите таблицы
.tables

# Посмотрите пользователей
SELECT * FROM users;

# Выход
.quit
```

## 🛑 Остановка

Нажмите `Ctrl+C` в терминале где запущен uvicorn.

## 📝 Автоматический скрипт запуска

Создайте файл `quick_start.sh`:

```bash
#!/bin/bash

echo "🚀 Запуск Telegram Analytics (SQLite версия)..."

cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend

# Активация venv
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install aiosqlite
else
    source venv/bin/activate
fi

# Проверка .env
if [ ! -f ".env" ]; then
    echo "⚙️ Создание .env файла..."
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
fi

# Миграции
if [ ! -f "telegram_analytics.db" ]; then
    echo "🗄️ Создание базы данных..."
    alembic upgrade head
fi

# Запуск
echo ""
echo "✅ Запуск сервера..."
echo "📡 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
echo "Нажмите Ctrl+C для остановки"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Использование:

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
chmod +x quick_start.sh
./quick_start.sh
```

---

**Готово!** Теперь у вас работающий API на http://localhost:8000/docs 🎉
