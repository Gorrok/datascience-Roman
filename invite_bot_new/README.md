# 🤖 Telegram Invite Tracker Bot

Бот для отслеживания вступлений в Telegram канал по инвайт-ссылкам с сохранением данных в Google Sheets.

## 📋 Возможности

- ✅ Отслеживание запросов на вступление в канал
- ✅ Сохранение информации о пользователях в Google Sheets
- ✅ Автоматическое обновление списка инвайт-ссылок
- ✅ Логирование всех событий
- ✅ Работа как systemd сервис с автозапуском
- ✅ Автоматический перезапуск при сбоях

## 📁 Структура проекта

```
invite_bot_new/
├── invite_tracker.py           # Основной файл бота
├── requirements.txt            # Python зависимости
├── invitebot.service          # Systemd сервис
├── credentials.json           # Google Sheets API credentials (не включен)
├── env.example                # Пример конфигурации
├── start_bot.sh              # Скрипт запуска (альтернатива systemd)
├── stop_bot.sh               # Скрипт остановки
├── check_status.sh           # Проверка статуса
├── create_deploy_archive.sh  # Создание архива для деплоя
└── README.md                 # Эта инструкция
```

## 🚀 Установка на Beget (или любой Linux сервер)

### 1. Подготовка

#### 1.1. Создание Telegram бота
1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота командой `/newbot`
3. Сохраните токен бота (например: `7528438846:AAGoNM6J-sZCIZJyEt2hH87akeqLdm_9QJo`)

