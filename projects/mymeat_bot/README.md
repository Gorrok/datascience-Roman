# Mymeat Reminder Bot

Бот следит за сообщениями в группе и при слове **онлайн** отвечает:
> не забудь включить Mymeat 🎥

## Настройка

1. Создай бота через [@BotFather](https://t.me/BotFather) и получи токен
2. Вставь токен в `bot.py` → `BOT_TOKEN = "твой_токен"`
3. Добавь бота в нужную конфу и дай ему права на чтение сообщений
4. Если нужно ограничить только одну конфу — узнай `chat_id` и вставь в `TARGET_CHAT_ID`

## Как узнать chat_id группы

Добавь бота в группу и напиши любое сообщение.
Открой: `https://api.telegram.org/bot<ТОЙ_ТОКЕН>/getUpdates`
Найди поле `"chat": {"id": -100XXXXXXXXX}` — это и есть chat_id.

## Запуск локально

```bash
pip install -r requirements.txt
python bot.py
```

## Запуск на сервере (systemd)

```bash
# Скопируй файлы на сервер
scp -r mymeat_bot/ user@server:/home/www/

# Создай venv и установи зависимости
cd /home/www/mymeat_bot
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# Установи службу
sudo cp mymeat_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mymeat_bot
sudo systemctl start mymeat_bot

# Проверь статус
sudo systemctl status mymeat_bot
```
