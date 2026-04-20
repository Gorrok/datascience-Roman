#!/usr/bin/python3
"""
Тест отправки сообщений в Telegram для проверки chat_id и bot token
"""

import requests
import json

# Тестовые данные - замените на реальные
BOT_TOKEN = "ВАШ_BOT_TOKEN"  # Замените на реальный токен бота
CHAT_IDS = {
    'луч': '-4832660589',
    'maximum': '-5089210322',
    'more': '-5053517827'
}

def test_send_message(bot_token, chat_id, text):
    """Тест отправки сообщения"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def test_bot_info(bot_token):
    """Проверка информации о боте"""
    url = f"https://api.telegram.org/bot{bot_token}/getMe"

    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("🔍 Тестирование Telegram бота...")
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print()

    # Проверка бота
    print("🤖 Проверка информации о боте:")
    bot_info = test_bot_info(BOT_TOKEN)
    print(json.dumps(bot_info, indent=2, ensure_ascii=False))
    print()

    if "error" in bot_info:
        print("❌ Ошибка с ботом! Проверьте токен.")
        exit(1)

    # Тест отправки в каждый чат
    for group, chat_id in CHAT_IDS.items():
        print(f"📤 Тестирование отправки в группу {group.upper()} (chat_id: {chat_id}):")
        test_message = f"🧪 Тестовое сообщение для группы {group.upper()}\nВремя: {__import__('datetime').datetime.now()}"

        result = test_send_message(BOT_TOKEN, chat_id, test_message)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("ok"):
            print("✅ Сообщение отправлено успешно!")
        else:
            print(f"❌ Ошибка: {result.get('description', 'Неизвестная ошибка')}")
        print()

    print("🎉 Тестирование завершено!")