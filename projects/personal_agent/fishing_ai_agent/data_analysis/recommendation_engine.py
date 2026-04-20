# -*- coding: utf-8 -*-
import sys
import json
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
import os

# Добавляем корневую директорию проекта в sys.path
# sys.path.append('.') - старый вариант, который не всегда работает
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import SessionLocal
from database.models import ScrapedData, Lure, Catch, FishingSession, WaterBody, LureKnowledge
from inventory.inventory_manager import list_inventory

# Ассоциации "рыба -> типы приманок"
FISH_TO_LURE_TYPE_MAP = {
    'Щука': ['воблер', 'блесна', 'силикон'],
    'Окунь': ['воблер', 'блесна', 'силикон'],
    'Судак': ['воблер', 'силикон'],
    'Голавль': ['воблер', 'блесна'],
    'Жерех': ['блесна', 'воблер'],
}

def generate_advanced_recommendations(db: Session, water_body_name: str, top_n: int = 20) -> dict:
    """
    Генерирует продвинутые, таргетированные рекомендации для конкретного водоема.
    """
    report = {"to_buy": {}, "colors_and_sizes": []}
    
    # 1. Определяем целевую рыбу для этого водоема на основе логов
    target_fish_query = db.query(Catch.fish_type).join(FishingSession).join(WaterBody)\
        .filter(WaterBody.name == water_body_name).distinct()
    target_fishes = [row[0] for row in target_fish_query.all()]
    
    if not target_fishes:
        # Если по водоему нет данных, берем стандартный набор хищников
        target_fishes = ['Щука', 'Окунь', 'Судак']

    # 2. Определяем релевантные типы приманок
    relevant_lure_types = set()
    for fish in target_fishes:
        relevant_lure_types.update(FISH_TO_LURE_TYPE_MAP.get(fish, []))
    
    # 3. Получаем все релевантные приманки из базы знаний
    knowledge_lures = db.query(LureKnowledge).filter(LureKnowledge.lure_type.in_(relevant_lure_types)).all()
    
    # 4. Получаем текущий инвентарь
    inventory = list_inventory(db)
    inventory_models = {f"{lure.brand.lower().strip()} {lure.model.lower().strip()}" for lure in inventory}

    # 5. Отбираем, что нужно докупить, и группируем по типу
    for lure in knowledge_lures:
        lure_full_name = f"{lure.brand.lower().strip()} {lure.model.lower().strip()}"
        is_in_inventory = any(inv_model in lure_full_name or lure_full_name in inv_model for inv_model in inventory_models)

        if not is_in_inventory:
            lure_type = lure.lure_type
            if lure_type not in report["to_buy"]:
                report["to_buy"][lure_type] = []
            
            if len(report["to_buy"][lure_type]) < top_n:
                 report["to_buy"][lure_type].append(f"{lure.brand} {lure.model}")

    # 6. Анализируем успешные цвета и размеры на этом водоеме
    successful_catches = db.query(Lure.color, Lure.size).join(Catch).join(FishingSession).join(WaterBody)\
        .filter(WaterBody.name == water_body_name).distinct().all()
    
    for color, size in successful_catches:
        if color:
            report["colors_and_sizes"].append(f"Успешный цвет: '{color}'")
        if size:
            report["colors_and_sizes"].append(f"Успешный размер: '{size}'")

    return report


def analyze_personal_effectiveness(db: Session, water_body_name: str = None, fish_type: str = None):
    """
    Анализирует личную эффективность приманок на основе логов рыбалки.
    """
    query = db.query(
        Lure.brand,
        Lure.model,
        Lure.color,
        WaterBody.name.label('water_body_name'),
        Catch.fish_type,
        func.count(Catch.id).label('catch_count')
    ).join(Catch, Lure.id == Catch.lure_id)\
     .join(FishingSession, Catch.session_id == FishingSession.id)\
     .join(WaterBody, FishingSession.water_body_id == WaterBody.id)

    if water_body_name:
        query = query.filter(WaterBody.name == water_body_name)
    
    if fish_type:
        query = query.filter(Catch.fish_type == fish_type)

    results = query.group_by(
        Lure.brand,
        Lure.model,
        Lure.color,
        WaterBody.name,
        Catch.fish_type
    ).order_by(func.count(Catch.id).desc()).all()
    
    return results


def generate_detailed_recommendations(db: Session, fish_name: str) -> dict:
    """
    Генерирует детальные рекомендации (конкретные модели и бренды) по конкретной рыбе.
    """
    processed_entries = db.query(ScrapedData).filter(
        ScrapedData.processed == True,
        ScrapedData.extracted_info.isnot(None)
    ).all()

    # Будем считать упоминания конкретных моделей
    lure_model_counter = Counter()

    for entry in processed_entries:
        try:
            info = json.loads(entry.extracted_info)
            fish_counts = info.get('fish_counts', {})

            if fish_name in fish_counts:
                specific_lures = info.get('specific_lures', [])
                for lure in specific_lures:
                    # Создаем уникальный ключ для приманки: "бренд модель (размер)"
                    model_key = f"{lure['brand'].capitalize()}"
                    if lure.get('model'):
                        model_key += f" {lure['model'].capitalize()}"
                    if lure.get('size'):
                        model_key += f" ({lure['size']})"
                    
                    lure_model_counter[model_key] += 1
        except (json.JSONDecodeError, AttributeError):
            continue
            
    return {
        "specific_models": lure_model_counter
    }

