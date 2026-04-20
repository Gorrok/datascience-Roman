# -*- coding: utf-8 -*-
import sys
import os
import json
import shutil
from sqlalchemy.orm import Session

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import SessionLocal, init_db
from database.models import LureKnowledge
from data_collection.knowledge_parser import get_lure_links_from_category, parse_lure_page
from data_collection.sources import SOURCES # Импортируем наши источники

def run_knowledge_population(db: Session, limit_per_category: int | None = None):
    """
    Запускает процесс сбора и сохранения знаний о приманках
    по всем источникам и категориям из sources.py.
    """
    total_saved_count = 0
    
    # Проходим по каждому источнику (магазину)
    for source_name, source_config in SOURCES.items():
        print(f"\n--- НАЧАЛО СБОРА ДАННЫХ ИЗ ИСТОЧНИКА: {source_name.upper()} ---")
        
        # Проходим по каждой категории в источнике
        for lure_type, category_url in source_config['categories'].items():
            print(f"\n--- Обработка категории: {lure_type.upper()} ---")
            
            # 1. Получаем ссылки на приманки, передавая конфиг
            lure_links = get_lure_links_from_category(category_url, source_config)
            if not lure_links:
                print("Не удалось получить ссылки. Переход к следующей категории.")
                continue
                
            links_to_process = lure_links[:limit_per_category] if limit_per_category else lure_links
            print(f"Будет обработано {len(links_to_process)} из {len(lure_links)} найденных ссылок.")
            
            # 2. Парсим каждую страницу и сохраняем в БД
            saved_in_category = 0
            for link in links_to_process:
                if db.query(LureKnowledge).filter(LureKnowledge.source_url == link).first():
                    # print(f"  - Приманка по ссылке {link} уже есть в базе. Пропуск.")
                    continue
                    
                lure_data = parse_lure_page(link, source_config)
                
                if lure_data:
                    new_entry = LureKnowledge(
                        brand=lure_data['brand'],
                        model=lure_data['model'],
                        lure_type=lure_type, # Берем тип из ключа категории
                        description=lure_data['description'],
                        source_url=lure_data['source_url']
                    )
                    db.add(new_entry)
                    db.commit()
                    saved_in_category += 1
                    print(f"  -> Сохранено: {new_entry.brand} {new_entry.model}")
            
            total_saved_count += saved_in_category
            print(f"В категории '{lure_type}' добавлено {saved_in_category} новых записей.")

    print(f"\n--- СБОР ДАННЫХ ПО ВСЕМ ИСТОЧНИКАМ ЗАВЕРШЕН. Всего добавлено {total_saved_count} новых записей. ---")


if __name__ == '__main__':
    init_db()
    db = SessionLocal()
    
    try:
        # Для теста обработаем первые 5 приманок из КАЖДОЙ категории
        run_knowledge_population(db, limit_per_category=5)
    finally:
        db.close()
        # Очищаем кэш веб-драйвера после работы
        webdriver_cache_path = os.path.join(os.path.expanduser("~"), ".wdm")
        if os.path.exists(webdriver_cache_path):
            print("\n--- Очистка кэша веб-драйвера ---")
            shutil.rmtree(webdriver_cache_path)
