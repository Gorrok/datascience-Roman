# 📦 Invite Bot - Содержимое проекта

## 🎯 Основные файлы для деплоя

### Обязательные файлы:
1. **invite_tracker.py** - Основной код бота (2.6 KB)
2. **requirements.txt** - Python зависимости (150 B)
3. **invitebot.service** - Systemd сервис файл (279 B)
4. **credentials.json** - ⚠️ НЕ ВКЛЮЧЕН - добавьте свой!

### Вспомогательные скрипты:
5. **start_bot.sh** - Альтернативный запуск (без systemd)
6. **stop_bot.sh** - Остановка бота
7. **check_status.sh** - Проверка статуса

### Документация:
8. **README.md** - Полная инструкция (11 KB)
9. **QUICKSTART.md** - Быстрый старт (2.3 KB)

### Дополнительно:
10. **env.example** - Пример конфигурации
11. **deploy_beget.exp** - Автоматический деплой через expect
12. **create_deploy_archive.sh** - Создание архива
13. **.gitignore** - Исключения для git

## 🔧 Что нужно настроить перед деплоем:

### 1. В файле `invite_tracker.py` (строки 15-17):
```python
TELEGRAM_BOT_TOKEN = '7528438846:AAGoNM6J-sZCIZJyEt2hH87akeqLdm_9QJo'  # ← Замените
CHANNEL_USERNAME = -1002207284486  # ← Замените
SPREADSHEET_NAME = 'TelegramInviteTracking'  # ← Замените при необходимости
```

### 2. В файле `invitebot.service` (строки 7-9):
```ini
User=root  # ← Замените на ваше имя пользователя
WorkingDirectory=/root/invite_bot  # ← Замените на ваш путь
ExecStart=/root/invite_bot/venv/bin/python /root/invite_bot/invite_tracker.py  # ← Замените
```

### 3. Добавьте файл `credentials.json`:
- Получите из Google Cloud Console
- Поместите рядом с invite_tracker.py

## 📋 Google Sheets структура:

Создайте таблицу с названием: **TelegramInviteTracking**

### Лист "Members" (заголовки):
| User ID | Link Name | Join Date |
|---------|-----------|-----------|

### Лист "Links" (заголовки):
| Link Name | Invite Link | Created Date |
|-----------|-------------|--------------|

## 🚀 Быстрый деплой:

```bash
# 1. Подключение к серверу
ssh user@host.beget.tech

# 2. Создание директории
mkdir -p ~/invite_bot && cd ~/invite_bot

# 3. Загрузка файлов (SCP/FTP)
# Загрузите: invite_tracker.py, requirements.txt, invitebot.service, credentials.json

# 4. Установка
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Настройка systemd
sudo cp invitebot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable invitebot.service
sudo systemctl start invitebot.service

# 6. Проверка
sudo systemctl status invitebot.service
```

## ✅ Проверка работы:

```bash
# Статус сервиса
sudo systemctl status invitebot.service

# Логи в реальном времени
sudo journalctl -u invitebot.service -f

# Последние 50 строк
sudo journalctl -u invitebot.service -n 50
```

## 🔄 Управление:

```bash
sudo systemctl start invitebot.service    # Запуск
sudo systemctl stop invitebot.service     # Остановка
sudo systemctl restart invitebot.service  # Перезапуск
sudo systemctl status invitebot.service   # Статус
```

## 📞 Что делать если не работает:

1. Проверьте логи: `sudo journalctl -u invitebot.service -n 100`
2. Проверьте токен бота и ID канала
3. Проверьте credentials.json
4. Проверьте доступ к Google Sheets
5. Проверьте, что бот администратор в канале
6. Проверьте виртуальное окружение: `source venv/bin/activate`

---

**Создано:** 2026-02-19  
**Версия:** 2.0  
**Тип:** Production Ready
