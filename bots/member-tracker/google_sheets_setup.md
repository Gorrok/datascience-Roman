# Настройка Google Sheets API для бота

## Шаг 1: Создание проекта в Google Cloud Console

1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Нажмите "Create Project" (или "Выбрать проект" → "Новый проект")
3. Введите название проекта (например, "Telegram Member Tracker")
4. Нажмите "Create"

## Шаг 2: Включение Google Sheets API

1. В боковом меню выберите "APIs & Services" → "Library"
2. Найдите "Google Sheets API"
3. Нажмите на него и затем "Enable"

## Шаг 3: Создание сервисного аккаунта

1. В боковом меню выберите "APIs & Services" → "Credentials"
2. Нажмите "Create credentials" → "Service account"
3. Заполните форму:
   - **Service account name**: `telegram-member-tracker`
   - **Service account ID**: оставьте по умолчанию
   - **Description**: `Service account for Telegram Member Tracker bot`
4. Нажмите "Create and continue"
5. Пропустите следующий шаг (роли) - нажмите "Done"

## Шаг 4: Создание ключа API

1. В списке сервисных аккаунтов найдите созданный аккаунт
2. Нажмите на его email
3. Перейдите во вкладку "Keys"
4. Нажмите "Add Key" → "Create new key"
5. Выберите тип "JSON"
6. Нажмите "Create"

Файл `credentials.json` автоматически скачается. Переименуйте его если нужно и поместите в папку с ботом.

## Шаг 5: Создание Google Sheets таблицы

1. Перейдите на [Google Sheets](https://sheets.google.com/)
2. Создайте новую таблицу
3. Назовите её (например, "Telegram Members Tracker")
4. Скопируйте ID таблицы из URL - это часть между `/d/` и `/edit`

Пример URL: `https://docs.google.com/spreadsheets/d/1IOqcxV7aP8eJ7Iil-XlkRGuGB6_EVVtNcQyoo111eWA/edit`

ID таблицы: `1IOqcxV7aP8eJ7Iil-XlkRGuGB6_EVVtNcQyoo111eWA`

## Шаг 6: Предоставление доступа к таблице

1. Откройте созданную Google Sheets таблицу
2. Нажмите "Share" (Поделиться)
3. В поле "Add people and groups" вставьте email сервисного аккаунта (из файла credentials.json, поле "client_email")
4. Выберите роль "Editor" (Редактор)
5. Снимите галочку "Notify people" (если не хотите получать уведомления)
6. Нажмите "Share"

## Шаг 7: Настройка .env файла

Создайте файл `.env` на основе `config_example.txt`:

```env
# Telegram Bot API
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь

# Каналы для отслеживания
MONITORED_CHANNELS=@your_channel

# Google Sheets API
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=1IOqcxV7aP8eJ7Iil-XlkRGuGB6_EVVtNcQyoo111eWA
GOOGLE_SHEETS_MEMBERS_SHEET=members
GOOGLE_SHEETS_ACTIVITY_SHEET=activity

# Логирование
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

## Проверка настройки

Запустите тест:

```bash
python test_bot.py
```

Если все настроено правильно, вы увидите:
- ✅ Конфигурация найдена
- ✅ Подключение к Google Sheets успешно
- ✅ Токен бота найден

## Устранение проблем

### "The caller does not have permission"
- Проверьте, что сервисный аккаунт имеет доступ "Editor" к таблице
- Убедитесь, что ID таблицы указан правильно

### "File credentials.json not found"
- Проверьте, что файл `credentials.json` находится в папке с ботом
- Убедитесь, что путь указан правильно в `.env`

### "Invalid credentials"
- Скачайте новый ключ API для сервисного аккаунта
- Проверьте, что JSON файл не поврежден

### "Google Sheets API has not been used"
- Убедитесь, что Google Sheets API включен в проекте
- Подождите 5-10 минут после включения API

## Полезные ссылки

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [gspread Documentation](https://gspread.readthedocs.io/)
