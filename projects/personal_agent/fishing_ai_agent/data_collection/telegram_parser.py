import sys
from pyrogram import Client
from pyrogram.errors import exceptions as pyrogram_exceptions

# Добавляем корневую директорию проекта в sys.path
sys.path.append('.')

async def get_channel_messages(client: Client, channel_username: str, limit: int = 100):
    """
    Получает последние сообщения из публичного Telegram-канала с помощью Pyrogram.
    Теперь принимает клиент как аргумент.
    """
    messages_text = []
    try:
        print(f"  -> Pyrogram: Получение истории для @{channel_username}...")
        
        async for message in client.get_chat_history(channel_username, limit=limit):
            if message.text:
                messages_text.append(message.text)
        
        print(f"  -> Pyrogram: Найдено {len(messages_text)} сообщений для @{channel_username}.")

    except pyrogram_exceptions.bad_request_400.UsernameNotOccupied:
        print(f"  -> Pyrogram: ОШИБКА - Канал @{channel_username} не существует.")
    except Exception as e:
        print(f"  -> Pyrogram: ПРОИЗОШЛА ОШИБКА при получении сообщений для @{channel_username}: {e}")
    
    return messages_text
