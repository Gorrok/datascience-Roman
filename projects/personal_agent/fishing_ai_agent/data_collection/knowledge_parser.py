# -*- coding: utf-8 -*-
import sys
import os
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_collection.web_scraper import fetch_html_with_selenium
from data_collection.sources import SOURCES # Импортируем новую структуру

def get_lure_links_from_category(category_url: str, source_config: dict) -> list[str]:
    """
    Собирает ссылки на страницы конкретных приманок из каталога.
    Работает с конфигурацией источника.
    """
    print(f"Сбор ссылок из каталога: {category_url}")
    html = fetch_html_with_selenium(category_url)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    
    # Используем селектор из конфигурации
    selector = source_config['selectors']['category_links']
    lure_elements = soup.select(selector)
    
    for element in lure_elements:
        href = element.get('href')
        if href:
            # Используем базовый URL из конфигурации
            full_url = urljoin(source_config['base_url'], href)
            links.append(full_url)
            
    print(f"Найдено {len(links)} ссылок на приманки.")
    return list(dict.fromkeys(links))


def parse_lure_page(lure_url: str, source_config: dict) -> dict | None:
    """
    Парсит страницу конкретной приманки, используя конфигурацию источника.
    """
    print(f"  -> Парсинг страницы: {lure_url}")
    html = fetch_html_with_selenium(lure_url)
    if not html:
        return None
        
    soup = BeautifulSoup(html, 'html.parser')
    selectors = source_config['selectors']
    
    try:
        title_element = soup.select_one(selectors['title'])
        full_title = title_element.text.strip() if title_element else "N/A"
        
        # Ищем бренд, используя селекторы и ключевое слово из конфига
        brand = "N/A"
        # zip'уем ключи (dt) и значения (dd) из таблицы характеристик
        char_keys = soup.select(selectors['brand_row_dt'])
        char_values = soup.select(selectors['brand_row_dd'])
        
        for key, value in zip(char_keys, char_values):
            if key and selectors['brand_keyword'] in key.text.lower():
                brand = value.text.strip()
                break
        
        model = full_title.replace(brand, '').strip()

        description_element = soup.select_one(selectors['description'])
        description = description_element.text.strip() if description_element else "Нет описания."

        lure_data = {
            "brand": brand,
            "model": model,
            "description": description,
            "source_url": lure_url,
        }
        
        return lure_data
        
    except Exception as e:
        print(f"    -! Ошибка при парсинге страницы {lure_url}: {e}")
        return None

if __name__ == '__main__':
    # Пример использования с новой структурой
    
    # 1. Выбираем источник
    source_name = 'rybalkashop.ru'
    source_config = SOURCES[source_name]
    
    # 2. Выбираем категорию из источника
    test_category_url = source_config['categories']['vobler']
    
    # 3. Передаем URL и конфигурацию в функцию
    lure_links = get_lure_links_from_category(test_category_url, source_config)
    
    if lure_links:
        print("\n--- Пример парсинга первых 3 приманок ---")
        for link in lure_links[:3]:
            # Передаем конфигурацию и в эту функцию
            data = parse_lure_page(link, source_config)
            if data:
                print(f"    - Бренд: {data['brand']}")
                print(f"    - Модель: {data['model']}")
                print(f"    - Описание (первые 70 символов): {data['description'][:70]}...")
            print("-" * 20)
    else:
        print("Не удалось получить ссылки на приманки.")
