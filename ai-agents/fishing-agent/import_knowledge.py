# -*- coding: utf-8 -*-
import sys
import os
from sqlalchemy.orm import Session

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import SessionLocal, init_db
from database.models import LureKnowledge

# Список актуальных приманок для импорта, значительно расширенный
TOP_LURES = [
    # --- ВОБЛЕРЫ ---
    {
        "brand": "ZipBaits", "model": "Rigge 90SP", "lure_type": "воблер",
        "description": "Плавающий воблер минноу, идеально подходящий для твичинга на мелководье. Цель - щука и окунь."
    },
    {
        "brand": "Rapala", "model": "X-Rap 10", "lure_type": "воблер",
        "description": "Тонущий воблер с резкими колебаниями. Эффективен для глубоких каналов и бровок."
    },
    {
        "brand": "Megabass", "model": "Vision 110", "lure_type": "воблер",
        "description": "Плавающий воблер с уникальной игрой при рывках, привлекает активную щуку."
    },
    {
        "brand": "Jackall", "model": "Squad Minnow 128SP", "lure_type": "воблер",
        "description": "Суспендер с шумовыми элементами, эффективен для твичинга на заросших мелководьях."
    },
    {
        "brand": "Lucky Craft", "model": "Pointer 100", "lure_type": "воблер",
        "description": "Суспендер со стабильной игрой, хорош для точечного облова коряжников."
    },
    {
        "brand": "Yo-Zuri", "model": "3D Crank", "lure_type": "воблер",
        "description": "Плавающий кренк с объемным 3D-зрением, подходит для ловли в траве."
    },
    {
        "brand": "Strike Pro", "model": "Hunchback", "lure_type": "воблер",
        "description": "Тонущий воблер с широкой игрой и вибрациями, эффективен на русловых свалах."
    },
    {
        "brand": "Salmo", "model": "Hornet 12F", "lure_type": "воблер",
        "description": "Плавающий воблер с шумовой камерой, устойчив к зацепам."
    },
    {
        "brand": "OSP", "model": "Rudra 130F", "lure_type": "воблер",
        "description": "Крупный плавающий воблер для трофейной щуки, эффективен осенью."
    },
    {
        "brand": "Pontoon21", "model": "Greedy Guts 80SP", "lure_type": "воблер",
        "description": "Компактный суспендер с агрессивной игрой, для ловли в камышах."
    },

    # --- СИЛИКОН ---
    {
        "brand": "Keitech", "model": "Easy Shiner 5\"", "lure_type": "силикон",
        "description": "Универсальная японская приманка из съедобного материала. Эффективна для щуки, судака и окуня."
    },
    {
        "brand": "Fanatik", "model": "Larva Lux", "lure_type": "силикон",
        "description": "Имитация личинки стрекозы. Эффективна при ловле щуки, судака и крупного окуня на джиг."
    },
    {
        "brand": "Lucky John", "model": "Tioga", "lure_type": "силикон",
        "description": "Виброхвост с характерной формой тела, привлекающей хищника с большого расстояния."
    },
    {
        "brand": "Sawamura", "model": "One'Up Shad", "lure_type": "силикон",
        "description": "Виброхвост с уникальной формой, создающей низкочастотные колебания. Отлично подходит для щуки."
    },
    {
        "brand": "Reins", "model": "G-Tail Saturn", "lure_type": "силикон",
        "description": "Червеобразная приманка с твистерным хвостом, идеальна для микроджига и ловли окуня."
    },

    # --- БЛЕСНЫ ---
    {
        "brand": "Mepps", "model": "Aglia Long", "lure_type": "блесна",
        "description": "Вращающаяся блесна с вытянутым лепестком. Универсальна, подходит для облова перекатов и течения."
    },
    {
        "brand": "Mepps", "model": "Black Fury", "lure_type": "блесна",
        "description": "Классическая вращающаяся блесна с черным лепестком, эффективна в мутной воде."
    },
    {
        "brand": "Kuusamo", "model": "Professor", "lure_type": "блесна",
        "description": "Колеблющаяся блесна-незацепляйка, идеальна для ловли щуки в заросших водоемах."
    },
    {
        "brand": "Abu Garcia", "model": "Toby", "lure_type": "блесна",
        "description": "Классическая колебалка с S-образной формой, отлично подходит для ловли лососевых и жереха."
    },
    {
        "brand": "Williams", "model": "Wabler", "lure_type": "блесна",
        "description": "Легендарная колеблющаяся блесна, покрытая драгоценными металлами для лучшего блеска."
    }
]

def import_manual_knowledge(db: Session, lures_to_import: list[dict]):
    """
    Добавляет записи в базу знаний LureKnowledge из предоставленного списка.
    Проверяет на дубликаты по бренду и модели.
    """
    print("--- НАЧАЛО РУЧНОГО ИМПОРТА ЗНАНИЙ ---")
    imported_count = 0
    for lure_data in lures_to_import:
        # Проверка на существование такой же приманки
        exists = db.query(LureKnowledge).filter(
            LureKnowledge.brand == lure_data["brand"],
            LureKnowledge.model == lure_data["model"]
        ).first()
        
        if not exists:
            new_entry = LureKnowledge(
                brand=lure_data["brand"],
                model=lure_data["model"],
                lure_type=lure_data["lure_type"],
                description=lure_data["description"],
                # Делаем URL уникальным, чтобы избежать конфликта в БД
                source_url=f"manual_import_{lure_data['brand'].lower()}_{lure_data['model'].lower().replace(' ', '_')}"
            )
            db.add(new_entry)
            db.commit()
            imported_count += 1
            print(f"  -> Добавлено: {new_entry.brand} {new_entry.model}")
        else:
            print(f"  - Пропуск (уже существует): {lure_data['brand']} {lure_data['model']}")
            
    print(f"\n--- ИМПОРТ ЗАВЕРШЕН. Добавлено {imported_count} новых записей. ---")


if __name__ == '__main__':
    init_db()
    db = SessionLocal()
    try:
        import_manual_knowledge(db, TOP_LURES)
    finally:
        db.close()
