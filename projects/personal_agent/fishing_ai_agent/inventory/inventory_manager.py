# -*- coding: utf-8 -*-
import sys
from sqlalchemy.orm import Session
import os

# Добавляем корневую директорию проекта в sys.path
# sys.path.append('.')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from database.database import SessionLocal
from database.models import Lure

def add_lure(db: Session, lure_type: str, brand: str, model: str, **kwargs) -> Lure:
    """
    Добавляет новую приманку в инвентарь (базу данных).

    Args:
        db: Сессия базы данных.
        lure_type: Тип приманки (воблер, блесна и т.д.).
        brand: Бренд приманки.
        model: Модель приманки.
        **kwargs: Дополнительные параметры (size, weight, color, quantity, condition).

    Returns:
        Созданный объект Lure.
    """
    new_lure = Lure(
        lure_type=lure_type.lower(),
        brand=brand.lower(),
        model=model.lower(),
        **kwargs
    )
    db.add(new_lure)
    db.commit()
    db.refresh(new_lure)
    print(f"✅ Добавлена приманка: {brand.capitalize()} {model.capitalize()} (ID: {new_lure.id})")
    return new_lure

def list_inventory(db: Session) -> list[Lure]:
    """
    Возвращает список всех приманок в инвентаре.

    Args:
        db: Сессия базы данных.

    Returns:
        Список объектов Lure.
    """
    return db.query(Lure).all()

def remove_lure(db: Session, lure_id: int) -> bool:
    """
    Удаляет приманку из инвентаря по её ID.

    Args:
        db: Сессия базы данных.
        lure_id: ID приманки для удаления.

    Returns:
        True, если удаление прошло успешно, иначе False.
    """
    lure_to_delete = db.query(Lure).filter(Lure.id == lure_id).first()
    if lure_to_delete:
        db.delete(lure_to_delete)
        db.commit()
        print(f"❌ Удалена приманка с ID: {lure_id}")
        return True
    print(f"⚠️ Приманка с ID: {lure_id} не найдена.")
    return False

if __name__ == '__main__':
    # Пример использования
    db = SessionLocal()
    try:
        print("--- УПРАВЛЕНИЕ ИНВЕНТАРЕМ ---")

        # Добавим несколько приманок
        add_lure(db, lure_type='воблер', brand='Megabass', model='Vision 110', color='mat tiger', size='110mm')
        add_lure(db, lure_type='силикон', brand='Keitech', model='Easy Shiner', size='4"', quantity=5)
        add_lure(db, lure_type='колебалка', brand='Mepps', model='Syclops', weight=12.5)

        print("\n--- ТЕКУЩИЙ ИНВЕНТАРЬ ---")
        inventory = list_inventory(db)
        if not inventory:
            print("Инвентарь пуст.")
        else:
            for lure in inventory:
                print(f"  - ID: {lure.id}, {lure.brand.capitalize()} {lure.model.capitalize()} ({lure.lure_type})")
        
        print("\n--- ТЕСТ УДАЛЕНИЯ ---")
        # Попробуем удалить одну из приманок (например, с ID 2)
        if inventory and len(inventory) > 1:
            remove_lure(db, inventory[1].id)
        
        print("\n--- ИНВЕНТАРЬ ПОСЛЕ УДАЛЕНИЯ ---")
        new_inventory = list_inventory(db)
        for lure in new_inventory:
            print(f"  - ID: {lure.id}, {lure.brand.capitalize()} {lure.model.capitalize()} ({lure.lure_type})")

    finally:
        db.close()
