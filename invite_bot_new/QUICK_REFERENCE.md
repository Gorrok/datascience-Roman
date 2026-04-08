# ⚡ Быстрая шпаргалка - Invite Tracker Bot

## 🎯 Подготовка (5 минут)

1. **@BotFather** → `/newbot` → сохранить токен
2. **@username_to_id_bot** → добавить в канал → получить ID
3. **Google Cloud** → Service Account → скачать credentials.json
4. **Google Sheets** → создать таблицу → 2 листа (Members, Links) → дать доступ email

## 📝 Настройка кода

Файл `invite_tracker.py` (строки 15-17):
```python
TELEGRAM_BOT_TOKEN = 'ваш_токен'
CHANNEL_USERNAME = -1001234567890
SPREADSHEET_NAME = 'Название таблицы'
```

## 🚀 Деплой на Beget (5 команд)

```bash
# 1. SSH
ssh user@host.beget.tech

# 2. Установка
mkdir -p ~/invite_bot && cd ~/invite_bot
mv ~/invite_tracker.py ~/credentials.json ~/requirements.txt .

# 3. Venv
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 4. Тест
python3 invite_tracker.py  # Ctrl+C если ОК

# 5. Systemd (создайте invitebot.service и установите)
sudo cp invitebot.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable invitebot.service && sudo systemctl start invitebot.service
```

## 🔧 Управление

```bash
sudo systemctl start invitebot.service    # Запуск
sudo systemctl stop invitebot.service     # Остановка
sudo systemctl restart invitebot.service  # Перезапуск
sudo systemctl status invitebot.service   # Статус
sudo journalctl -u invitebot.service -f   # Логи
```

## 📋 Systemd сервис

```ini
[Unit]
Description=Invite Tracker Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/bot/invite_tracker
ExecStart=/bot/invite_tracker/venv/bin/python /bot/invite_tracker/invite_tracker.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## ❗ Частые проблемы

**ModuleNotFoundError:**
```bash
source venv/bin/activate && pip install -r requirements.txt
```

**SpreadsheetNotFound:**
- Проверить название таблицы
- Дать доступ email из credentials.json (Редактор)

**Бот не получает события:**
- Бот = администратор канала
- Права: "Invite Users via Link" + "Approve New Members"
- В канале включен "Approve New Members"

## 📁 Файлы

```
invite_tracker.py       # Настроить токен, ID, название
credentials.json        # Ваш файл от Google
requirements.txt        # Зависимости
invitebot.service      # Systemd сервис
```

---

**Полная инструкция:** FULL_GUIDE.md
