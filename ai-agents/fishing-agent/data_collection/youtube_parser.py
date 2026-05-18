import sys
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Возвращаем стандартный импорт
from config import YOUTUBE_API_KEY

# Проверяем, есть ли API ключ
if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == 'your_youtube_api_key_here':
    print("Ошибка: API-ключ YouTube не найден. Проверьте .env файл.")
    youtube_service = None
else:
    youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def find_channel_id_by_query(query: str) -> str | None:
    """
    Ищет ID канала по поисковому запросу (например, названию канала или @-имени).
    """
    if not youtube_service:
        return None
    try:
        request = youtube_service.search().list(
            part="id",
            q=query,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        if response.get('items'):
            return response['items'][0]['id']['channelId']
        return None
    except HttpError as e:
        print(f"Произошла ошибка HTTP при поиске канала: {e.resp.status} {e.content}")
        return None

# Оставляем старую функцию, но не будем ее использовать
def find_channel_id_by_name(username: str) -> str | None:
    """
    Ищет ID канала по его имени пользователя (например, @username).
    """
    if not youtube_service:
        return None
    try:
        request = youtube_service.channels().list(
            part="id",
            forUsername=username
        )
        response = request.execute()
        if response.get('items'):
            return response['items'][0]['id']
        return None
    except HttpError as e:
        print(f"Произошла ошибка HTTP при поиске канала: {e.resp.status} {e.content}")
        return None

def get_channel_videos(channel_id: str, max_results: int = 10) -> list[dict]:
    """
    Получает список последних видео с указанного YouTube канала.
    """
    if not youtube_service:
        return []
    
    try:
        # Сначала получаем ID плейлиста "uploads" для канала
        request = youtube_service.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Затем получаем видео из этого плейлиста
        request = youtube_service.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=max_results
        )
        response = request.execute()

        videos = []
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            video_title = item['snippet']['title']
            video_description = item['snippet']['description']
            videos.append({
                'id': video_id,
                'title': video_title,
                'description': video_description
            })
        return videos

    except HttpError as e:
        print(f"Произошла ошибка HTTP: {e.resp.status} {e.content}")
        return []
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return []

def get_video_comments(video_id: str, max_results: int = 20) -> list[str]:
    """
    Получает комментарии к указанному видео.
    """
    if not youtube_service:
        return []
        
    comments = []
    try:
        request = youtube_service.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        
        return comments
    except HttpError as e:
        # Некоторые видео могут иметь отключенные комментарии
        if "commentsDisabled" in str(e.content):
            print(f"Комментарии для видео {video_id} отключены.")
        else:
            print(f"Произошла ошибка HTTP при получении комментариев: {e.resp.status} {e.content}")
        return []
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при получении комментариев: {e}")
        return []


if __name__ == '__main__':
    # Пример использования. 
    # ID канала "Снасти Здрасьте": UCg__N4v2j0W2s4iA24m-z_g
    
    TEST_CHANNEL_ID = "UCg__N4v2j0W2s4iA24m-z_g"
    
    if youtube_service:
        print(f"Получение видео с канала ID: {TEST_CHANNEL_ID}...")
        videos = get_channel_videos(TEST_CHANNEL_ID, max_results=2)
        
        if videos:
            print(f"\nНайдено {len(videos)} видео.")
            for video in videos:
                print(f"\n--- Видео: {video['title']} (ID: {video['id']}) ---")
                print(f"Описание (первые 100 символов): {video['description'][:100]}...")
                
                print("\n  Получение комментариев...")
                comments = get_video_comments(video['id'], max_results=3)
                if comments:
                    for i, comment in enumerate(comments, 1):
                        print(f"    {i}. {comment}")
                else:
                    print("  Комментариев не найдено или они отключены.")
        else:
            print("Не удалось получить видео с канала. Проверьте правильность ID и API ключа.")
