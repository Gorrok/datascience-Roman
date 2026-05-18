# 🤖 Job Vacancy Agent

Автоматический агент для поиска подходящих IT вакансий в Telegram каналах с использованием **Hermes AI** (через Ollama).

## 🎯 Возможности

- 📥 **Автоматический мониторинг** Telegram каналов с вакансиями
- 🤖 **AI-анализ** вакансий через Hermes AI (локально, через Ollama)
- 🎯 **Умная фильтрация** по вашим навыкам, опыту и требованиям
- 📊 **Оценка релевантности** каждой вакансии (0-100%)
- 📨 **Автоматические отчеты** в Telegram раз в N дней
- 🔄 **Работает в фоне** на вашем сервере 24/7

## 🏗️ Архитектура

```
Telegram каналы → Parser → Detector → Database
                                         ↓
                                    Ollama AI (Hermes) → Analyzer
                                         ↓
                                    Filtered Vacancies
                                         ↓
                                    Scheduler → Report Bot → You
```

## 📋 Требования

### Системные требования

**Минимум:**
- Ubuntu 22.04+ / Debian 11+
- 8 GB RAM
- 10 GB свободного места
- Python 3.11+

**Рекомендуется:**
- 16 GB RAM
- GPU с 8+ GB VRAM (для ускорения Ollama)
- 20 GB свободного места

### Необходимые ключи

1. **Telegram API** (для парсинга каналов)
   - Получить: https://my.telegram.org/apps
   - Нужны: `API_ID` и `API_HASH`

2. **Telegram Bot** (для отправки отчетов)
   - Создать: @BotFather в Telegram
   - Нужен: `BOT_TOKEN`

3. **Ваш Telegram ID**
   - Узнать: @userinfobot в Telegram

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
cd ~/
git clone <your-repo-url>
cd datascience-Roman/ai-agents/job-vacancy-agent
```

### 2. Автоматический деплой (рекомендуется)

```bash
chmod +x deploy.sh
./deploy.sh
```

Скрипт автоматически:
- ✅ Установит Python 3.11
- ✅ Установит Ollama
- ✅ Скачает модель Hermes AI
- ✅ Создаст виртуальное окружение
- ✅ Установит зависимости
- ✅ Настроит systemd сервис
- ✅ Запустит агента

### 3. Настройка конфигурации

После деплоя отредактируйте `secrets.py`:

```bash
nano secrets.py
```

Заполните свои ключи:

```python
TELEGRAM_API_ID = 12345678
TELEGRAM_API_HASH = "your_api_hash"
TELEGRAM_BOT_TOKEN = "1234567890:ABC..."
USER_TELEGRAM_ID = 123456789
```

### 4. Настройка фильтров

Отредактируйте `config.py` под свой профиль:

```python
# Ваши навыки
user_skills = [
    "Python",
    "FastAPI",
    "Django",
    "PostgreSQL",
    "Docker",
]

# Опыт работы
user_experience_years = 5

# Минимальная зарплата
user_min_salary = 150000  # в рублях

# Предпочитаемые локации
user_preferred_locations = [
    "Удаленно",
    "Remote",
    "Москва",
]

# Каналы для мониторинга
job_channels = [
    "python_jobs",
    "remote_jobs_russia",
    "freelance_ru",
    # добавьте свои
]
```

### 5. Тестовый запуск

```bash
python main.py --test
```

Проверит:
- ✅ Конфигурацию
- ✅ Базу данных
- ✅ Ollama
- ✅ Telegram бота

Если все OK - получите тестовое сообщение в Telegram!

## 📖 Использование

### Запуск в фоновом режиме

```bash
# Через systemd (рекомендуется)
sudo systemctl start vacancy-agent
sudo systemctl status vacancy-agent

# Или напрямую
python main.py
```

### Разовые задачи

```bash
# Разовый парсинг каналов
python main.py --once parse

# Разовая отправка отчета
python main.py --once report
```

### Мониторинг

```bash
# Логи systemd
sudo journalctl -u vacancy-agent -f

# Логи приложения
tail -f vacancy_agent.log

# Статус сервиса
sudo systemctl status vacancy-agent
```

### Управление сервисом

```bash
# Остановить
sudo systemctl stop vacancy-agent

# Перезапустить
sudo systemctl restart vacancy-agent

