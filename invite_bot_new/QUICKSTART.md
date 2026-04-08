# 🚀 Быстрый деплой на Beget

## Шаг 1: Подготовка (локально)

1. **Настройте конфигурацию** в `invite_tracker.py`:
   ```python
   TELEGRAM_BOT_TOKEN = 'ВАШ_ТОКЕН'
   CHANNEL_USERNAME = -1002207284486  # Ваш ID канала
   SPREADSHEET_NAME = 'TelegramInviteTracking'
   ```

2. **Подготовьте credentials.json** от Google Sheets API

## Шаг 2: Подключение к Beget

```bash
ssh your_username@your_host.beget.tech
```

## Шаг 3: Установка на сервере

```bash
# Создать директорию
mkdir -p ~/invite_bot
cd ~/invite_bot

# Загрузить файлы (через SCP или FileZilla):
# - invite_tracker.py
# - requirements.txt
# - credentials.json
# - invitebot.service

# Создать venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Шаг 4: Настройка systemd

```bash
# Отредактировать пути в invitebot.service
nano invitebot.service

# Установить сервис
sudo cp invitebot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable invitebot.service
sudo systemctl start invitebot.service

# Проверить
sudo systemctl status invitebot.service
```

## ✅ Готово!

Проверить логи:
```bash
sudo journalctl -u invitebot.service -f
```

Управление:
```bash
sudo systemctl start invitebot.service    # Запуск
sudo systemctl stop invitebot.service     # Остановка
sudo systemctl restart invitebot.service  # Перезапуск
sudo systemctl status invitebot.service   # Статус
```

## 📋 Чеклист перед запуском

- [ ] Токен бота получен от @BotFather
- [ ] ID канала получен (формат: -100XXXXXXXXXX)
- [ ] Google Sheets таблица создана с листами "Members" и "Links"
- [ ] credentials.json загружен
- [ ] Service account имеет доступ к таблице (Editor)
- [ ] Бот добавлен в канал как администратор
- [ ] В канале включен режим "Approve New Members"
- [ ] Боту даны права: "Invite Users via Link" и "Approve New Members"

---

Полная документация: [README.md](README.md)
