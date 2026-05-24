import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./couples_planner.db"
    )
    
    # Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Users (только двое)
    USER_1_ID: int = int(os.getenv("USER_1_ID", 0))
    USER_1_NAME: str = os.getenv("USER_1_NAME", "User1")
    USER_2_ID: int = int(os.getenv("USER_2_ID", 0))
    USER_2_NAME: str = os.getenv("USER_2_NAME", "User2")
    
    # Mini App
    MINI_APP_URL: str = os.getenv("MINI_APP_URL", "")

settings = Settings()