# Отключить автозапуск
sudo systemctl disable vacancy-agent
```

## ⚙️ Конфигурация

### Расписание

По умолчанию:
- **Парсинг каналов:** каждые 4 часа
- **Отправка отчетов:** каждые 3 дня в 10:00

Изменить в `config.py`:

```python
parse_interval_hours = 4  # Каждые N часов
report_interval_days = 3  # Каждые N дней
report_time_hour = 10     # В какое время (0-23)
```

### Фильтрация

Настройка порога релевантности:

```python
min_relevance_score = 0.6  # 0-1 (0.6 = 60%)
```

Чем выше порог, тем строже фильтрация.

### Ollama

Если Ollama на другом сервере:

```python
# В secrets.py
OLLAMA_URL = "http://192.168.1.100:11434"
OLLAMA_MODEL = "hermes3:8b"  # или другая модель
```

## 📊 Как это работает

### 1. Парсинг каналов

Каждые N часов агент:
- Подключается к Telegram через Pyrogram
- Читает последние ~50 сообщений из каждого канала
- Определяет какие сообщения являются вакансиями (по ключевым словам)
- Сохраняет новые вакансии в БД

### 2. AI-анализ

Для каждой новой вакансии:
- Отправляет текст в Ollama (Hermes AI)
- AI извлекает: должность, требования, зарплату, локацию и т.д.
- Вычисляет релевантность на основе вашего профиля:
  - Совпадение навыков (40%)
  - Опыт работы (20%)
  - Зарплата (25%)
  - Локация (15%)
- Сохраняет результат с оценкой 0-1

### 3. Отправка отчетов

Раз в N дней:
- Собирает все релевантные вакансии (score > 0.6)
- Форматирует их в красивые сообщения
- Отправляет вам в Telegram через бота
- Отмечает вакансии как отправленные

## 🧪 Примеры

### Пример отчета в Telegram

```
🎯 Senior Python Developer

🏢 Компания: TechCorp
💰 Зарплата: 200000-300000 RUB
📍 Локация: Удаленно, remote

📝 Разработка backend на Python/FastAPI для ML проектов

⭐️ Релевантность: 85%

Подходит потому что:
  ✓ Совпадение навыков: python, fastapi, docker
  ✓ Опыт подходит: требуется 4, есть 5
  ✓ Зарплата подходит: до 300000

📢 Канал: @python_jobs

🔗 Открыть в Telegram
────────────────────────────────────────
```

### Пример настройки для Junior

```python
# config.py
user_skills = ["Python", "Django", "Git"]
user_experience_years = 1
user_min_salary = 80000
exclude_keywords = ["senior", "lead", "10+ лет"]
min_relevance_score = 0.5  # Более мягкая фильтрация
```

### Пример настройки для Senior

```python
# config.py
user_skills = ["Python", "FastAPI", "PostgreSQL", "Docker", "Kubernetes", "AWS"]
user_experience_years = 7
user_min_salary = 250000
exclude_keywords = ["junior", "стажер", "до 3 лет"]
min_relevance_score = 0.7  # Строгая фильтрация
```

## 🔧 Troubleshooting

### Ollama не запускается

```bash
# Проверить статус
sudo systemctl status ollama

# Перезапустить
sudo systemctl restart ollama

# Проверить доступность
curl http://localhost:11434/api/tags
```

### Модель не найдена

```bash
# Список установленных моделей
ollama list

# Установить Hermes
ollama pull hermes3:8b

# Альтернативные модели
ollama pull llama3.2:8b
ollama pull mistral-nemo:12b
```

### Telegram бот не отправляет сообщения

1. Проверьте токен бота в `secrets.py`
2. Убедитесь что вы написали боту `/start`
3. Проверьте ваш Telegram ID:
   ```bash
   # Отправьте /start боту @userinfobot
   ```

### Не находит вакансии

1. Проверьте что каналы публичные
2. Убедитесь что вы подписаны на каналы
3. Проверьте username каналов в `config.py`:
   ```python
   job_channels = [
       "python_jobs",  # Без @
       "remote_jobs",
   ]
   ```

### Все вакансии нерелевантные

Попробуйте:
- Снизить `min_relevance_score` до 0.5
- Расширить список `user_skills`
- Убрать `exclude_keywords`
- Проверить логи: `tail -f vacancy_agent.log`

## 📝 Структура проекта

```
job-vacancy-agent/
├── main.py                 # Точка входа
├── config.py              # Конфигурация
├── secrets.py             # Ключи (не коммитится)
├── requirements.txt       # Зависимости
├── deploy.sh              # Скрипт деплоя
├── database/
│   ├── models.py          # SQLAlchemy модели
│   └── database.py        # Подключение к БД
├── parsers/
│   ├── telegram_parser.py # Парсинг Telegram
│   └── vacancy_extractor.py # Детектор вакансий
├── ai/
│   ├── ollama_client.py   # Клиент Ollama
│   └── vacancy_analyzer.py # Анализ вакансий
├── bot/
│   └── telegram_bot.py    # Отправка отчетов
└── scheduler/
    └── job_scheduler.py   # Планировщик задач
```

## 🤝 Вклад

Это личный проект, но предложения приветствуются!

## 📄 Лицензия

MIT

## 🙋 Автор

Roman Muhachev
- GitHub: [@romanmuhachev](https://github.com/romanmuhachev)
- Telegram: @your_username

---

**Удачи в поиске работы! 🚀**
