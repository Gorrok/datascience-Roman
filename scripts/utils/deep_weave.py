import requests
import re
from pathlib import Path

# Configuration
API_KEY = "7ec3da33da4da82035362e470a61f854fb041ba12b4befd4ce4e210d73d41479"
BASE_URL = "https://127.0.0.1:27124/vault"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "text/markdown"
}

# Universal Hubs to create
HUBS = {
    "Concepts/Telegram.md": ["Telegram", "Тг", "телеграм", "бот", "bot"],
    "Concepts/Python.md": ["Python", "питон", "скрипт", "script"],
    "Concepts/n8n.md": ["n8n", "workflow", "воркфлоу", "автоматизация"],
    "Concepts/AI.md": ["AI", "ИИ", "агент", "assistant", "openai", "gpt", "llm"],
    "Concepts/Career.md": ["работа", "вакансия", "резюме", "карьера", "работодатель", "career"],
    "Concepts/Analytics.md": ["аналитика", "анализ", "данные", "data", "analytics", "sql"]
}

def update_file(path, content):
    requests.post(f"{BASE_URL}/{path}", data=content.encode('utf-8'), headers=HEADERS, verify=False)

def get_file_content(path):
    r = requests.get(f"{BASE_URL}/{path}", headers=HEADERS, verify=False)
    return r.text if r.status_code == 200 else None

def get_all_files():
    # Since we can't easily list all files recursively via this API without knowing names,
    # I will use a list of known important paths and directories to scan.
    # For a real "deep" clean, I'd need a way to list all .md files.
    # I'll use the ones from the previous migration logs.
    return [] # Will populate with logic below

def create_hubs():
    for path, keywords in HUBS.items():
        title = Path(path).stem
        content = f"# 🏷️ Hub: {title}\n\nВсе заметки и проекты, связанные с {title}.\n\n--- \n#project #hub"
        update_file(path, content)
    print("✅ Created Concept Hubs.")

def deep_weave():
    # Known project list
    projects = [
        "telegram-analytics-saas", "superagent", "telegram_member_tracker", 
        "invite_bot_new", "personal_agent", "n8n_daily_messages", "portfolio"
    ]
    
    # We'll focus on injecting links into the main READMEs and Personal files
    # to pull everything together.
    
    # 1. Link all Project READMEs to Hubs
    for proj in projects:
        path = f"Project Knowledge/datascience-Roman/projects/{proj}/README.md"
        content = get_file_content(path)
        if content:
            added_links = []
            for hub_path, keywords in HUBS.items():
                hub_name = Path(hub_path).stem
                for kw in keywords:
                    if kw.lower() in content.lower():
                        link = f"[[{hub_path.replace('.md', '')}|{hub_name}]]"
                        if link not in content:
                            added_links.append(link)
                        break
            if added_links:
                content += "\n\n--- \n**Ключевые темы:** " + ", ".join(added_links)
                update_file(path, content)
                print(f"🔗 Linked Project {proj} to hubs.")

    # 2. Aggressively link Personal Notes to Hubs and Projects
    # We'll target files that seem isolated
    personal_files = [
        "Personal/Пространство Роста/Моя_Жизнь/README.md",
        "Personal/Пространство Роста/Моя_Жизнь/Саморазвитие/Цели/README.md",
        "Personal/Пространство Роста/Моя_Жизнь/Саморазвитие/Проблемы/Актуальные_проблемы.md",
        "Personal/Пространство Роста/Моя_Жизнь/Саморазвитие/Проблемы/Анализ_поиска_работы_2026-02.md",
        "Personal/Пространство Роста/Моя_Жизнь/Разум/Рефлексии/README.md",
        "Personal/Пространство Роста/Моя_Жизнь/Дух/Практики/Ежедневные_ритуалы.md"
    ]
    
    for path in personal_files:
        content = get_file_content(path)
        if content:
            # Link to Hubs
            added = []
            for hub_path, keywords in HUBS.items():
                hub_name = Path(hub_path).stem
                for kw in keywords:
                    if kw.lower() in content.lower():
                        link = f"[[{hub_path.replace('.md', '')}|{hub_name}]]"
                        if link not in content:
                            added.append(link)
                        break
            
            # Link to Core Brain always
            if "[[000_CORE_BRAIN]]" not in content:
                content = "[[000_CORE_BRAIN|⬅️ Назад в Core Brain]]\n\n" + content
                
            if added:
                content += "\n\n--- \n**Контекст из Базы Знаний:** " + ", ".join(added)
            
            update_file(path, content)
            print(f"🔗 Weaved personal note: {path}")

if __name__ == "__main__":
    create_hubs()
    deep_weave()
