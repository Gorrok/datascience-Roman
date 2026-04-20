# -*- coding: utf-8 -*-
import sys
import re
from collections import Counter, defaultdict

# Добавляем корневую директорию проекта в sys.path
sys.path.append('.')
from data_analysis.nlp_processor import preprocess_text

# --- Словари для анализа (значительно расширены) ---

# Ключевые слова приводятся к нормальной форме (лемме)
FISH_KEYWORDS = {
    'щука', 'окунь', 'судак', 'сом', 'лещ', 'плотва', 'голавль', 'жерех', 'язь', 'форель', 'хариус'
}

LURE_TYPE_KEYWORDS = {
    'воблер', 'блесна', 'вертушка', 'колебалка', 'джиг', 'резина', 'силикон', 
    'мормышка', 'тейл-спиннер', 'раттлин', 'мандула', 'стример', 'муха', 'поппер', 'уокер'
}

BRAND_KEYWORDS = {
    # Воблеры
    'rapala', 'zipbaits', 'megabass', 'lucky john', 'strike pro', 'yo-zuri', 'jackall', 
    'pontoon21', 'kosadaka', 'duo', 'tsuyoki', 'salmo', 'ima', 'major craft', 'smith',
    # Силикон
    'keitech', 'relax', 'narval', 'fanatik', 'sawamura', 'crazy fish', 'lucky john', 'frapp',
    # Блесны
    'mepps', 'blue fox', 'myran', 'kuusamo', 'williams', 'acme',
    # Спиннинги/Катушки (могут упоминаться рядом с приманками)
    'shimano', 'daiwa', 'g.loomis', 'st.croix', 'favorite', 'graphiteleader', 'major craft'
}

# Добавляем словарь для извлечения конкретных моделей, если они упоминаются
# Ключ - бренд, значение - список моделей (в нижнем регистре и без пробелов для простоты поиска)
MODEL_KEYWORDS = {
    'megabass': ['vision', 'vision110', 'popx', 'griffon'],
    'zipbaits': ['orbit', 'rigge', 'khamsin'],
    'jackall': ['chubby', 'squadminnow', 'magsquad', 'rerange'],
    'keitech': ['easyshiner', 'swingimpact', 'sexyshad'],
    'rapala': ['x-rap', 'shadowrap', 'countdown', 'jssr'],
    'lucky john': ['tioga', 'jocoshaker', 'ultraworm']
}


def analyze_text_for_lures(text: str) -> dict:
    """
    Анализирует исходный текст на упоминания рыб и конкретных приманок (бренд, модель, размер, цвет).
    Работает с сырым текстом для поиска паттернов.
    """
    
    # Сначала проводим базовую обработку для поиска ключевых слов
    processed_words = preprocess_text(text)
    
    found_fish = [word for word in processed_words if word in FISH_KEYWORDS]
    found_lure_types = [word for word in processed_words if word in LURE_TYPE_KEYWORDS]
    
    # Теперь ищем конкретные упоминания приманок в оригинальном тексте (в нижнем регистре)
    lower_text = text.lower()
    lure_mentions = []

    # Проходим по всем известным брендам
    for brand in BRAND_KEYWORDS:
        if brand in lower_text:
            # Ищем известные модели этого бренда
            found_model = None
            if brand in MODEL_KEYWORDS:
                for model in MODEL_KEYWORDS[brand]:
                    if model in lower_text.replace(" ", ""): # Ищем без пробелов, т.к. могут написать "vision 110" или "vision110"
                        found_model = model
                        break
            
            # Используем регулярные выражения для поиска размера и цвета рядом с брендом/моделью
            # Ищем в радиусе ~30 символов от упоминания бренда
            start_index = lower_text.find(brand)
            search_area = lower_text[start_index:start_index + 40]
            
            size_match = re.search(r'(\d{1,3}\s?(mm|мм|sm|см|"|in))|(\d\.\d\s?(in|"))', search_area)
            size = size_match.group(0).strip() if size_match else None
            
            mention = {
                "brand": brand,
                "model": found_model,
                "size": size,
                # Цвет пока пропустим, его сложнее надежно извлекать
            }
            
            # Добавляем, только если нашли что-то кроме бренда
            if mention['model'] or mention['size']:
                lure_mentions.append(mention)


    analysis_result = {
        'fish_counts': Counter(found_fish),
        'lure_type_counts': Counter(found_lure_types),
        'brand_counts': Counter([lure['brand'] for lure in lure_mentions]),
        'specific_lures': lure_mentions
    }
    
    return analysis_result


if __name__ == '__main__':
    # Пример использования
    example_text = """
    Сегодня на реке отлично отработал воблер Jackall Rerange 130SP. 
    Щуку поймал именно на него. Также пробовал Keitech Easy Shiner 4" - поймал пару окуней.
    A вот вертушка Mepps Aglia №3 молчала.
    """
    
    analysis = analyze_text_for_lures(example_text)
    
    print("--- Результаты детального анализа ---")
    print("\nНайденные рыбы:")
    for fish, count in analysis['fish_counts'].items():
        print(f"  - {fish}: {count} раз")
        
    print("\nНайденные типы приманок (общие):")
    for lure_type, count in analysis['lure_type_counts'].items():
        print(f"  - {lure_type}: {count} раз")

    print("\nНайденные конкретные приманки:")
    if not analysis['specific_lures']:
        print("  - Конкретных моделей не найдено.")
    else:
        for lure in analysis['specific_lures']:
            print(f"  - Бренд: {lure['brand']}, Модель: {lure.get('model', 'N/A')}, Размер: {lure.get('size', 'N/A')}")
