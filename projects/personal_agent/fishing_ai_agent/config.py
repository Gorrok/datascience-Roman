import os

# --- УДАЛЯЕМ СТАРЫЙ СПОСОБ ЗАГРУЗКИ ---
# --- ВМЕСТО НЕГО ИМПОРТИРУЕМ НАПРЯМУЮ ---
try:
    from secrets import (
        YOUTUBE_API_KEY,
        TELEGRAM_API_ID,
        TELEGRAM_API_HASH,
        OPENAI_API_KEY,
        GITHUB_TOKEN,
        GITHUB_REPO
    )
    print("--- Секретные ключи успешно импортированы из secrets.py ---")
except ImportError:
    print("ОШИБКА: Файл secrets.py не найден. Пожалуйста, создайте его.")
    YOUTUBE_API_KEY = None
    TELEGRAM_API_ID = None
    TELEGRAM_API_HASH = None
    OPENAI_API_KEY = None
    GITHUB_TOKEN = None
    GITHUB_REPO = None

# --- Остальные настройки остаются прежними ---

# Database
db_path = os.path.join(os.path.dirname(__file__), "fishing_data.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

# Scraping settings
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
REQUEST_DELAY = int(os.getenv("REQUEST_DELAY", 2))

# Prompts
try:
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.md')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        FISHING_AI_AGENT_PROMPT = f.read()
except FileNotFoundError:
    print("Warning: prompt.md not found. Using a default prompt.")
    FISHING_AI_AGENT_PROMPT = "You are a helpful fishing assistant."