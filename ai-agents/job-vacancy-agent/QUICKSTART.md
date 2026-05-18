# 🚀 Быстрый старт за 5 минут

## Шаг 1: Получить ключи (5 минут)

### 1.1 Telegram API
1. Откройте https://my.telegram.org/apps
2. Залогиньтесь
3. Создайте приложение
4. Скопируйте `api_id` и `api_hash`

### 1.2 Создать бота
1. Откройте @BotFather в Telegram
2. Отправьте `/newbot`
3. Придумайте имя и username
4. Скопируйте токен бота

### 1.3 Узнать свой ID
1. Откройте @userinfobot в Telegram
2. Отправьте `/start`
3. Скопируйте ваш ID

## Шаг 2: Установка (1 команда)

```bash
cd ~/datascience-Roman/ai-agents/job-vacancy-agent
./deploy.sh
```

Скрипт все сделает автоматически!

## Шаг 3: Настройка (2 минуты)

```bash
nano secrets.py
```

Вставьте свои ключи:

```python
TELEGRAM_API_ID = 12345678
TELEGRAM_API_HASH = "abcdef123456"
TELEGRAM_BOT_TOKEN = "1234567890:ABC-DEF..."
USER_TELEGRAM_ID = 123456789
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

## Шаг 4: Настройка профиля (3 минуты)

```bash
nano config.py
```

Измените под себя:

```python
# Ваши навыки
user_skills = [
    "Python",      # Ваши технологии
    "FastAPI",
    "PostgreSQL",
]

# Опыт
user_experience_years = 5

# Минимальная зарплата (в рублях или $)
user_min_salary = 150000

# Каналы для мониторинга
job_channels = [
    "python_jobs",
    "remote_jobs_russia",
    # Добавьте свои каналы
]
```

## Шаг 5: Тест

```bash
python main.py --test
```

Если все ✓ - вы получите тестовое сообщение в Telegram!

## Шаг 6: Запуск

```bash
sudo systemctl start vacancy-agent
sudo systemctl status vacancy-agent
```

## 🎉 Готово!

Агент работает в фоне и будет:
- ✅ Парсить каналы каждые 4 часа
- ✅ Анализировать вакансии через AI
- ✅ Отправлять отчеты каждые 3 дня

## 📊 Мониторинг

```bash
# Логи в реальном времени
sudo journalctl -u vacancy-agent -f

# Статус
sudo systemctl status vacancy-agent
```

## 🔧 Проблемы?

### Ollama не работает
```bash
sudo systemctl restart ollama
ollama pull hermes3:8b
```

### Бот не отправляет
```bash
# Напишите боту /start в Telegram
# Проверьте что USER_TELEGRAM_ID правильный
```

### Не находит вакансии
```bash
# Проверьте что каналы публичные
# Убедитесь что подписаны на них
# Снизьте min_relevance_score в config.py
```

---

**Нужна помощь?** Смотрите полный [README.md](README.md)
