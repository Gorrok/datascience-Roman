# 📋 Шпаргалка команд

Быстрый справочник всех команд для работы с проектом.

## 🚀 Запуск

### Простой запуск (SQLite)
```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas
./quick_start.sh
```

### С Docker
```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## 🔗 Важные ссылки

| Сервис | URL |
|--------|-----|
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Flower (Celery) | http://localhost:5555 |

## 🛑 Остановка

### Простая версия
```bash
# Нажать Ctrl+C в терминале где запущен uvicorn
```

### Docker версия
```bash
docker-compose stop        # Остановить
docker-compose down        # Остановить и удалить контейнеры
docker-compose down -v     # + удалить данные
```

## 📊 Мониторинг

### Логи (Docker)
```bash
docker-compose logs -f              # Все логи
docker-compose logs -f backend      # Backend логи
docker-compose logs -f celery_worker # Celery логи
```

### Статус сервисов
```bash
docker-compose ps                   # Статус всех контейнеров
```

## 🗄️ База данных

### SQLite версия
```bash
cd backend
sqlite3 telegram_analytics.db
.tables                    # Список таблиц
SELECT * FROM users;       # Посмотреть пользователей
.quit                      # Выход
```

### PostgreSQL (Docker)
```bash
docker-compose exec db psql -U postgres -d telegram_analytics
\dt                        # Список таблиц
SELECT * FROM users;       # Посмотреть пользователей
\q                         # Выход
```

## 🔄 Миграции

### Применить миграции
```bash
# SQLite версия
cd backend && source venv/bin/activate
alembic upgrade head

# Docker версия
docker-compose exec backend alembic upgrade head
```

### Создать новую миграцию
```bash
# SQLite версия
cd backend && source venv/bin/activate
alembic revision --autogenerate -m "описание"

# Docker версия
docker-compose exec backend alembic revision --autogenerate -m "описание"
```

### Откатить миграцию
```bash
alembic downgrade -1       # На одну назад
```

## 🧪 Тестирование API

### Регистрация
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

### Вход
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"
```

### Проверка токена
```bash
TOKEN="ваш_access_token"
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### Добавление бота
```bash
TOKEN="ваш_access_token"
curl -X POST "http://localhost:8000/api/v1/bots" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_token": "YOUR_BOT_TOKEN"
  }'
```

## 🐍 Python окружение

### Активация venv
```bash
cd backend
source venv/bin/activate        # macOS/Linux
# или
venv\Scripts\activate           # Windows
```

### Установка зависимостей
```bash
pip install -r requirements.txt
pip install aiosqlite           # Для SQLite
```

### Деактивация
```bash
deactivate
```

## 🐳 Docker команды

### Пересборка образов
```bash
docker-compose build           # Пересобрать все
docker-compose build backend   # Пересобрать только backend
```

### Перезапуск сервиса
```bash
docker-compose restart backend
```

### Выполнение команд в контейнере
```bash
docker-compose exec backend bash           # Войти в shell
docker-compose exec backend python -c "..."# Выполнить Python
```

### Очистка
```bash
docker system prune -a         # Удалить неиспользуемые образы
docker volume prune            # Удалить неиспользуемые volumes
```

## 🔧 Разработка

### Запуск backend локально
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Запуск Celery worker
```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

### Запуск Flower
```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app flower --port=5555
```

### Запуск frontend (если установлен npm)
```bash
cd frontend
npm install
npm run dev
```

## 📝 Полезные переменные

### Установка переменных в shell
```bash
export API_URL="http://localhost:8000"
export TOKEN="your_access_token_here"
```

### Использование
```bash
curl -X GET "$API_URL/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## 🔍 Отладка

### Проверка портов
```bash
lsof -i :8000              # Кто использует порт 8000
lsof -i :5432              # PostgreSQL
lsof -i :6379              # Redis
```

### Убить процесс на порту
```bash
lsof -ti :8000 | xargs kill -9
```

### Проверка Python пакетов
```bash
pip list | grep fastapi
pip show fastapi
```

## 🎯 Быстрые задачи

### Сброс всего и запуск заново
```bash
# Docker версия
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head

# SQLite версия
cd backend
rm -f telegram_analytics.db
source venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload
```

### Создать тестовые данные
```bash
# Войдите в Python shell
cd backend && source venv/bin/activate
python

# В Python:
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
user = User(
    email="admin@test.com",
    hashed_password=get_password_hash("admin123"),
    full_name="Admin User",
    is_active=True
)
db.add(user)
db.commit()
print("User created!")
```

---

**Совет:** Добавьте эту страницу в закладки браузера для быстрого доступа!
