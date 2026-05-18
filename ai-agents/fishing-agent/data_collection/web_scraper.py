import requests
import time
from bs4 import BeautifulSoup
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import USER_AGENT, REQUEST_DELAY

def get_webdriver():
    """Настраивает и возвращает экземпляр веб-драйвера Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме, без открытия окна браузера
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Автоматически устанавливаем и управляем драйвером
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_html_with_selenium(url: str) -> str:
    """
    Получает HTML-содержимое страницы с помощью Selenium, дожидаясь выполнения JS.
    """
    driver = None
    try:
        driver = get_webdriver()
        print(f"Fetching URL with Selenium: {url}...")
        driver.get(url)
        # Даем время на прогрузку динамического контента
        time.sleep(REQUEST_DELAY + 3) # Дополнительная задержка для JS
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error fetching {url} with Selenium: {e}")
        return None
    finally:
        if driver:
            driver.quit()

def fetch_html(url: str) -> str:
    """
    Получает HTML-содержимое страницы по заданному URL.
    """
    headers = {
        'User-Agent': USER_AGENT
    }
    try:
        print(f"Fetching URL: {url}...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text_from_html(html: str) -> str:
    """
    Извлекает весь видимый текст из HTML-разметки.
    """
    if not html:
        return ""
    soup = BeautifulSoup(html, 'html.parser')
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

if __name__ == '__main__':
    test_url = "https://www.rusfishing.ru/forum/forums/primanki-i-nasadki.21/"
    html_content = fetch_html(test_url)
    if html_content:
        print("\nSuccessfully fetched HTML.")
        plain_text = extract_text_from_html(html_content)
        print("\nExtracted Text (first 500 characters):")
        print(plain_text[:500])
    else:
        print("\nFailed to fetch HTML.")