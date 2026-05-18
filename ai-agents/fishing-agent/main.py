import sys
import os
from sqlalchemy.orm import Session
import asyncio
from pyrogram import Client
import nltk

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import SessionLocal, init_db
from database.models import ScrapedData
from data_collection.youtube_parser import get_channel_videos, get_video_comments, find_channel_id_by_query
from data_collection.telegram_parser import get_channel_messages
from secrets import TELEGRAM_API_ID, TELEGRAM_API_HASH
from data_analysis.nlp_processor import preprocess_text
# Меняем старый анализатор на новый
from data_analysis.lure_analyzer import analyze_text_for_lures
# Меняем старую функцию рекомендаций на новую
from data_analysis.recommendation_engine import analyze_arsenal_gaps_detailed
import json
# Удаляем импорты, связанные с демонстрационным инвентарем
# from inventory.inventory_manager import add_lure, list_inventory, remove_lure


def save_youtube_data_to_db(db: Session, channel_query: str):
    """
    Получает данные с YouTube канала и сохраняет их в базу данных.
    (Этот код остается синхронным и не меняется)
    """
    print(f"\n--- Начало сбора данных с YouTube канала: {channel_query} ---")
    channel_id = find_channel_id_by_query(channel_query)
    if not channel_id:
        print(f"Не удалось найти ID для канала '{channel_query}'.")
        return
    print(f"Найден ID канала: {channel_id}")
    videos = get_channel_videos(channel_id, max_results=5)
    if not videos:
        print("Не удалось получить видео.")
        return
    print(f"Найдено {len(videos)} видео. Сохранение в базу данных...")
    for video in videos:
        comments = get_video_comments(video['id'], max_results=10)
        full_text_content = f"Заголовок: {video['title']}\n\nОписание: {video['description']}\n\nКомментарии:\n"
        full_text_content += "\n---\n".join(comments)
        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        existing_data = db.query(ScrapedData).filter(ScrapedData.source_url == video_url).first()
        if not existing_data:
            scraped_entry = ScrapedData(source_type='youtube', source_url=video_url, content=full_text_content)
            db.add(scraped_entry)
            print(f"  - Сохранено видео: {video['title']}")
        else:
            print(f"  - Видео уже существует в БД: {video['title']}")

async def save_telegram_data_to_db(client: Client, db: Session, channel_username: str):
    """
    Получает данные из Telegram канала и сохраняет их в базу данных.
    """
    print(f"\n--- Сбор данных из Telegram: @{channel_username} ---")
    messages = await get_channel_messages(client, channel_username, limit=20)

    if not messages:
        print(f"Сообщений для @{channel_username} не найдено.")
        return

    print(f"Найдено {len(messages)} сообщений. Сохранение в базу данных...")
    for msg in messages:
        source_url = f"https://t.me/{channel_username}/{hash(msg)}"
        existing_data = db.query(ScrapedData).filter(ScrapedData.source_url == source_url).first()
        if not existing_data:
            scraped_entry = ScrapedData(source_type='telegram', source_url=source_url, content=msg)
            db.add(scraped_entry)
            print(f"  - Сохранено сообщение: {msg[:50]}...")
        else:
            print(f"  - Сообщение уже существует в БД: {msg[:50]}...")

def run_analysis_on_db(db: Session):
    """
    Выполняет анализ необработанных текстов в базе данных, используя новый детальный анализатор.
    """
    print("\n--- НАЧАЛО ДЕТАЛЬНОГО АНАЛИЗА ДАННЫХ В БД ---")
    
    # 1. Находим все записи (даже уже обработанные, чтобы пере-анализировать с новым методом)
    all_data = db.query(ScrapedData).all()
    
    if not all_data:
        print("Данных для анализа не найдено.")
        return

    print(f"Найдено {len(all_data)} записей для пере-анализа...")
    
    analysis_counter = 0
    for entry in all_data:
        # 2. Используем новый анализатор, который работает с сырым текстом
        analysis_result = analyze_text_for_lures(entry.content)
        
        # Проверяем, был ли найден хоть какой-то результат (рыба или конкретные приманки)
        if analysis_result['fish_counts'] or analysis_result['specific_lures']:
            # 4. Сохраняем результат в JSON и обновляем запись
            # Преобразуем Counter в обычный dict для JSON-сериализации
            serializable_result = {
                'fish_counts': dict(analysis_result['fish_counts']),
                'lure_type_counts': dict(analysis_result['lure_type_counts']),
                'brand_counts': dict(analysis_result['brand_counts']),
                'specific_lures': analysis_result['specific_lures']
            }
            entry.extracted_info = json.dumps(serializable_result, ensure_ascii=False, indent=2)
            entry.processed = True
            analysis_counter += 1
            print(f"  - Проанализирована запись ID {entry.id}. Найдены конкретные данные.")
        else:
            # Если ничего не найдено, просто помечаем как обработанное
            entry.processed = True
            print(f"  - Проанализирована запись ID {entry.id}. Конкретные данные не найдены.")

    db.commit()
    print(f"--- АНАЛИЗ ЗАВЕРШЕН. Обновлено {analysis_counter} записей с результатами. ---")