def analyze_arsenal_gaps_detailed(db: Session, fish_name: str) -> str:
    """
    Анализирует инвентарь на основе ДЕТАЛЬНЫХ рекомендаций и находит пробелы.
    """
    # 1. Получаем детальные рекомендации
    recommendations = generate_detailed_recommendations(db, fish_name)
    recommended_models = {model for model, count in recommendations['specific_models'].most_common(5)}
    
    # 2. Получаем текущий инвентарь в виде простых строк для сравнения
    inventory = list_inventory(db)
    inventory_models = {f"{lure.brand.capitalize()} {lure.model.capitalize()}" for lure in inventory}
    
    # 3. Формируем отчет
    report = f"--- ДЕТАЛЬНЫЙ АНАЛИЗ АРСЕНАЛА ДЛЯ: {fish_name.upper()} ---\n\n"
    
    if not recommended_models:
        report += "Недостаточно данных для построения детальных рекомендаций.\n"
        return report

    report += "Топ-5 упоминаемых моделей: " + ", ".join(recommended_models) + "\n\n"
    
    # Ищем пробелы. Сравнение пока упрощенное (без учета размера).
    gaps = []
    for rec_model in recommended_models:
        is_in_inventory = False
        # Проверяем, есть ли что-то похожее в инвентаре
        for inv_model_full in inventory_models:
            if inv_model_full in rec_model:
                is_in_inventory = True
                break
        if not is_in_inventory:
            gaps.append(rec_model)
            
    if not gaps:
        report += "✅ Ваш арсенал хорошо укомплектован согласно найденным данным!\n"
    else:
        report += "⚠️ СОВЕТ: РАССМОТРЕТЬ К ПОКУПКЕ\n"
        for model in gaps:
            report += f"  - {model} (часто упоминается, но похожего нет в вашем арсенале)\n"
            
    return report


def generate_user_recommendations(db: Session, knowledge_lure_limit: int = 10) -> dict:
    """
    Генерирует персональные рекомендации: что докупить и что распробовать.
    """
    
    # 1. Получить текущий инвентарь
    inventory = list_inventory(db)
    inventory_models = {f"{lure.brand.lower().strip()} {lure.model.lower().strip()}" for lure in inventory}
    inventory_ids = {lure.id for lure in inventory}

    # 2. Получить "лучшие" приманки из базы знаний
    top_knowledge_lures = db.query(LureKnowledge).order_by(LureKnowledge.source_url != 'manual_import', LureKnowledge.id).limit(knowledge_lure_limit).all()
    
    knowledge_models_to_check = []
    for lure in top_knowledge_lures:
        knowledge_models_to_check.append({
            "full_name": f"{lure.brand.lower().strip()} {lure.model.lower().strip()}",
            "brand": lure.brand,
            "model": lure.model,
            "type": lure.lure_type
        })

    # 3. Найти, что нужно докупить (анализ пробелов)
    lures_to_buy = []
    for k_lure in knowledge_models_to_check:
        is_in_inventory = any(inv_model in k_lure["full_name"] or k_lure["full_name"] in inv_model for inv_model in inventory_models)
        if not is_in_inventory:
            lures_to_buy.append(k_lure)
            
    # 4. Найти, что нужно распробовать из имеющегося
    successful_lure_ids = {c.lure_id for c in db.query(Catch.lure_id).distinct().all()}
    lures_to_try_ids = inventory_ids - successful_lure_ids
    lures_to_try = db.query(Lure).filter(Lure.id.in_(lures_to_try_ids)).all() if lures_to_try_ids else []
        
    return {
        "to_buy": lures_to_buy,
        "to_try": lures_to_try,
        "successful": db.query(Lure).filter(Lure.id.in_(successful_lure_ids)).all()
    }


if __name__ == '__main__':
    db = SessionLocal()
    try:
        # --- НОВЫЙ ПРОДВИНУТЫЙ АНАЛИЗ ---
        TARGET_WATER_BODY = "Ока" # Название водоема для анализа
        print(f"--- 🎣 ПЕРСОНАЛЬНЫЙ СОВЕТНИК ДЛЯ ВОДОЕМА: {TARGET_WATER_BODY.upper()} 🎣 ---")

        recommendations = generate_advanced_recommendations(db, TARGET_WATER_BODY)

        print("\n🔥 ТОП РЕКОМЕНДАЦИЙ К ПОКУПКЕ (на основе ваших уловов на этом водоеме):")
        if not recommendations['to_buy']:
            print("  ✅ Ваш арсенал полностью укомплектован для известных вам целей на этом водоеме!")
        else:
            for lure_type, lures in recommendations['to_buy'].items():
                print(f"\n  --- Категория: {lure_type.upper()} ---")
                for lure_name in lures:
                    print(f"    - {lure_name}")

        print("\n🎨 РЕКОМЕНДУЕМЫЕ ЦВЕТА И РАЗМЕРЫ (на основе ваших успехов здесь):")
        if not recommendations['colors_and_sizes']:
            print("  Пока нет данных об успешных цветах/размерах на этом водоеме. Логируйте уловы!")
        else:
            for tip in set(recommendations['colors_and_sizes']): # Используем set для уникальности
                print(f"  - {tip}")

    finally:
        db.close()
