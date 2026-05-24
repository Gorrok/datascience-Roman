# 💕 Couples Planner Bot

Telegram Mini App для планирования совместных дел и хотелок для пары. Красивый, милый и уютный дизайн! 

## 📚 Документация

- **[QUICK_START.md](QUICK_START.md)** - быстрый старт за 5 минут ⚡
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - деплой как полноценное приложение 🚀
- **[WHY_TELEGRAM_ID.md](WHY_TELEGRAM_ID.md)** - зачем нужен Telegram ID? 🔐
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - архитектура проекта 📊

## 🎯 Возможности

- ✨ **Хотелки** - создавайте список того, что хотите сделать вместе
- 📅 **Планы** - назначайте конкретные даты для планов
- 💌 **Инвайты** - приглашайте друг друга на планы с уведомлениями
- ✅ **Отметки о выполнении** - отмечайте выполненные планы
- 📱 **Mini App** - красивый веб-интерфейс прямо в Telegram
- 🔔 **Уведомления** - получайте уведомления через Telegram бот

## 🏗️ Архитектура

Проект состоит из трех компонентов:

1. **Backend** (FastAPI) - API сервер с базой данных
2. **Bot** (aiogram) - Telegram бот для уведомлений
3. **Mini App** (React) - веб-интерфейс

```
┌─────────────────┐
│   Mini App      │  React приложение в Telegram
│   (React)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Backend       │  FastAPI + SQLite
│   (Python)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Telegram Bot  │  Уведомления и команды
│   (aiogram)     │
└─────────────────┘
```

## 📦 Установка

### 1. Клонируйте репозиторий

```bash
cd bots/couples-planner-bot
```

### 2. Настройка Backend

```bash
cd backend

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Скопируйте .env.example в .env
cp ../.env.example .env
```

### 3. Настройка Bot

```bash
cd bot

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте папку для логов
mkdir logs
```

### 4. Настройка Mini App

```bash
cd mini-app

# Установите зависимости
npm install

# Скопируйте .env.example в .env
cp .env.example .env
```

## 🔧 Конфигурация

### 1. Создайте Telegram бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен бота

### 2. Настройте Mini App в BotFather

1. Отправьте `/newapp` боту @BotFather
2. Выберите вашего бота
3. Введите название приложения
4. Введите описание
5. Загрузите иконку (512x512 px)
6. Введите URL вашего Mini App (после деплоя)
7. Введите короткое имя (используется в URL)

### 3. Узнайте ваши Telegram ID

