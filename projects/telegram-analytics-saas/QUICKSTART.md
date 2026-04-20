# 🚀 Быстрый старт Telegram Analytics SaaS

Пошаговая инструкция для запуска проекта на вашем компьютере.

## Предварительные требования

- ✅ **Docker Desktop** установлен и запущен
- ✅ **Git** установлен

## Шаг 1: Подготовка файла конфигурации

`.env` файл уже создан в `backend/` директории. Для базового запуска он готов к использованию.

### ⚠️ Важно для production:

Измените `SECRET_KEY` в `backend/.env`:
```bash
SECRET_KEY=ваш-очень-сложный-секретный-ключ-минимум-32-символа
```

Для генерации безопасного ключа можно использовать:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Шаг 2: Запуск проекта

### Вариант 1: Полный запуск (рекомендуется)

```bash
cd telegram-analytics-saas
docker-compose up -d
```

Это запустит:
- ✅ PostgreSQL (база данных)
- ✅ Redis (кэш и очереди)
- ✅ Backend API (FastAPI)
- ✅ Celery Worker (обработка ботов)
- ✅ Flower (мониторинг Celery)

### Вариант 2: Запуск только backend (без frontend)

```bash
cd telegram-analytics-saas
docker-compose up -d db redis backend celery_worker flower
```

## Шаг 3: Инициализация базы данных

После запуска контейнеров, примените миграции:

```bash
docker-compose exec backend alembic upgrade head
```

## Шаг 4: Проверка работоспособности

### Проверьте статус контейнеров:

```bash
docker-compose ps
```

Все сервисы должны быть в статусе `Up`.

### Проверьте API:

Откройте в браузере:
- **API Health**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs

Вы должны увидеть Swagger UI с документацией API.

### Проверьте Flower (мониторинг Celery):

- **Flower**: http://localhost:5555

## Шаг 5: Тестирование API

### 1. Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }'
```

### 2. Вход в систему

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

Сохраните полученный `access_token`.

### 3. Проверка профиля

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer ВАШ_ACCESS_TOKEN"
```

## Шаг 6: Добавление бота (опционально)

### 1. Создайте бота через @BotFather в Telegram

1. Откройте [@BotFather](https://t.me/botfather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен бота

### 2. Добавьте бота через API

```bash
curl -X POST "http://localhost:8000/api/v1/bots" \
  -H "Authorization: Bearer ВАШ_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_token": "ВАШ_ТОКЕН_БОТА"
  }'
```

## 📊 Мониторинг и логи

### Просмотр логов

```bash
# Все логи
docker-compose logs -f

# Логи backend
docker-compose logs -f backend

# Логи Celery worker
docker-compose logs -f celery_worker

# Логи базы данных
docker-compose logs -f db
```

### Мониторинг задач Celery

Откройте http://localhost:5555 для просмотра:
- Запущенных задач
- Истории выполнения
- Статуса воркеров

## 🛑 Остановка проекта

### Остановить все сервисы:

```bash
docker-compose stop
```

### Остановить и удалить контейнеры:

```bash
docker-compose down
```

### Полная очистка (включая volumes):

```bash
docker-compose down -v
```

⚠️ Внимание: это удалит все данные из базы данных!

## 🔧 Разработка

### Запуск backend в режиме разработки (без Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Запуск frontend (когда установлен Node.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на http://localhost:3000

## 📝 Полезные команды

### Перезапуск определенного сервиса

```bash
docker-compose restart backend
docker-compose restart celery_worker
```

### Выполнение команд внутри контейнера

```bash
# Зайти в shell backend контейнера
docker-compose exec backend bash

# Выполнить Python команду
docker-compose exec backend python -c "print('Hello')"

# Создать новую миграцию
docker-compose exec backend alembic revision --autogenerate -m "описание"
```

### Очистка Docker

```bash
# Удалить неиспользуемые образы
docker image prune -a

# Удалить неиспользуемые volumes
docker volume prune
```

## 🐛 Устранение проблем

### Проблема: Порты уже заняты

Если порты 5432 (PostgreSQL), 6379 (Redis) или 8000 (Backend) уже используются:

1. Остановите другие приложения использующие эти порты
2. Или измените порты в `docker-compose.yml`

### Проблема: Контейнеры не запускаются

```bash
# Посмотрите логи
docker-compose logs

# Пересоздайте контейнеры
docker-compose down
docker-compose up -d --build
```

### Проблема: Ошибки миграций БД

```bash
# Сбросьте базу данных
docker-compose down -v
docker-compose up -d db redis
sleep 5
docker-compose up -d backend
docker-compose exec backend alembic upgrade head
```

## 🎯 Следующие шаги

После успешного запуска вы можете:

1. ✅ Зарегистрировать пользователя через API
2. ✅ Добавить Telegram бота
3. ✅ Добавить канал для мониторинга
4. ✅ Посмотреть аналитику
5. ✅ Настроить экспорт в Google Sheets

Полная документация доступна в файле [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)

---

**Нужна помощь?** Откройте issue или смотрите документацию по адресу http://localhost:8000/docs
