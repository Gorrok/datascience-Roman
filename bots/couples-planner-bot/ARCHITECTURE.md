# 📊 Архитектура проекта

## Общая структура

```
couples-planner-bot/
│
├── backend/                    # FastAPI сервер
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   └── plans.py       # Планы и инвайты
│   │   ├── core/              # Ядро приложения
│   │   │   ├── config.py      # Конфигурация
│   │   │   └── database.py    # Подключение к БД
│   │   ├── models/            # SQLAlchemy модели
│   │   │   └── plan.py        # Plan, Invite
│   │   ├── schemas/           # Pydantic схемы
│   │   │   └── plan.py        # DTO для API
│   │   └── main.py            # Точка входа
│   ├── requirements.txt
│   └── couples_planner.db     # SQLite база данных
│
├── bot/                       # Telegram бот
│   ├── handlers/              # Обработчики команд
│   │   └── main.py            # /start, callback queries
│   ├── keyboards/             # Клавиатуры
│   │   └── inline.py          # Inline кнопки
│   ├── utils/                 # Утилиты
│   │   └── api_client.py      # HTTP клиент для backend
│   ├── bot.py                 # Точка входа
│   ├── requirements.txt
│   └── logs/                  # Логи
│
├── mini-app/                  # React Mini App
│   ├── src/
│   │   ├── App.jsx            # Главный компонент
│   │   ├── App.css            # Стили
│   │   ├── api.js             # API клиент
│   │   └── main.jsx           # Точка входа
│   ├── public/                # Статические файлы
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .env.example               # Пример конфигурации
├── .gitignore
├── README.md                  # Полная документация
├── QUICK_START.md             # Быстрый старт
└── start_all.sh               # Скрипт запуска всех компонентов
```

## Поток данных

### 1. Создание плана

```
User (Mini App)
    │
    ├─> POST /api/plans/
    │       {
    │         "title": "Сходить в кино",
    │         "plan_type": "wish",
    │         "created_by_id": 123456
    │       }
    │
    ▼
Backend (FastAPI)
    │
    ├─> SQLAlchemy ORM
    │
    ▼
Database (SQLite)
    └─> Сохранение в таблицу plans
```

### 2. Отправка инвайта

```
User 1 (Mini App)
    │
    ├─> POST /api/plans/invites
    │       {
    │         "plan_id": 1,
    │         "from_user_id": 123456,
    │         "to_user_id": 789012
    │       }
    │
    ▼
Backend (FastAPI)
    │
    ├─> Сохранение инвайта
    │
    ▼
Telegram Bot
    │
    ├─> bot.send_message(to_user_id, ...)
    │
    ▼
User 2 получает уведомление в Telegram
    │
    └─> Нажимает "Принять" / "Отклонить"
```

### 3. Принятие инвайта

```
User 2 (Telegram Bot)
    │
    ├─> Callback: invite_accept_1
    │
    ▼
Bot Handler
    │
    ├─> PATCH /api/plans/invites/1/respond?status=accepted
    │
    ▼
Backend (FastAPI)
    │
    ├─> UPDATE invites SET status='accepted'
    │
    ▼
Database
    └─> План теперь виден обоим пользователям
```

## API Endpoints

### Plans

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/plans/` | Получить планы пользователя |
| POST | `/api/plans/` | Создать новый план |
| GET | `/api/plans/{id}` | Получить план по ID |
| PATCH | `/api/plans/{id}` | Обновить план |
| DELETE | `/api/plans/{id}` | Удалить план |

### Invites

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/plans/invites` | Отправить инвайт |
| GET | `/api/plans/invites/{user_id}` | Получить инвайты |
| PATCH | `/api/plans/invites/{id}/respond` | Ответить на инвайт |

## База данных

### Схема

```sql
-- Планы и хотелки
CREATE TABLE plans (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    plan_type ENUM('wish', 'plan') DEFAULT 'wish',
    created_by_id INTEGER NOT NULL,
    created_by_name VARCHAR(100),
    planned_date DATETIME NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Инвайты
CREATE TABLE invites (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    from_user_id INTEGER NOT NULL,
    from_user_name VARCHAR(100),
    to_user_id INTEGER NOT NULL,
    to_user_name VARCHAR(100),
    status ENUM('pending', 'accepted', 'declined') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    responded_at DATETIME NULL,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
);
```

### Индексы

```sql
-- Быстрый поиск планов пользователя
CREATE INDEX idx_plans_created_by ON plans(created_by_id);
CREATE INDEX idx_plans_planned_date ON plans(planned_date);

-- Быстрый поиск инвайтов
CREATE INDEX idx_invites_to_user ON invites(to_user_id);
CREATE INDEX idx_invites_status ON invites(status);
```

## Технологии

### Backend
- **FastAPI** 0.109.0 - современный Python фреймворк для API
- **SQLAlchemy** 2.0.25 - ORM для работы с БД
- **Pydantic** 2.5.3 - валидация данных
- **SQLite** - легкая встраиваемая БД
- **uvicorn** - ASGI сервер

### Bot
- **aiogram** 3.3.0 - асинхронный фреймворк для Telegram ботов
- **aiohttp** - асинхронный HTTP клиент
- **loguru** - красивое логирование

### Mini App
- **React** 18.2 - UI библиотека
- **Vite** - быстрый сборщик
- **Telegram WebApp SDK** - интеграция с Telegram
- **axios** - HTTP клиент

## Безопасность

### Аутентификация

В текущей версии:
- Не используется традиционная аутентификация (JWT, OAuth)
- Доступ ограничен по Telegram ID (только двое пользователей)
- Mini App использует `window.Telegram.WebApp.initData` для идентификации

### Рекомендации для production:

1. **Валидация Telegram данных:**
```python
def validate_telegram_data(init_data: str, bot_token: str) -> bool:
    # Проверка подписи от Telegram
    # https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    pass
```

2. **HTTPS обязательно:**
```nginx
# Настройте SSL сертификат
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

3. **Rate Limiting:**
```python
from slowapi import Limiter

limiter = Limiter(key_func=lambda: request.client.host)

@app.post("/api/plans/")
@limiter.limit("10/minute")
async def create_plan(...):
    pass
```

## Масштабирование

### Если захотите добавить больше пользователей:

1. **Добавьте таблицу users:**
```python
class User(Base):
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String(100))
    partner_id = Column(Integer, ForeignKey("users.id"))
```

2. **Добавьте регистрацию:**
```python
@router.post("/auth/register")
async def register(telegram_id: int):
    # Создать пользователя
    # Вернуть JWT токен
    pass
```

3. **Используйте PostgreSQL вместо SQLite:**
```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/couples_planner
```

## Мониторинг

### Логи

**Backend:**
- FastAPI логирует все запросы в stdout
- Uvicorn показывает HTTP статусы

**Bot:**
- Логи сохраняются в `bot/logs/bot.log`
- Ротация каждый день, хранятся 7 дней

### Метрики (опционально)

Можно добавить Prometheus + Grafana:

```python
from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)
```

---

**Последнее обновление:** 2026-05-24