#### 1.2. Получение ID канала
1. Добавьте [@username_to_id_bot](https://t.me/username_to_id_bot) в ваш канал
2. Отправьте любое сообщение в канал
3. Бот пришлет ID канала (например: `-1002207284486`)
4. Удалите бота из канала

#### 1.3. Настройка Google Sheets API
1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект
3. Включите Google Sheets API и Google Drive API
4. Создайте Service Account
5. Создайте ключ (JSON) и скачайте файл `credentials.json`
6. Создайте Google Sheets таблицу с названием `TelegramInviteTracking`
7. Создайте два листа: `Members` и `Links`
8. Предоставьте доступ к таблице email из credentials.json (Editor)

### 2. Подключение к серверу Beget

#### Вариант A: Через SSH (терминал)

```bash
# Подключитесь к серверу
ssh your_username@your_host.beget.tech

# Введите пароль когда попросят
```

#### Вариант B: Через expect скрипт (автоматический)

Отредактируйте файл `deploy_beget.exp`:
```bash
set beget_user "your_username"
set beget_host "your_host.beget.tech"
set beget_password "your_password"
```

Запустите:
```bash
./deploy_beget.exp
```

### 3. Установка на сервере

#### 3.1. Создание директории
```bash
mkdir -p ~/invite_bot
cd ~/invite_bot
```

#### 3.2. Загрузка файлов

**Вариант A: Через SCP**
```bash
# На локальной машине
scp invite_tracker.py your_username@your_host.beget.tech:~/invite_bot/
scp requirements.txt your_username@your_host.beget.tech:~/invite_bot/
scp credentials.json your_username@your_host.beget.tech:~/invite_bot/
```

**Вариант B: Через FileZilla / WinSCP**
Загрузите все файлы в папку `invite_bot`

**Вариант C: Используя архив**
```bash
# На локальной машине создайте архив
./create_deploy_archive.sh

# Загрузите архив на сервер
scp invite_bot_deploy_*.tar.gz your_username@your_host.beget.tech:~/

# На сервере распакуйте
cd ~/invite_bot
tar -xzf ~/invite_bot_deploy_*.tar.gz
```

#### 3.3. Настройка бота

Отредактируйте файл `invite_tracker.py`, замените:
```python
TELEGRAM_BOT_TOKEN = 'ВАШ_ТОКЕН_БОТА'
CHANNEL_USERNAME = ВАШ_ID_КАНАЛА  # например: -1002207284486
SPREADSHEET_NAME = 'TelegramInviteTracking'
```

#### 3.4. Создание виртуального окружения
```bash
cd ~/invite_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3.5. Проверка работы (тестовый запуск)
```bash
python3 invite_tracker.py
```

Если все работает, нажмите `Ctrl+C` для остановки.

### 4. Настройка systemd сервиса (автозапуск)

#### 4.1. Редактирование сервис-файла

Отредактируйте `invitebot.service`, замените пути:
```ini
WorkingDirectory=/root/invite_bot  # <- ваш путь
ExecStart=/root/invite_bot/venv/bin/python /root/invite_bot/invite_tracker.py
```

Если не root пользователь:
```ini
User=your_username  # <- ваше имя пользователя
WorkingDirectory=/home/your_username/invite_bot
ExecStart=/home/your_username/invite_bot/venv/bin/python /home/your_username/invite_bot/invite_tracker.py
```

#### 4.2. Установка сервиса
```bash
# Скопировать файл сервиса
sudo cp invitebot.service /etc/systemd/system/

# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить автозапуск
sudo systemctl enable invitebot.service

# Запустить сервис
sudo systemctl start invitebot.service
```

#### 4.3. Проверка статуса
```bash
# Статус сервиса
sudo systemctl status invitebot.service

# Логи сервиса
sudo journalctl -u invitebot.service -f

# Последние 50 строк логов
sudo journalctl -u invitebot.service -n 50
```

## 🔧 Управление ботом

### Через systemd сервис (рекомендуется)

```bash
# Запуск
sudo systemctl start invitebot.service

# Остановка
sudo systemctl stop invitebot.service

# Перезапуск
sudo systemctl restart invitebot.service

# Статус
sudo systemctl status invitebot.service

# Логи в реальном времени
sudo journalctl -u invitebot.service -f
```

### Через shell скрипты (альтернатива)

```bash
# Дать права на выполнение
chmod +x *.sh

# Запуск
./start_bot.sh

# Остановка
./stop_bot.sh

# Проверка статуса
./check_status.sh
```

## 📊 Структура данных в Google Sheets

### Лист "Members"
| User ID | Link Name | Join Date |
|---------|-----------|-----------|
| 123456 | VIP ссылка | 2026-02-19 15:30:00 |
| 789012 | Акция | 2026-02-19 16:45:00 |

### Лист "Links"
| Link Name | Invite Link | Created Date |
|-----------|-------------|--------------|
| VIP ссылка | https://t.me/+abc... | 2026-02-19 10:00:00 |
| Акция | https://t.me/+xyz... | 2026-02-19 11:00:00 |

## 🔍 Диагностика проблем

### Бот не запускается

```bash
# Проверить логи
sudo journalctl -u invitebot.service -n 100

# Проверить Python
python3 --version

# Проверить виртуальное окружение
source venv/bin/activate
python -c "import telegram, gspread; print('OK')"
```

### Ошибки доступа к Google Sheets

1. Проверьте, что файл `credentials.json` существует
2. Проверьте права доступа к таблице (Editor для email из credentials)
3. Проверьте название таблицы в коде
4. Проверьте, что созданы листы "Members" и "Links"

### Бот не получает события

1. Проверьте, что бот добавлен в канал как администратор
2. Проверьте права бота: "Approve new members"
3. Проверьте, что в канале включен режим "Approve new members"
4. Проверьте правильность CHANNEL_ID (должен быть с минусом и -100)

## ⚙️ Настройка канала

1. Зайдите в настройки канала
2. Перейдите в "Manage Channel" → "Administrators"
3. Добавьте вашего бота
4. Дайте права: "Invite Users via Link" и "Approve New Members"
5. В настройках канала включите "Approve New Members"

## 🔐 Безопасность

⚠️ **ВАЖНО:**
- Не коммитьте `credentials.json` в git
- Не коммитьте токен бота в git
- Храните пароль от сервера в безопасности
- Регулярно проверяйте логи на наличие ошибок

## 📝 Логи

Логи хранятся:
- **systemd**: `sudo journalctl -u invitebot.service`
- **shell скрипты**: `logs/bot_output.log` и `logs/bot.log`

## 🆘 Поддержка

При проблемах проверьте:
1. ✅ Токен бота правильный
2. ✅ ID канала правильный
3. ✅ Бот добавлен в канал как администратор
4. ✅ credentials.json существует и правильный
5. ✅ Таблица Google Sheets существует
6. ✅ Service account имеет доступ к таблице
7. ✅ Листы "Members" и "Links" созданы
8. ✅ Виртуальное окружение активировано
9. ✅ Все зависимости установлены

## 🔄 Обновление бота

```bash
# Остановить бота
sudo systemctl stop invitebot.service

# Обновить код
cd ~/invite_bot
# Загрузите новый invite_tracker.py

# Перезапустить
sudo systemctl start invitebot.service

# Проверить статус
sudo systemctl status invitebot.service
```

## 📦 Бэкап

Регулярно делайте бэкап:
```bash
cd ~
tar -czf invite_bot_backup_$(date +%Y%m%d).tar.gz invite_bot/
```

## 🎯 Полезные команды

```bash
# Проверка процессов
ps aux | grep python

# Проверка портов
netstat -tulpn | grep python

# Дисковое пространство
df -h

# Память
free -h

# Время работы
uptime
```

---

**Автор:** Roman Muhachev  
**Версия:** 2.0  
**Дата:** 2026-02-19
