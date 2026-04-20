# Changelog

## 2026-04-18

### Фикс: вступления через инвайт-ссылку записывались как "direct"

**Проблема**  
В функции `handle_member_update` все боты при вступлении пользователя без предшествующего join request писали `'direct'` в колонку `link_name`, даже если человек пришёл по инвайт-ссылке.

**Причина**  
Объект `ChatMemberUpdated` от Telegram содержит поле `invite_link`, но код его игнорировал и всегда использовал хардкод `'direct'`.

**Что было:**
```python
members_sheet.append_row([user_id, 'direct', join_date, 'subscribe', ...])
```

**Что стало:**
```python
invite_link_obj = getattr(result, 'invite_link', None)
link_name = 'direct'
if invite_link_obj:
    link_name = invite_link_obj.name or invite_link_obj.invite_link or 'direct'
members_sheet.append_row([user_id, link_name, join_date, 'subscribe', ...])
```

**Исправлено в файлах:**
- `/bot/invite_tracker/bot.py` (invitebot / Mickey)
- `/root/Invite_tracker/bot.py` (mybot)
- `/home/telegram-bot/bot2/bot.py` (bot2 / Shepoit)

Бэкапы до правки: `bot.py.bak_direct_fix` в каждой директории.

**Когда `direct` остаётся корректным значением:**  
Когда пользователь реально вступил без ссылки — через поиск, был добавлен администратором, или Telegram не передал `invite_link` в событии.

**Исторические данные:**  
Записи с `direct` до 2026-04-18 восстановить невозможно — Telegram не хранит историю «кто по какой ссылке вступил».

---

## 2026-03-28

Обновление кода bot2 — бэкап `bot.py.backup.20260328_152803`.

## 2026-03-13

Правки на сервере, бэкапы `bot.py.backup.1773516431`.

## 2026-02-19

Первичный деплой Mickey-бота (`invitebot.service`).