Отправьте `/start` боту [@userinfobot](https://t.me/userinfobot) чтобы узнать ваш ID.

### 4. Заполните `.env` файл

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# Пользователи (только вы двое)
USER_1_ID=your_telegram_id
USER_1_NAME=Roman
USER_2_ID=katya_telegram_id
USER_2_NAME=Katya

# Backend
API_HOST=localhost
API_PORT=8000

# Database
DATABASE_URL=sqlite+aiosqlite:///./couples_planner.db

# Mini App URL (после деплоя укажите реальный)
MINI_APP_URL=https://your-domain.com
```

## 🚀 Запуск (Локально)

### Терминал 1: Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на http://localhost:8000

API документация: http://localhost:8000/docs

### Терминал 2: Bot

```bash
cd bot
source venv/bin/activate
python bot.py
```

### Терминал 3: Mini App

```bash
cd mini-app
npm run dev
```

Mini App будет доступен на http://localhost:5173

## 🌐 Деплой (Production)

### Вариант 1: Railway (Бесплатно)

**Backend + Bot:**

1. Зарегистрируйтесь на [Railway.app](https://railway.app)
2. Создайте новый проект
3. Подключите GitHub репозиторий
4. Добавьте переменные окружения из `.env`
5. Railway автоматически задеплоит приложение

**Mini App:**

1. Используйте [Vercel](https://vercel.com) или [Netlify](https://netlify.com)
2. Подключите папку `mini-app`
3. Установите переменную окружения `VITE_API_URL` с URL вашего backend

### Вариант 2: VPS (Полный контроль)

**Требования:**
- Ubuntu 20.04+
- Python 3.10+
- Node.js 18+
- Nginx

**Установка:**

```bash
# 1. Клонируйте репозиторий
git clone <your-repo>
cd couples-planner-bot

# 2. Запустите backend через systemd
sudo nano /etc/systemd/system/couples-backend.service

[Unit]
Description=Couples Planner Backend
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/couples-planner-bot/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

# 3. Запустите бот через systemd
sudo nano /etc/systemd/system/couples-bot.service

[Unit]
Description=Couples Planner Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/couples-planner-bot/bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target

# 4. Запустите сервисы
sudo systemctl enable couples-backend
sudo systemctl enable couples-bot
sudo systemctl start couples-backend
sudo systemctl start couples-bot

# 5. Соберите Mini App
cd mini-app
npm run build

# 6. Настройте Nginx
sudo nano /etc/nginx/sites-available/couples-planner

server {
    listen 80;
    server_name your-domain.com;
    
    # Mini App
    location / {
        root /path/to/couples-planner-bot/mini-app/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 7. Активируйте конфигурацию
sudo ln -s /etc/nginx/sites-available/couples-planner /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 8. Настройте SSL (опционально, но рекомендуется)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📱 Использование

### Через Mini App:

1. Откройте вашего бота в Telegram
2. Отправьте `/start`
3. Нажмите "🎯 Открыть планировщик"
4. Создавайте планы и хотелки
5. Приглашайте друг друга на планы

### Через бота:

- `/start` - главное меню
- Нажмите "📋 Мои планы" - увидите все планы
- Нажмите "📨 Инвайты" - увидите приглашения

### Уведомления:

Когда один человек приглашает другого на план, второму приходит уведомление в Telegram с кнопками "Принять" / "Отклонить".

## 🎨 Кастомизация

### Изменить цвета (Mini App):

Отредактируйте `mini-app/src/App.css`:

```css
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Измените на свои цвета */
}
```

### Добавить новые функции:

1. **Backend**: добавьте новый endpoint в `backend/app/api/plans.py`
2. **Bot**: добавьте новый handler в `bot/handlers/main.py`
3. **Mini App**: добавьте новый компонент в `mini-app/src/`

## 🐛 Отладка

### Проверка логов Backend:

```bash
# Смотрите логи uvicorn в терминале
# Или проверьте системные логи
sudo journalctl -u couples-backend -f
```

### Проверка логов Bot:

```bash
# Логи в файле
tail -f bot/logs/bot.log

# Или системные логи
sudo journalctl -u couples-bot -f
```

### Проверка API:

```bash
# Проверьте что API работает
curl http://localhost:8000/health

# Проверьте документацию
open http://localhost:8000/docs
```

## 📝 База данных

### Структура:

- **plans** - планы и хотелки
  - `id`, `title`, `description`, `plan_type`, `created_by_id`, `planned_date`, `is_completed`
  
- **invites** - приглашения
  - `id`, `plan_id`, `from_user_id`, `to_user_id`, `status`

### Резервное копирование:

```bash
# Создать бэкап
cp backend/couples_planner.db backup_$(date +%Y%m%d).db

# Восстановить
cp backup_20260524.db backend/couples_planner.db
```

## 🔒 Безопасность

- ✅ Только два пользователя могут использовать бот (проверка по ID)
- ✅ База данных хранится локально
- ✅ API не требует аутентификации (т.к. только для вас двоих)
- ✅ Данные не передаются третьим лицам

## 💡 Идеи для улучшения

- [ ] Push-уведомления за день до плана
- [ ] Фотографии к планам
- [ ] История выполненных планов
- [ ] Статистика (сколько планов выполнено)
- [ ] Категории планов (романтика, путешествия, кино и т.д.)
- [ ] Экспорт в календарь (iCal)
- [ ] Темная тема

## 🤝 Поддержка

Если что-то не работает:

1. Проверьте логи (backend, bot)
2. Проверьте что все сервисы запущены
3. Проверьте `.env` файл
4. Проверьте что Telegram ID правильные

## 📄 Лицензия

Это ваш личный проект для использования только вами и Катей 💕

---

**Создано с любовью для совместного планирования 💕**
