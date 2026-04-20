# 📊 Telegram Analytics SaaS

> **Красивая SaaS-платформа для аналитики Telegram каналов**

Минималистичный интерфейс, запуск за 2 минуты, интуитивно понятный для любых пользователей.

🎨 **Новый дизайн!** Забудьте про Swagger — теперь у вас современный UI с онбордингом и красивыми дашбордами.

## ✅ Статус: Готово к запуску!

🎯 **Хотите быстро запустить?** → Смотрите [START_HERE.md](START_HERE.md)

Проект полностью реализован. См. [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) для полной документации.

## ✨ Особенности

- 🎨 **Красивый минималистичный интерфейс** — удобно для обычных пользователей
- 🤖 **Мультиботовая архитектура** — каждый использует своего бота
- 📊 **Продвинутая аналитика** — графики, KPI, эффективность инвайт-ссылок
- 📈 **Дашборды в реальном времени**
- 📑 **Экспорт в Google Sheets**
- 💳 **Система подписок с Stripe**
- 🔒 **Безопасность и изоляция данных**

## Технологический стек

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL / SQLite
- Redis
- Celery
- SQLAlchemy 2.0

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- TailwindCSS
- shadcn/ui

## 🎨 Новый интерфейс

Красивый, минималистичный UI вместо технического Swagger:

- ✅ **Главная страница** с Hero и описанием в 3 шага
- ✅ **Онбординг** для новых пользователей (гайд по добавлению бота)
- ✅ **Минималистичный дашборд** с KPI и графиками
- ✅ **Интуитивно понятный** для обычных пользователей
- ✅ **Современный дизайн** с градиентами и плавными переходами

👉 **[Подробнее про новый дизайн →](BEAUTIFUL_FRONTEND.md)**

## Структура проекта

```
telegram-analytics-saas/
├── backend/          # FastAPI приложение
├── frontend/         # Next.js приложение
├── bot_worker/       # Celery workers для ботов
├── docker/           # Dockerfiles
└── docker-compose.yml
```

## 🚀 Деплой на продакшн

**Готово к деплою на Beget!** 🔥

- 📝 **[DEPLOY_QUICK.md](DEPLOY_QUICK.md)** - Быстрая инструкция (3 шага)
- 📖 **[DEPLOY_BEGET.md](DEPLOY_BEGET.md)** - Подробный гайд
- 🤖 **[deploy.sh](deploy.sh)** - Автоматический скрипт деплоя

```bash
# Автоматический деплой одной командой!
export BEGET_USER="your_login"
export BEGET_HOST="yourserver.beget.tech"
./deploy.sh
```

---

## 🚀 Быстрый старт (локально)

### Вариант 1: Самый простой запуск (рекомендуется для начала)

Для быстрого тестирования без установки Docker/PostgreSQL/Redis:

```bash
cd telegram-analytics-saas
./quick_start.sh
```

Это запустит backend с SQLite базой данных.

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs ← Начните здесь!

📖 Подробнее: [QUICKSTART_SIMPLE.md](QUICKSTART_SIMPLE.md)

### Вариант 2: Полный запуск с Docker

Если у вас установлен Docker:

```bash
cd telegram-analytics-saas
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Flower** (мониторинг Celery): http://localhost:5555

📖 Подробнее: [QUICKSTART.md](QUICKSTART.md)

### Вариант 3: Локальная разработка без Docker

Если хотите запустить всё локально:

📖 Смотрите: [QUICKSTART_NO_DOCKER.md](QUICKSTART_NO_DOCKER.md)

## 📝 Первые шаги

1. Запустите backend (любой из вариантов выше)
2. Откройте http://localhost:8000/docs
3. Зарегистрируйте пользователя через Swagger UI
4. Получите access token при входе
5. Добавьте Telegram бота
6. Начните мониторинг каналов!

## Реализованные функции

✅ JWT аутентификация  
✅ Управление ботами (добавление, старт/стоп)  
✅ Мониторинг каналов  
✅ Детальная аналитика (stats, trends, retention)  
✅ Статистика инвайт-ссылок  
✅ Экспорт в Google Sheets  
✅ Stripe интеграция (подписки, платежи)  
✅ Dashboard с KPI метриками  

## 📚 Документация

### 🚀 Быстрый старт
- **[START_HERE.md](START_HERE.md)** ← 👈 Начните отсюда!
- [QUICKSTART_SIMPLE.md](QUICKSTART_SIMPLE.md) - Самый простой запуск
- [QUICKSTART.md](QUICKSTART.md) - Запуск с Docker
- [QUICKSTART_NO_DOCKER.md](QUICKSTART_NO_DOCKER.md) - Без Docker

### 📖 Справочники
- [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) - Полная документация
- [CHEATSHEET.md](CHEATSHEET.md) - Шпаргалка команд
- [DOCS_INDEX.md](DOCS_INDEX.md) - Навигация по всей документации

### 🌐 API Документация
- **Swagger UI**: http://localhost:8000/docs (после запуска)
- **ReDoc**: http://localhost:8000/redoc

## Лицензия

MIT