# Удаляем всю демонстрационную функцию
# def manage_inventory_example(db: Session):
#     """
#     Демонстрирует работу с инвентарем: очищает старые тестовые записи,
#     добавляет новые и выводит список.
#     """
#     print("\n--- УПРАВЛЕНИЕ ИНВЕНТАРЕМ (ДЕМО) ---")
    
#     # Очистим инвентарь от предыдущих запусков, чтобы не было дублей
#     all_lures = list_inventory(db)
#     for lure in all_lures:
#         remove_lure(db, lure.id)

#     print("\nДобавляем тестовые приманки в ваш арсенал...")
#     # Добавляем приманки, которые якобы есть у вас
#     add_lure(db, lure_type='воблер', brand='rapala', model='x-rap', size='100mm')
#     add_lure(db, lure_type='силикон', brand='keitech', model='easy shiner', size='3"')
    
#     print("\n--- ВАШ ТЕКУЩИЙ АРСЕНАЛ ---")
#     current_inventory = list_inventory(db)
#     if not current_inventory:
#         print("Инвентарь пуст.")
#     else:
#         for lure in current_inventory:
#             print(f"  - {lure.brand.capitalize()} {lure.model.capitalize()} ({lure.lure_type})")

def run_recommendation_engine(db: Session):
    """
    Запускает движок рекомендаций и выводит детальные отчеты по анализу арсенала.
    """
    print("\n--- ЗАПУСК ДЕТАЛЬНЫХ ПЕРСОНАЛЬНЫХ РЕКОМЕНДАЦИЙ ---")
    
    target_fishes = ['щука', 'окунь', 'судак']
    
    for fish in target_fishes:
        # Вызываем новую детальную функцию для анализа пробелов
        recommendations = analyze_arsenal_gaps_detailed(db, fish)
        print(recommendations)
        print("-" * 40)


def download_nltk_data():
    """
    Проверяет наличие и при необходимости загружает пакет 'punkt' для NLTK.
    """
    resources = ['punkt', 'punkt_tab']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
            print(f"--- NLTK '{resource}' уже загружен. ---")
        except LookupError:
            print(f"--- Загрузка пакета '{resource}' для NLTK... ---")
            nltk.download(resource, quiet=True)
            print(f"--- '{resource}' успешно загружен. ---")


async def main():
    # --- Подготовка ---
    download_nltk_data() # Сначала проверяем и загружаем все необходимое
    init_db()
    db: Session = SessionLocal()

    try:
        # --- YOUTUBE (Синхронная часть) ---
        print("\n--- НАЧАЛО СБОРА ДАННЫХ YOUTUBE ---")
        YOUTUBE_CHANNELS = [
            "Vitalik Ignatyuk",
            "Клуб рыбаков / Клёвая рыбалка",
            "Снасти Здрасьте",
            "NRG FISHING",
            "Сибирский странник",
            "AssistanceTV",
            "Просто о рыбалке"
        ]
        for channel in YOUTUBE_CHANNELS:
            save_youtube_data_to_db(db, channel)
        print("--- ЗАВЕРШЕНИЕ СБОРА ДАННЫХ YOUTUBE ---")

        # --- TELEGRAM (Асинхронная часть) ---
        print("\n--- ИНИЦИАЛИЗАЦИЯ КЛИЕНТА TELEGRAM ---")
        if not TELEGRAM_API_ID or not TELEGRAM_API_HASH:
            print("ОШИБКА: Ключи для Telegram не найдены в secrets.py")
            return

        # Самый надежный способ управления сессией
        async with Client("pyrogram_session", api_id=int(TELEGRAM_API_ID), api_hash=TELEGRAM_API_HASH) as app:
            print("--- КЛИЕНТ TELEGRAM ЗАПУЩЕН ---")
            TELEGRAM_CHANNELS = [
                "prosto_o_rybalk",
                "rubalkamoskva",
                "fishingspb1",
                "Fishing_Kuban_Adygea",
                "rybalka_kazan_fishing",
                "astrafishing30",
                "maintarget"
            ]
            for channel in TELEGRAM_CHANNELS:
                await save_telegram_data_to_db(app, db, channel)

        print("--- КЛИЕНТ TELEGRAM ОСТАНОВЛЕН ---")
        
        db.commit()
        print("\nДанные сбора успешно сохранены в БД.")

        # --- АНАЛИЗ (Синхронная часть) ---
        run_analysis_on_db(db)

        # Удаляем вызов демонстрационного блока
        # # --- ИНВЕНТАРЬ (Синхронная часть) ---
        # manage_inventory_example(db)

        # --- РЕКОМЕНДАЦИИ (Синхронная часть) ---
        run_recommendation_engine(db)

    except Exception as e:
        print(f"\nПроизошла ошибка в главном процессе: {e}")
    finally:
        db.close()
        print("\nСбор и сохранение всех данных завершены.")


if __name__ == '__main__':
    asyncio.run(main())
