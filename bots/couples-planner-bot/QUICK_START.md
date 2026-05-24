# 🚀 Быстрый старт

Это краткая инструкция для быстрого запуска проекта. Полная документация в [README.md](README.md).

## 📋 Чеклист перед первым запуском

### 1. Создайте Telegram бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. `/newbot` → следуйте инструкциям
3. Скопируйте токен бота

### 2. Узнайте свои Telegram ID

Отправьте `/start` боту [@userinfobot](https://t.me/userinfobot)

### 3. Настройте окружение

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env файл
nano .env
```

Заполните:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather
USER_1_ID=ваш_telegram_id
USER_1_NAME=Роман
USER_2_ID=telegram_id_кати
USER_2_NAME=Катя
```

### 4. Установите зависимости

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Bot:**
```bash
cd bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir logs
```

**Mini App:**
```bash
cd mini-app
npm install
cp .env.example .env
```

## ⚡ Запуск

### Вариант 1: Автоматический (macOS)

```bash
./start_all.sh
```

Скрипт откроет 3 терминала:
- Backend API (http://localhost:8000)
- Telegram Bot
- Mini App (http://localhost:5173)

### Вариант 2: Ручной запуск

**Терминал 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Терминал 2 - Bot:**
```bash
cd bot
source venv/bin/activate
python bot.py
```

**Терминал 3 - Mini App:**
```bash
cd mini-app
npm run dev
```

## ✅ Проверка

1. Откройте http://localhost:8000/docs - должна открыться API документация
2. Откройте вашего бота в Telegram
3. Отправьте `/start`
4. Нажмите "🎯 Открыть планировщик"

## 🎯 Первое использование

1. **Создайте хотелку:**
   - Откройте Mini App
   - Вкладка "Создать"
   - Выберите "✨ Хотелка"
   - Введите название: "Сходить в кино"
   - Нажмите "Создать"

2. **Пригласите партнера:**
   - Откройте вкладку "Хотелки"
   - Найдите созданную хотелку
   - Нажмите "💌 Пригласить"
   - Партнеру придет уведомление в Telegram!

3. **Примите приглашение:**
   - Партнер получит сообщение от бота
   - Нажмите "✅ Принять"
   - План появится у обоих!

## 🐛 Проблемы?

**Backend не запускается:**
```bash
# Проверьте что порт 8000 свободен
lsof -i :8000

# Убейте процесс если нужно
kill -9 <PID>
```

**Bot не реагирует:**
```bash
# Проверьте логи
tail -f bot/logs/bot.log

# Проверьте токен в .env
cat .env | grep BOT_TOKEN
```

**Mini App не открывается:**
```bash
# Переустановите зависимости
cd mini-app
rm -rf node_modules package-lock.json
npm install
```

## 📚 Что дальше?

- Прочитайте полный [README.md](README.md) для деплоя
- Настройте Mini App URL в BotFather
- Задеплойте на Railway или VPS

---

**Готово! Наслаждайтесь совместным планированием 💕**
