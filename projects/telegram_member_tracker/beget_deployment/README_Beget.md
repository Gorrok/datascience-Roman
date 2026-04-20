# 🚀 Развертывание Telegram Member Tracker на Beget

## 📋 Что в папке:

```
beget_deployment/
├── invite_tracker.py      # 🏠 Основной файл бота
├── credentials1.json      # 🔐 Ключи Google API
├── .env                   # ⚙️ Настройки
├── start_bot.sh          # ▶️ Скрипт запуска
├── stop_bot.sh           # ⏹️ Скрипт остановки
└── README_Beget.md       # 📖 Эта инструкция
```

## 🛠️ Развертывание на Beget:

### 1. Загрузка файлов:
- Загрузите **всю папку** `beget_deployment` на ваш хостинг Beget
- Поместите файлы в корневую директорию сайта

### 2. Установка зависимостей:
```bash
pip3 install python-telegram-bot gspread oauth2client
```

### 3. Настройка разрешений:
```bash
chmod +x start_bot.sh stop_bot.sh
```

### 4. Запуск бота:
```bash
./start_bot.sh
```

## 🔍 Проверка работы:

### Проверить статус бота:
```bash
ps aux | grep python3
```

### Посмотреть логи:
```bash
tail -f logs/bot_output.log
```

### Остановить бота:
```bash
./stop_bot.sh
```

## 📊 Как работает бот:

1. **Отслеживает вступления** в канал по инвайт-ссылкам
2. **Сохраняет данные** в Google Sheets таблицу "ShepoitBukmekera"
3. **Лист "Members"** - информация о вступивших пользователях
4. **Лист "Links"** - список инвайт-ссылок

## ⚠️ Важно:

- **Не удаляйте** файлы `credentials1.json` и `.env`
- **Не коммитьте** эти файлы в git
- Бот должен иметь права администратора в канале
- Google Sheets таблица должна быть доступна сервисному аккаунту

## 🆘 Проблемы:

### Бот не запускается:
```bash
# Проверить логи
cat logs/bot_output.log

# Проверить Python
python3 --version

# Проверить зависимости
python3 -c "import telegram, gspread; print('OK')"
```

### Нет записи в Google Sheets:
- Проверьте доступ к таблице
- Убедитесь, что сервисный аккаунт имеет права "Editor"
- Проверьте правильность ID таблицы

## 📞 Поддержка:

При проблемах проверьте:
1. Логи бота: `logs/bot_output.log`
2. Статус процессов: `ps aux | grep python`
3. Доступность Google Sheets API
