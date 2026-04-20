# 🔧 Ручной запуск (если quick_start.sh не работает)

Если автоматический скрипт не работает, выполните команды вручную:

## Шаг 1: Переход в директорию backend

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
```

## Шаг 2: Создание виртуального окружения

```bash
python3 -m venv venv
```

## Шаг 3: Активация виртуального окружения

```bash
source venv/bin/activate
```

Вы увидите `(venv)` в начале строки терминала.

## Шаг 4: Обновление pip

```bash
pip install --upgrade pip
```

## Шаг 5: Установка зависимостей для SQLite

```bash
pip install -r requirements-sqlite.txt
```

⏳ Это займет 2-3 минуты. Подождите до конца.

## Шаг 6: Создание .env файла

```bash
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
```

## Шаг 7: Создание базы данных

```bash
alembic upgrade head
```

## Шаг 8: Запуск сервера

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Готово! Откройте: http://localhost:8000/docs

## 🛑 Остановка

Нажмите `Ctrl+C` в терминале.

## 🔄 Повторный запуск

Для повторного запуска:

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ⚠️ Если что-то не работает

### Ошибка: "command not found: alembic"

```bash
pip install alembic
```

### Ошибка: "command not found: uvicorn"

```bash
pip install uvicorn[standard]
```

### Ошибка: "Module not found"

```bash
pip install -r requirements-sqlite.txt --force-reinstall
```

### Полный сброс и переустановка

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
rm -rf venv
rm -f telegram_analytics.db
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-sqlite.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 Проверка успешного запуска

1. В терминале должно появиться:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

2. Откройте в браузере: http://localhost:8000/health

Должен вернуться:
```json
{"status": "healthy"}
```

3. Откройте: http://localhost:8000/docs

Вы увидите Swagger UI! 🎉

---

**Всё работает?** Переходите к [START_HERE.md](START_HERE.md#-что-делать-дальше) для следующих шагов!
