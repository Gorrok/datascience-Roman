# Invite Tracker Bots

Боты для трекинга инвайт-ссылок и вступлений в Telegram-каналы/группы. Пишут данные в Google Sheets.

## Сервер

```
Host:     93.189.230.247
User:     root
Password: GG4(w~Fva9Xk
```

---

## Архитектура: 4 бота

| Сервис | Канал | Google Sheet | Путь на сервере | Особенности |
|--------|-------|-------------|-----------------|-------------|
| `invitebot.service` | Mickey (-1001589094262) | `Invitetrackermickey` | `/bot/invite_tracker/` | Трекинг + реакции |
| `mybot.service` | Main (-1002207284486) | `TelegramInviteTracking` | `/root/Invite_tracker/` | AUTO_APPROVE=true |
| `bot2.service` | Shepoit (-1001225013297) | `ShepoitBukmekera` | `/home/telegram-bot/bot2/` | user=telegram-bot |
| `reportbot.service` | — | — | `/bot/report_bot/` | Отправляет отчёты в чат -4256699399 |

---

## Структура Google Sheets

Каждая таблица имеет два листа:

### Лист `Members`
| user_id | link_name | join_date | status | leave_date | days | joined_group | sent_message | set_reaction |
|---------|-----------|-----------|--------|------------|------|--------------|--------------|--------------|
| 123456 | Ссылка-1 | 2026-04-18 10:00:00 | subscribe | | | 0 | 0 | 0 |

**Статусы**: `pending` → `subscribe` → `unsubscribe`

### Лист `Links`
| name | url | created_at |
|------|-----|-----------|
| Ссылка-1 | https://t.me/+xxx | 2026-01-01 |

---

## Как работает трекинг

```
Пользователь нажимает инвайт-ссылку
         ↓
[Если группа требует одобрения]
  → handle_join_request → записывает user_id + link_name + "pending"
  → handle_member_update (is_join) → обновляет статус на "subscribe"

[Если группа НЕ требует одобрения]
  → handle_member_update (is_join) → записывает user_id + link_name + "subscribe"
     └─ берёт link_name из result.invite_link (поле ChatMemberUpdated)
     └─ если ссылки нет — пишет "direct" (реально прямое вступление)

Пользователь выходит
  → handle_member_update (is_leave) → статус "unsubscribe", дата выхода, кол-во дней
```

---

## Управление сервисами

```bash
# Статус всех ботов
systemctl status invitebot mybot bot2 reportbot

# Перезапуск одного
systemctl restart invitebot.service

# Перезапуск всех
systemctl restart invitebot.service mybot.service bot2.service reportbot.service

# Логи в реальном времени
journalctl -u invitebot.service -f

# Последние 50 строк логов
journalctl -u mybot.service -n 50 --no-pager
```

---

## Деплой нового бота (с нуля)

### 1. На сервере — создать директорию и загрузить файлы

```bash
ssh root@93.189.230.247

mkdir -p /bot/NEW_BOT_NAME
cd /bot/NEW_BOT_NAME

# Загрузить через scp (локально):
# scp bot.py credentials.json requirements.txt root@93.189.230.247:/bot/NEW_BOT_NAME/
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Создать .env файл

```bash
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН
CHANNEL_ID=-100XXXXXXXXXX
SPREADSHEET_NAME=НазваниеТаблицы
CREDENTIALS_FILE=credentials.json
UPDATE_INTERVAL_SEC=300
LOG_LEVEL=INFO
EOF
```

### 4. Создать systemd сервис

```bash
cat > /etc/systemd/system/NEWBOT.service << 'EOF'
[Unit]
Description=Invite Tracker Bot - ОПИСАНИЕ
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/bot/NEW_BOT_NAME
Environment=PATH=/bot/NEW_BOT_NAME/venv/bin
Environment=PYTHONPATH=/bot/NEW_BOT_NAME
EnvironmentFile=/bot/NEW_BOT_NAME/.env
ExecStart=/bot/NEW_BOT_NAME/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable NEWBOT.service
systemctl start NEWBOT.service
systemctl status NEWBOT.service
```

### 5. Проверить что работает

```bash
journalctl -u NEWBOT.service -n 20 --no-pager
# Должно быть: "Application started"
```

---

## Требования к боту в Telegram

- Бот добавлен в канал/группу как **администратор**
- Права бота: **Invite Users via Link** + **Manage Members**
- Если нужен трекинг join requests: включить **Approve New Members** в настройках группы
- Service account Google Sheets добавлен в таблицу как **Editor**

---

## Требования к Google Sheets

1. Создать таблицу с двумя листами: `Members` и `Links`
2. В листе `Members` — заголовки в первой строке:
   `user_id | link_name | join_date | status | leave_date | days | joined_group | sent_message | set_reaction`
3. В листе `Links` — заголовки: `name | url | created_at`
4. Дать доступ service account (email из credentials.json) — роль **Редактор**

---

## Известные проблемы и решения

| Проблема | Причина | Решение |
|---------|---------|---------|
| `RuntimeError: Cannot close a running event loop` в логах при остановке | Безвредный артефакт `nest_asyncio` при shutdown | Игнорировать, бот работает нормально |
| `409 Conflict: terminated by other getUpdates` | Запущено два экземпляра одного бота | `systemctl stop` лишнего экземпляра |
| Все вступления пишутся как `direct` | Бот не извлекает `invite_link` из `ChatMemberUpdated` | Исправлено 2026-04-18, см. CHANGELOG.md |
| Бот не записывает join requests | Бот не добавлен как admin или не включён режим одобрения | Проверить права и настройки группы |
