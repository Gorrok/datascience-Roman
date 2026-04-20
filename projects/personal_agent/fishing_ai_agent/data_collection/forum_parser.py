from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Используем новую функцию с Selenium
from data_collection.web_scraper import fetch_html_with_selenium

def parse_forum_page_for_topic_links(url: str) -> list[str]:
    """
    Парсит страницу раздела форума и извлекает ссылки на страницы тем, используя Selenium.
    """
    # Вызываем функцию, которая работает с JS
    html = fetch_html_with_selenium(url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    links = []
    
    # --- ДИАГНОСТИЧЕСКИЙ БЛОК ---
    print("\n--- НАЧАЛО ДИАГНОСТИКИ: ПОИСК ВСЕХ ССЫЛОК ---")
    all_links = soup.find_all('a', href=True)
    print(f"Найдено всего {len(all_links)} ссылок на странице.")
    
    count = 0
    for link in all_links:
        if count < 30:
            parent = link.parent
            parent_classes = parent.get('class', 'N/A')
            print(f"  - Текст: '{link.text.strip()}' | Href: {link['href']} | Класс родителя: {parent_classes}")
            count += 1
        else:
            break
    print("--- КОНЕЦ ДИАГНОСТИКИ ---\n")
    # --- КОНЕЦ ДИАГНОСТИЧЕСКОГО БЛОКА ---

    # Возвращаемся к первому, более точному селектору
    topic_elements = soup.select('.structItem-title a[href*="/forum/threads/"]')

    for element in topic_elements:
        href = element.get('href')
        if href:
            # Преобразуем относительную ссылку в абсолютную
            full_url = urljoin(url, href)
            links.append(full_url)
            
    unique_links = list(dict.fromkeys(links))
    return unique_links

if __name__ == '__main__':
    forum_section_url = "https://www.rusfishing.ru/forum/forums/primanki-i-nasadki.21/"
    print(f"Парсинг ссылок на темы из: {forum_section_url}")
    topic_links = parse_forum_page_for_topic_links(forum_section_url)
    
    if topic_links:
        print(f"\nНайдено {len(topic_links)} уникальных ссылок на темы:")
        for link in topic_links[:10]:
            print(link)
    else:
        print("\nНе удалось найти ссылки на темы.")