# 🚀 START HERE

> **Самый быстрый способ начать работу с платформой**

## 🎨 Новинка: Красивый интерфейс!

Забудьте про Swagger! Теперь у вас минималистичный UI с онбордингом для пользователей.

👉 **[Смотреть описание дизайна →](BEAUTIFUL_FRONTEND.md)**

---

## Выберите способ запуска

### 🎨 Полный запуск с красивым UI (рекомендуется!)

**Backend + Frontend вместе:**

```bash
# Терминал 1: Backend
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Терминал 2: Frontend
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/frontend
npm install
npm run dev
```

Откройте **http://localhost:3000** 🎉

👉 **[Подробная инструкция с Frontend →](FULL_START.md)**

---

### ⚡ Только Backend (API)

**Если у вас уже запущено:**

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: **http://localhost:8000/docs**

---

### 🆕 Первый запуск (автоматическая установка)

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas
./quick_start.sh
```

Скрипт автоматически:
- Создаст виртуальное окружение
- Установит зависимости
- Создаст базу данных SQLite
- Запустит backend

---

## Что дальше?

### После запуска backend:
1. Откройте API документацию: **http://localhost:8000/docs**
2. Зарегистрируйтесь через `POST /api/v1/auth/register`
3. Добавьте бота через `POST /api/v1/bots/`

### После запуска frontend:
1. Откройте **http://localhost:3000**
2. Нажмите "Начать бесплатно"
3. Зарегистрируйтесь
4. Добавьте бота (токен из @BotFather)
5. Смотрите аналитику! 📊

---

## Документация

### Быстрый старт:
- **[FULL_START.md](FULL_START.md)** - Полный запуск Backend + Frontend
- **[QUICKSTART.md](QUICKSTART.md)** - Docker Compose запуск
- **[MANUAL_START.md](MANUAL_START.md)** - Ручная установка backend

### Дизайн:
- **[BEAUTIFUL_FRONTEND.md](BEAUTIFUL_FRONTEND.md)** - Описание нового UI
- **[frontend/FRONTEND_README.md](frontend/FRONTEND_README.md)** - Frontend документация

### Полная документация:
- **[DOCS_INDEX.md](DOCS_INDEX.md)** - Индекс всей документации
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Детали реализации
- **[CHEATSHEET.md](CHEATSHEET.md)** - Шпаргалка по командам

---

**Готово!** Выберите способ запуска выше и начинайте! 🚀
