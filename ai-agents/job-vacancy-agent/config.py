"""
Конфигурация для Job Vacancy Agent
"""
import os
from dataclasses import dataclass, field
from typing import List

try:
    from secrets import (
        TELEGRAM_API_ID,
        TELEGRAM_API_HASH,
        TELEGRAM_BOT_TOKEN,
        USER_TELEGRAM_ID
    )
    print("✓ Секретные ключи загружены из secrets.py")
except ImportError:
    print("⚠️ ОШИБКА: Файл secrets.py не найден. Создайте его по примеру secrets.py.example")
    TELEGRAM_API_ID = None
    TELEGRAM_API_HASH = None
    TELEGRAM_BOT_TOKEN = None
    USER_TELEGRAM_ID = None


@dataclass
class Config:
    """Основная конфигурация приложения"""
    
    # Telegram API для парсинга каналов (pyrogram)
    telegram_api_id: int = TELEGRAM_API_ID
    telegram_api_hash: str = TELEGRAM_API_HASH
    telegram_session: str = "vacancy_parser"
    
    # Telegram Bot для отправки отчетов
    telegram_bot_token: str = TELEGRAM_BOT_TOKEN
    user_telegram_id: int = USER_TELEGRAM_ID
    
    # Ollama настройки
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "hermes3:8b")
    ollama_timeout: int = 120  # секунды
    
    # Каналы для мониторинга (замените на свои)
    job_channels: List[str] = field(default_factory=lambda: [
        "python_jobs",
        "remote_jobs_russia",
        "freelance_ru",
        "digital_vacancies",
        "it_jobs_russia",
        "job_dev_python",
        # Добавьте свои каналы
    ])
    
    # Фильтрация вакансий
    min_relevance_score: float = 0.6  # Минимальный порог релевантности (0-1)
    max_messages_per_channel: int = 50  # Сколько последних сообщений парсить
    
    # Расписание
    parse_interval_hours: int = 4  # Парсить каждые N часов
    report_interval_days: int = 3  # Отправлять отчет раз в N дней
    report_time_hour: int = 10  # В какое время отправлять (0-23)
    
    # База данных
    database_url: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), 'vacancies.db')}"
    )
    
    # Профиль пользователя для фильтрации
    user_skills: List[str] = field(default_factory=lambda: [
        "Python",
        "FastAPI",
        "Django",
        "PostgreSQL",
        "Docker",
        "REST API",
    ])
    
    user_experience_years: int = 5
    user_min_salary: int = 150000  # Минимальная зарплата в рублях (или $3000)
    user_preferred_locations: List[str] = field(default_factory=lambda: [
        "Удаленно",
        "Remote",
        "Москва",
    ])
    
    # Исключающие ключевые слова (если они есть - вакансия отклоняется)
    exclude_keywords: List[str] = field(default_factory=lambda: [
        "стажер",
        "intern",
        "trainee",
        "junior",
        "без опыта",
    ])
    
    # Логирование
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = "vacancy_agent.log"


# Глобальный экземпляр конфигурации
config = Config()


def validate_config() -> bool:
    """Проверяет что все необходимые параметры заданы"""
    errors = []
    
    if not config.telegram_api_id:
        errors.append("TELEGRAM_API_ID не задан в secrets.py")
    if not config.telegram_api_hash:
        errors.append("TELEGRAM_API_HASH не задан в secrets.py")
    if not config.telegram_bot_token:
        errors.append("TELEGRAM_BOT_TOKEN не задан в secrets.py")
    if not config.user_telegram_id:
        errors.append("USER_TELEGRAM_ID не задан в secrets.py")
    
    if errors:
        print("\n❌ Ошибки конфигурации:")
        for error in errors:
            print(f"  - {error}")
        print("\nСоздайте файл secrets.py по примеру secrets.py.example\n")
        return False
    
    return True
