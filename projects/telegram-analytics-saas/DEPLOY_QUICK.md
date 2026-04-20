# 🚀 БЫСТРЫЙ ДЕПЛОЙ НА BEGET

## Способ 1: Автоматический (рекомендуется)

### Шаг 1: Настройте переменные окружения

```bash
export BEGET_USER="ваш_логин"
export BEGET_HOST="yourserver.beget.tech"
export BEGET_PATH="~/telegram-analytics"
```

### Шаг 2: Запустите скрипт деплоя

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas
./deploy.sh
```

Скрипт автоматически:
- ✅ Создаст архив проекта
- ✅ Загрузит на сервер
- ✅ Установит зависимости
- ✅ Настроит базу данных
- ✅ Соберёт frontend

### Шаг 3: Подключитесь к серверу и запустите

```bash
ssh $BEGET_USER@$BEGET_HOST

# Backend
cd ~/telegram-analytics/backend
source venv/bin/activate
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --daemon

# Frontend  
cd ~/telegram-analytics/frontend
npm start &
```

---

## Способ 2: Ручной

### 1. Создайте архив

```bash
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas

tar -czf telegram-analytics.tar.gz \
  --exclude='backend/venv' \
  --exclude='backend/__pycache__' \
  --exclude='backend/*.db' \
  --exclude='frontend/node_modules' \
  --exclude='frontend/.next' \
  backend/ frontend/
```

### 2. Загрузите на Beget

```bash
scp telegram-analytics.tar.gz username@yourserver.beget.tech:~/
```

### 3. На сервере

```bash
ssh username@yourserver.beget.tech

mkdir -p ~/telegram-analytics
cd ~/telegram-analytics
tar -xzf ~/telegram-analytics.tar.gz

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-sqlite.txt gunicorn
alembic upgrade head

# Frontend
cd ../frontend
npm install
npm run build
```

---

## Настройка автозапуска

### Вариант A: Screen (простой)

```bash
# Backend
screen -dmS telegram-backend bash -c 'cd ~/telegram-analytics/backend && source venv/bin/activate && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000'

# Frontend
screen -dmS telegram-frontend bash -c 'cd ~/telegram-analytics/frontend && npm start'

# Проверка
screen -ls
```

### Вариант B: PM2 (для Node.js)

```bash
npm install -g pm2

# Frontend
cd ~/telegram-analytics/frontend
pm2 start npm --name "telegram-frontend" -- start

# Backend
pm2 start "gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000" --name "telegram-backend" --cwd ~/telegram-analytics/backend

# Автозапуск при перезагрузке
pm2 startup
pm2 save
```

### Вариант C: Cron (для перезапуска)

```bash
crontab -e

# Добавьте:
@reboot cd ~/telegram-analytics/backend && source venv/bin/activate && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &
@reboot cd ~/telegram-analytics/frontend && npm start &
```

---

## Проверка работы

### Backend

```bash
curl http://localhost:8000/health
# Ответ: {"status":"healthy"}

curl http://localhost:8000/docs
# Откроется Swagger UI
```

### Frontend

```bash
curl http://localhost:3000
# Должна вернуться HTML страница
```

---

## Обновление (после изменений)

```bash
# Локально
./deploy.sh

# На сервере
cd ~/telegram-analytics

# Перезапустите backend
pkill -f gunicorn
cd backend && source venv/bin/activate
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --daemon

# Перезапустите frontend
pm2 restart telegram-frontend
# или
pkill -f "npm start"
cd frontend && npm start &
```

---

## Troubleshooting

### Ошибка "Permission denied"

```bash
chmod +x deploy.sh
```

### Backend не запускается

```bash
# Проверьте логи
tail -f ~/telegram-analytics/backend/logs/error.log

# Проверьте порт
netstat -tulpn | grep 8000
```

### Frontend не собирается

```bash
cd ~/telegram-analytics/frontend
rm -rf node_modules .next package-lock.json
npm install
npm run build
```

---

**Готово!** 🎉 Ваш проект на Beget! 🚀
