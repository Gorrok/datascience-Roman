# 🚀 Полный запуск (Backend + Frontend)

Запустите весь стек за 5 минут!

## Шаг 1: Запустите Backend

```bash
cd backend

# Активируйте виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Проверьте .env файл (должен быть настроен на SQLite)
cat .env

# Запустите миграции (если ещё не делали)
alembic upgrade head

# Запустите сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на **http://localhost:8000**

## Шаг 2: Запустите Frontend (в новом терминале)

```bash
cd frontend

# Установите зависимости (первый раз)
npm install

# Создайте .env.local (если ещё не создали)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Запустите dev-сервер
npm run dev
```

Frontend будет доступен на **http://localhost:3000**

## Шаг 3: Попробуйте!

1. Откройте **http://localhost:3000**
2. Нажмите "Начать бесплатно"
3. Зарегистрируйтесь (имя, email, пароль)
4. Добавьте своего бота (токен из @BotFather)
5. Выберите канал для мониторинга
6. Смотрите аналитику! 📊

## Что вы увидите

### Главная страница (`/`)
- Красивый Hero с градиентом
- "Как это работает" в 3 шага
- Карточки с фичами
- CTA кнопки

### После регистрации (`/dashboard`)
- **Если ботов нет**: онбординг с гайдом по добавлению бота
- **Если боты есть**: дашборд с KPI, графиками и топ инвайт-ссылками

## API эндпоинты (если нужно для отладки)

Backend API документация: **http://localhost:8000/docs**

Основные эндпоинты:
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Логин
- `GET /api/v1/auth/me` - Текущий пользователь
- `GET /api/v1/bots/` - Список ботов
- `POST /api/v1/bots/` - Добавить бота
- `GET /api/v1/channels/?bot_id=X` - Список каналов
- `GET /api/v1/analytics/{channel_id}/stats` - Статистика канала

## Остановка

### Backend
```bash
# В терминале backend нажмите:
Ctrl+C
```

### Frontend
```bash
# В терминале frontend нажмите:
Ctrl+C
```

## Проблемы?

### Backend не запускается
```bash
# Проверьте виртуальное окружение
which python  # должно показывать путь внутри venv/

# Проверьте зависимости
pip list | grep fastapi

# Проверьте .env файл
cat .env | grep DATABASE_URL
# Должно быть: DATABASE_URL=sqlite+aiosqlite:///./telegram_analytics.db
```

### Frontend не запускается
```bash
# Проверьте Node.js
node --version  # должно быть >= 18

# Переустановите зависимости
rm -rf node_modules package-lock.json
npm install

# Проверьте .env.local
cat .env.local
# Должно быть: NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Ошибка CORS
Убедитесь что в `backend/.env` есть:
```
CORS_ORIGINS=["http://localhost:3000"]
```

---

**Готово!** 🎉 Теперь у вас работает полный стек с красивым интерфейсом!
