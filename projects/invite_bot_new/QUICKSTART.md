# Быстрый старт

## SSH на сервер

```bash
ssh root@93.189.230.247
# пароль: GG4(w~Fva9Xk
```

---

## Проверить статус всех ботов

```bash
systemctl status invitebot mybot bot2 reportbot --no-pager | grep -E 'service -|Active:|Main PID'
```

---

## Перезапустить бота

```bash
# Один бот
systemctl restart invitebot.service

# Все боты
systemctl restart invitebot.service mybot.service bot2.service reportbot.service

# Проверить что поднялись
sleep 3 && systemctl status invitebot mybot bot2 --no-pager | grep Active
```

---

## Посмотреть логи

```bash
# Следить в реальном времени
journalctl -u invitebot.service -f

# Последние записи
journalctl -u mybot.service -n 30 --no-pager

# Только ошибки
journalctl -u bot2.service -p err --no-pager -n 20
```

---

## Редактировать код бота

```bash
# invitebot (Mickey)
nano /bot/invite_tracker/bot.py
systemctl restart invitebot.service

# mybot (основной)
nano /root/Invite_tracker/bot.py
systemctl restart mybot.service

# bot2 (Shepoit)
nano /home/telegram-bot/bot2/bot.py
systemctl restart bot2.service
```

---

## Бот упал и не поднимается

```bash
# Посмотреть причину
journalctl -u invitebot.service -n 50 --no-pager

# Проверить .env
cat /bot/invite_tracker/.env

# Запустить вручную для отладки
cd /bot/invite_tracker
source venv/bin/activate
python bot.py
```

---

## Обновить зависимости

```bash
cd /bot/invite_tracker
source venv/bin/activate
pip install -r requirements.txt --upgrade
systemctl restart invitebot.service
```

---

## Расположение файлов

| Бот | Код | .env | Сервис |
|-----|-----|------|--------|
| invitebot (Mickey) | `/bot/invite_tracker/bot.py` | `/bot/invite_tracker/.env` | `invitebot.service` |
| mybot (основной) | `/root/Invite_tracker/bot.py` | `/root/Invite_tracker/.env` | `mybot.service` |
| bot2 (Shepoit) | `/home/telegram-bot/bot2/bot.py` | `/home/telegram-bot/bot2/.env` | `bot2.service` |
| reportbot | `/bot/report_bot/bot.py` | — | `reportbot.service` |
