# 🚀 Деплой на Beget - ПОЛНЫЙ ГААААЗ!

## Что нужно сделать

### 1. Backend (FastAPI)
- ✅ Подготовить requirements.txt
- ✅ Настроить production конфиг
- ✅ Создать deploy скрипт
- ✅ Настроить systemd/supervisor

### 2. Frontend (Next.js)
- ✅ Собрать production build
- ✅ Настроить static export или Node.js сервер
- ✅ Настроить nginx

### 3. База данных
- ✅ SQLite (простой вариант)
- ⚠️ PostgreSQL (если нужен)

## Быстрый старт на Beget

### Шаг 1: Подключитесь к серверу

```bash
ssh username@yourserver.beget.tech
```

### Шаг 2: Создайте папку проекта

```bash
mkdir -p ~/telegram-analytics
cd ~/telegram-analytics
```

### Шаг 3: Загрузите файлы

**Вариант A: Через SCP**
```bash
# На локальном компьютере
cd /Users/romanmuhachev/Documents/GitHub/datascience-Roman/telegram-analytics-saas
tar -czf telegram-analytics-deploy.tar.gz backend/ frontend/ docker/
scp telegram-analytics-deploy.tar.gz username@yourserver.beget.tech:~/telegram-analytics/

# На сервере
cd ~/telegram-analytics
tar -xzf telegram-analytics-deploy.tar.gz
```

**Вариант B: Через Git**
```bash
# На сервере
cd ~/telegram-analytics
git clone https://github.com/yourusername/telegram-analytics-saas.git .
```

### Шаг 4: Настройте Backend

```bash
cd ~/telegram-analytics/backend

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements-sqlite.txt
pip install gunicorn

# Создайте .env
cat > .env << 'EOF'
# Database
DATABASE_URL=sqlite+aiosqlite:///./telegram_analytics.db
DATABASE_URL_SYNC=sqlite:///./telegram_analytics.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ENCRYPTION_KEY=your-32-char-encryption-key-here

# CORS
CORS_ORIGINS=["https://yourdomain.beget.tech"]

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
EOF

# Запустите миграции
alembic upgrade head

# Тестовый запуск
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Шаг 5: Настройте автозапуск (Supervisor)

Создайте файл конфигурации:

```bash
cat > ~/telegram-analytics/supervisor-backend.conf << 'EOF'
[program:telegram-analytics-backend]
directory=/home/username/telegram-analytics/backend
command=/home/username/telegram-analytics/backend/venv/bin/gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
user=username
autostart=true
autorestart=true
stderr_logfile=/home/username/telegram-analytics/backend.err.log
stdout_logfile=/home/username/telegram-analytics/backend.out.log
EOF
```

Подключите к supervisord:
```bash
# Свяжитесь с поддержкой Beget для активации supervisor
# Или используйте cron для автозапуска
```

### Шаг 6: Настройте Frontend

**Вариант A: Static Export (рекомендуется для Beget)**

```bash
cd ~/telegram-analytics/frontend

# Установите Node.js (если нет)
# На Beget обычно уже установлен

# Установите зависимости
npm install

# Создайте .env.production
echo "NEXT_PUBLIC_API_URL=https://api.yourdomain.beget.tech" > .env.production

# Соберите статику
npm run build
```

**Вариант B: Node.js сервер**

```bash
# После npm run build
npm start
```

### Шаг 7: Настройте Nginx

Создайте конфиг:

```nginx
# /home/username/.nginx/telegram-analytics.conf

# Backend API
server {
    listen 80;
    server_name api.yourdomain.beget.tech;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.beget.tech;

    root /home/username/telegram-analytics/frontend/.next/server/app;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Шаг 8: Запустите!

```bash
# Перезагрузите nginx
nginx -s reload

# Проверьте backend
curl http://127.0.0.1:8000/health

# Откройте в браузере
# https://yourdomain.beget.tech
```

## Упрощённый вариант (без домена)

Если нет домена, можно использовать через IP:

```bash
# Backend на порту 8000
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &

# Frontend на порту 3000
cd frontend
npm run dev -- -H 0.0.0.0 &
```

Откройте: `http://YOUR_IP:3000`

## Особенности Beget

### 1. Python версия
```bash
python3 --version
# Должна быть >= 3.11
```

Если нужна другая версия, установите через:
```bash
pyenv install 3.11.0
pyenv local 3.11.0
```

### 2. Node.js версия
```bash
node --version
# Должна быть >= 18
```

### 3. База данных

**SQLite (простой вариант):**
- Уже настроено в `.env`
- Файл БД: `telegram_analytics.db`

**PostgreSQL (если нужен):**
```bash
# В панели Beget создайте базу данных
# Обновите .env:
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
DATABASE_URL_SYNC=postgresql://user:pass@localhost/dbname
```

### 4. HTTPS (SSL)

В панели Beget:
1. Перейдите в "Домены"
2. Выберите домен
3. Включите "Let's Encrypt SSL"

Обновите `.env`:
```bash
CORS_ORIGINS=["https://yourdomain.beget.tech"]
```

## Проверка работы

### Backend
```bash
curl https://api.yourdomain.beget.tech/health
# Ожидаем: {"status": "healthy"}

curl https://api.yourdomain.beget.tech/docs
# Откроется Swagger UI
```

### Frontend
```bash
curl https://yourdomain.beget.tech
# Должна загрузиться главная страница
```

## Troubleshooting

### Backend не запускается
```bash
# Проверьте логи
tail -f ~/telegram-analytics/backend.err.log

# Проверьте порт
netstat -tulpn | grep 8000

# Проверьте процесс
ps aux | grep gunicorn
```

### Frontend не собирается
```bash
# Очистите кэш
rm -rf .next node_modules package-lock.json
npm install
npm run build
```

### CORS ошибки
Проверьте в `backend/.env`:
```bash
CORS_ORIGINS=["https://yourdomain.beget.tech"]
```

---

**Готово к деплою!** 🚀 

Следующий шаг: создам автоматический deploy скрипт! 💪
