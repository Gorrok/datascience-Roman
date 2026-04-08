# 🤖 Telegram Invite Tracker Bot - Полный гайд по установке

> **Проверено и работает!** Mickey Edition 2.0  
> Дата: 2026-02-19

## 📋 Что делает бот:

- ✅ Отслеживает запросы на вступление в Telegram канал
- ✅ Записывает данные в Google Sheets (User ID, Link Name, Join Date)
- ✅ Автоматически обновляет список инвайт-ссылок каждые 5 минут
- ✅ Работает как systemd сервис с автозапуском
- ✅ БЕЗ автоодобрения заявок (только отслеживание)

---

## 🎯 ЧТО НУЖНО ПОДГОТОВИТЬ (до деплоя):

### 1. Telegram бот
- Создайте бота через [@BotFather](https://t.me/BotFather) → `/newbot`
- Сохраните токен (например: `7773528819:AAFT2HUPl-axcFCvYVYc5uHmgQZfMNKcOfE`)

### 2. ID канала
- Добавьте [@username_to_id_bot](https://t.me/username_to_id_bot) в канал
- Получите ID (например: `-1001589094262`)
- Удалите бота из канала

### 3. Google Sheets API
1. Зайдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте проект
3. Включите Google Sheets API и Google Drive API
4. Создайте Service Account
5. Создайте ключ (JSON) → скачайте как `credentials.json`
6. Откройте файл и скопируйте `client_email` (нужен для шага 4)

### 4. Google Sheets таблица
1. Создайте таблицу: [https://sheets.google.com](https://sheets.google.com)
2. Назовите: `Invite tracker mickey` (или любое имя, но запомните)
3. Создайте 2 листа:
   - **Members** (заголовки: User ID | Link Name | Join Date)
   - **Links** (заголовки: Link Name | Invite Link | Created Date)
4. **ВАЖНО!** Нажмите "Поделиться" → добавьте email из credentials.json → роль "Редактор"

### 5. Настройка канала
1. Добавьте бота в канал как администратора
2. Дайте права: "Invite Users via Link" и "Approve New Members"
3. В настройках канала включите "Approve New Members"

---

## 📦 ЧТО ЗАГРУЗИТЬ НА СЕРВЕР:

### Обязательные файлы:
1. **invite_tracker.py** - основной код бота
2. **credentials.json** - ваш файл от Google Cloud
3. **requirements.txt** - зависимости Python

### Где взять файлы:
```
/Users/romanmuhachev/Documents/GitHub/datascience-Roman/invite_bot_new/
├── invite_tracker.py       ← загрузить
├── credentials.json        ← ваш файл
├── requirements.txt        ← загрузить
└── invitebot.service       ← опционально
```

---

## 🚀 УСТАНОВКА НА BEGET (пошагово):

### ШАГ 1: Настройте код (локально перед загрузкой)

Откройте `invite_tracker.py` и измените строки 15-17:

```python
TELEGRAM_BOT_TOKEN = '7773528819:AAFT2HUPl-axcFCvYVYc5uHmgQZfMNKcOfE'  # ← ваш токен
CHANNEL_USERNAME = -1001589094262  # ← ваш ID канала
SPREADSHEET_NAME = 'Invite tracker mickey'  # ← название вашей таблицы
```

### ШАГ 2: Загрузите файлы

**Через панель Beget:**
1. Зайдите в "Файловый менеджер"
2. Загрузите 3 файла:
   - invite_tracker.py (настроенный!)
   - credentials.json
   - requirements.txt

**Или через SCP:**
```bash
scp invite_tracker.py user@host.beget.tech:~/
scp credentials.json user@host.beget.tech:~/
scp requirements.txt user@host.beget.tech:~/
```

### ШАГ 3: Подключитесь по SSH

```bash
ssh your_username@your_host.beget.tech
```

### ШАГ 4: Создайте директорию и переместите файлы

```bash
# Проверьте где файлы
ls -la ~/

# Создайте директорию
mkdir -p ~/invite_bot
cd ~/invite_bot

# Переместите файлы (если в корне ~/)
mv ~/invite_tracker.py .
mv ~/credentials.json .
mv ~/requirements.txt .

# Проверьте
ls -la
```

### ШАГ 5: Создайте виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

*Должна появиться `(venv)` в начале строки*

### ШАГ 6: Установите зависимости

```bash
pip install -r requirements.txt
```

*Подождите 1-2 минуты*

### ШАГ 7: ТЕСТОВЫЙ ЗАПУСК

```bash
python3 invite_tracker.py
```

**Должны увидеть:**
```
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot.../getMe "HTTP/1.1 200 OK"
INFO:telegram.ext.Application:Application started
```

✅ **Если видите это - ОТЛИЧНО! Бот работает!**

❌ **Если ошибка `SpreadsheetNotFound`:**
   - Проверьте название таблицы (должно совпадать с кодом)
   - Проверьте что email из credentials.json добавлен в таблицу

**Остановите бота:** `Ctrl+C`

### ШАГ 8: Создайте systemd сервис

```bash
# Узнайте ваш путь и пользователя
pwd
whoami

# Создайте файл сервиса
nano ~/invite_bot/invitebot.service
```

**Вставьте (замените пути на свои!):**

```ini
[Unit]
Description=Mickey Invite Tracker Bot
After=network.target

[Service]
Type=simple
User=root                                          # ← ваш username
WorkingDirectory=/bot/invite_tracker               # ← ваш путь (из pwd)
ExecStart=/bot/invite_tracker/venv/bin/python /bot/invite_tracker/invite_tracker.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Сохраните:** `Ctrl+O`, `Enter`, `Ctrl+X`

### ШАГ 9: Установите сервис

```bash
sudo cp ~/invite_bot/invitebot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable invitebot.service
sudo systemctl start invitebot.service
```

### ШАГ 10: Проверьте статус

```bash
sudo systemctl status invitebot.service
```

**Должно быть:** `Active: active (running)` 🟢

### ШАГ 11: Смотрите логи

```bash
# Логи в реальном времени
sudo journalctl -u invitebot.service -f

# Последние 50 строк
sudo journalctl -u invitebot.service -n 50

# Только ошибки
sudo journalctl -u invitebot.service -p err
```

---

## 🎉 ГОТОВО!

Бот работает и будет автоматически запускаться при перезагрузке сервера!

---

## 🔧 УПРАВЛЕНИЕ БОТОМ:

```bash
# Запуск
sudo systemctl start invitebot.service

# Остановка
sudo systemctl stop invitebot.service

# Перезапуск
sudo systemctl restart invitebot.service

# Статус
sudo systemctl status invitebot.service

# Логи
sudo journalctl -u invitebot.service -f
```

---

## 🆘 РЕШЕНИЕ ПРОБЛЕМ:

### Бот не запускается

```bash
# Проверьте логи
sudo journalctl -u invitebot.service -n 100

# Проверьте файлы
ls -la ~/invite_bot/

# Проверьте venv
ls -la ~/invite_bot/venv/bin/python

# Запустите вручную для отладки
cd ~/invite_bot
source venv/bin/activate
python3 invite_tracker.py
```

### Ошибка `ModuleNotFoundError: No module named 'gspread'`

```bash
cd ~/invite_bot
source venv/bin/activate
pip install -r requirements.txt
```

### Ошибка `SpreadsheetNotFound`

**Проблема:** Бот не может найти таблицу Google Sheets

**Решение:**
1. Проверьте название таблицы (должно точно совпадать с кодом)
2. Откройте credentials.json: `cat ~/invite_bot/credentials.json | grep client_email`
3. Скопируйте email
4. Откройте таблицу в Google Sheets → "Поделиться" → добавьте этот email → роль "Редактор"
5. Проверьте что листы называются "Members" и "Links" (с большой буквы)

### Бот не получает события из канала

1. Проверьте что бот добавлен в канал как **администратор**
2. Проверьте права бота: "Invite Users via Link" и "Approve New Members"
3. Проверьте что в канале включен режим "Approve New Members"
4. Проверьте ID канала в коде (должен быть с минусом, например: `-1001589094262`)

---

## 📊 СТРУКТУРА ДАННЫХ В GOOGLE SHEETS:

### Лист "Members"
| User ID | Link Name | Join Date |
|---------|-----------|-----------|
| 123456789 | VIP ссылка | 2026-02-19 10:30:00 |
| 987654321 | Акция | 2026-02-19 11:45:00 |

### Лист "Links"
| Link Name | Invite Link | Created Date |
|-----------|-------------|--------------|
| VIP ссылка | https://t.me/+abc... | 2026-02-19 09:00:00 |
| Акция | https://t.me/+xyz... | 2026-02-19 10:00:00 |

---

## ⚙️ НАСТРОЙКИ БОТА:

Все настройки в файле `invite_tracker.py` (строки 15-17):

```python
TELEGRAM_BOT_TOKEN = 'ваш_токен'
CHANNEL_USERNAME = -1001234567890  # ID канала
SPREADSHEET_NAME = 'Название таблицы'
```

Частота обновления инвайт-ссылок (строка 68):
```python
await asyncio.sleep(300)  # 300 секунд = 5 минут
```

---

## 📁 ФАЙЛЫ ПРОЕКТА:

```
invite_bot_new/
├── invite_tracker.py              # Основной код (настроить!)
├── requirements.txt               # Зависимости
├── credentials.json               # Ваш файл от Google
├── invitebot.service             # Systemd сервис
├── FULL_GUIDE.md                 # ← Эта инструкция
├── SSH_INSTRUCTIONS.txt          # Быстрая шпаргалка
└── mickey_invite_bot_*.tar.gz    # Архив для деплоя
```

---

## 🎯 ЧЕКЛИСТ ДЛЯ НОВОГО ДЕПЛОЯ:

### Подготовка (локально):
- [ ] Создал бота через @BotFather (получил токен)
- [ ] Получил ID канала
- [ ] Создал Service Account в Google Cloud (получил credentials.json)
- [ ] Создал таблицу Google Sheets
- [ ] Создал листы "Members" и "Links"
- [ ] Дал доступ к таблице (email из credentials.json)
- [ ] Настроил invite_tracker.py (токен, ID канала, название таблицы)
- [ ] Добавил бота в канал как администратора
- [ ] Дал права боту в канале
- [ ] Включил режим "Approve New Members" в канале

### Деплой (на сервере):
- [ ] Загрузил файлы на Beget (invite_tracker.py, credentials.json, requirements.txt)
- [ ] Подключился по SSH
- [ ] Создал директорию и переместил файлы
- [ ] Создал venv
- [ ] Установил зависимости
- [ ] Протестировал запуск вручную
- [ ] Создал systemd сервис
- [ ] Установил и запустил сервис
- [ ] Проверил логи

---

## 💾 ГДЕ ХРАНЯТСЯ ЛОГИ:

```bash
# Системные логи (через journalctl)
sudo journalctl -u invitebot.service -f

# Логи хранятся в systemd журнале
# Для просмотра истории:
sudo journalctl -u invitebot.service --since "1 hour ago"
sudo journalctl -u invitebot.service --since "today"
```

---

## 🔄 ОБНОВЛЕНИЕ БОТА:

Если нужно обновить код:

```bash
# Остановите бота
sudo systemctl stop invitebot.service

# Отредактируйте код
nano ~/invite_bot/invite_tracker.py

# Или загрузите новый файл через FileZilla

# Запустите снова
sudo systemctl start invitebot.service

# Проверьте
sudo systemctl status invitebot.service
```

---

## 🚀 БЫСТРЫЙ СТАРТ (для опытных):

```bash
# 1. Загрузите файлы на сервер
# 2. SSH подключение
ssh user@host.beget.tech

# 3. Установка
mkdir -p ~/invite_bot && cd ~/invite_bot
mv ~/invite_tracker.py ~/credentials.json ~/requirements.txt .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Тест
python3 invite_tracker.py
# Ctrl+C

# 5. Systemd
nano invitebot.service  # создайте и настройте
sudo cp invitebot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable invitebot.service
sudo systemctl start invitebot.service
sudo systemctl status invitebot.service
```

---

## 📞 КОНТАКТЫ:

**Автор:** Roman Muhachev  
**Версия:** 2.0 (Mickey Edition)  
**Дата:** 2026-02-19  
**Проверено:** ✅ Работает на Beget

---

## 📝 ИСТОРИЯ ВЕРСИЙ:

**v2.0** (2026-02-19):
- Проверено на реальном сервере Beget
- Добавлена полная инструкция
- Systemd сервис с автозапуском
- БЕЗ автоодобрения заявок

---

**🎉 Успешного деплоя!**
