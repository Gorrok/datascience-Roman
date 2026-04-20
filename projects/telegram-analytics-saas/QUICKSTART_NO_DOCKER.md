# 🚀 Запуск без Docker (Локальная разработка)

Инструкция для запуска проекта на macOS без Docker.

## ✅ Что нужно установить

### 1. PostgreSQL

```bash
# Установка через Homebrew
brew install postgresql@15

# Запуск PostgreSQL
brew services start postgresql@15

# Создание базы данных
createdb telegram_analytics
```

### 2. Redis

```bash
# Установка через Homebrew
brew install redis

# Запуск Redis
brew services start redis
```

### 3. Python 3.11+

```bash
# Проверка версии
python3 --version

# Если нужно установить
brew install python@3.11
```

## 🔧 Настройка Backend

### 1. Перейдите в директорию backend

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

### 4. Настройте .env файл

Файл `.env` уже создан. Обновите подключения для локального запуска:

```bash
# Откройте файл
nano .env
```

Измените строки:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/telegram_analytics
DATABASE_URL_SYNC=postgresql://postgres:postgres@localhost:5432/telegram_analytics
REDIS_URL=redis://localhost:6379/0
```

Сохраните (Ctrl+O, Enter, Ctrl+X).

### 5. Примените миграции

```bash
alembic upgrade head
```

### 6. Запустите Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на http://localhost:8000

API документация: http://localhost:8000/docs

## 🔄 Запуск Celery Worker (отдельный терминал)

### 1. Откройте новое окно терминала

### 2. Активируйте виртуальное окружение

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
source venv/bin/activate
```

### 3. Запустите Celery Worker

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

## 📊 Flower (опционально, для мониторинга Celery)

В новом терминале:

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
source venv/bin/activate
celery -A app.tasks.celery_app flower --port=5555
```

Flower будет доступен на http://localhost:5555

## 🎨 Frontend (опционально)

### 1. Установите Node.js

```bash
# Через Homebrew
brew install node
```

### 2. Запустите Frontend

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/frontend
npm install
npm run dev
```

Frontend будет доступен на http://localhost:3000

## ✅ Проверка работоспособности

### 1. Проверьте Backend

Откройте в браузере: http://localhost:8000/health

Должен вернуться:
```json
{"status": "healthy"}
```

### 2. Проверьте API документацию

http://localhost:8000/docs

### 3. Тестовая регистрация

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }'
```

## 📝 Полезные команды

### Остановка сервисов

```bash
# Остановить PostgreSQL
brew services stop postgresql@15

# Остановить Redis
brew services stop redis
```

### Перезапуск сервисов

```bash
brew services restart postgresql@15
brew services restart redis
```

### Проверка статуса

```bash
brew services list
```

## 🐛 Устранение проблем

### PostgreSQL не подключается

```bash
# Проверьте статус
brew services list

# Перезапустите
brew services restart postgresql@15

# Проверьте подключение
psql -U postgres -d telegram_analytics
```

### Redis не работает

```bash
# Проверьте статус
redis-cli ping

# Должен вернуть: PONG
```

### Ошибки миграций

```bash
# Сбросьте БД
dropdb telegram_analytics
createdb telegram_analytics

# Примените миграции заново
alembic upgrade head
```

## 🚀 Быстрый запуск (все в одном скрипте)

Создайте файл `start.sh`:

```bash
#!/bin/bash

# Запуск сервисов
brew services start postgresql@15
brew services start redis

# Ждем запуска
sleep 3

# Переходим в backend
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend

# Активируем venv
source venv/bin/activate

# Запускаем backend в фоне
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Запускаем celery worker в фоне
celery -A app.tasks.celery_app worker --loglevel=info &

echo "✅ Backend запущен на http://localhost:8000"
echo "✅ API Docs: http://localhost:8000/docs"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Ждем
wait
```

Запуск:

```bash
chmod +x start.sh
./start.sh
```

## 📚 Следующие шаги

После успешного запуска:

1. ✅ Откройте http://localhost:8000/docs
2. ✅ Зарегистрируйте пользователя через Swagger UI
3. ✅ Добавьте Telegram бота
4. ✅ Начните мониторинг каналов

Полная документация: [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)

---

**Нужна помощь?** Смотрите основную документацию или создайте issue.
