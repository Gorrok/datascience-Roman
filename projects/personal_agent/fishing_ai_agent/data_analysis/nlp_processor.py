import re
import pymorphy3
from nltk.tokenize import word_tokenize
import nltk

# Загрузчик перенесен в main.py для централизованного управления
# # Одноразовая загрузка необходимых компонентов NLTK
# try:
#     nltk.data.find('tokenizers/punkt')
# except nltk.downloader.Downloader: # Исправленная ошибка
#     print("--- Загрузка токенизатора 'punkt' для NLTK ---")
#     nltk.download('punkt', quiet=True)

# Инициализируем морфологический анализатор
morph = pymorphy3.MorphAnalyzer()

def preprocess_text(text: str) -> list[str]:
    """
    Выполняет полную предобработку текста: очистку, токенизацию и лемматизацию.

    Args:
        text: Исходная строка текста.

    Returns:
        Список очищенных и нормализованных слов (лемм).
    """
    if not isinstance(text, str):
        return []

    # 1. Приведение к нижнему регистру
    text = text.lower()

    # 2. Удаление URL-адресов
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # 3. Удаление всего, что не является буквами кириллицы, латиницы или пробелами
    text = re.sub(r'[^a-zа-яё\s]', '', text)

    # 4. Токенизация (разбиение на слова)
    tokens = word_tokenize(text, language='russian')

    # 5. Лемматизация (приведение к начальной форме) и удаление стоп-слов
    lemmas = []
    # Простой список стоп-слов, можно расширить
    stop_words = {'и', 'в', 'на', 'с', 'о', 'не', 'я', 'а', 'по', 'за', 'но', 'это', 'как', 'бы'}
    for token in tokens:
        if token and token not in stop_words:
            normal_form = morph.parse(token)[0].normal_form
            lemmas.append(normal_form)
            
    return lemmas

if __name__ == '__main__':
    # Пример использования
    example_text = """
    Всем привет! Вчера отлично отрыбачил на реке. 
    Щуку поймал на воблер от Strike Pro, а окуней - на джиг. 
    Подробности тут: https://example.com. Мой лучший улов!
    """
    
    processed_words = preprocess_text(example_text)
    
    print(f"Исходный текст:\n{example_text}")
    print("-" * 30)
    print(f"Обработанные слова (леммы):\n{processed_words}")

    # Пример с пустым вводом
    print("\n" + "-" * 30)
    print("Тест с пустым текстом:")
    print(preprocess_text(""))
