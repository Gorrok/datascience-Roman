# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

# Добавляем корневую директорию проекта в sys.path
sys.path.append('.')

from database.database import SessionLocal
from database.models import Lure, WaterBody, FishingSession, Catch

def add_or_get_water_body(db: Session, name: str, body_type: str = None, location: str = None) -> WaterBody:
    """
    Добавляет новый водоем, если он не существует, или возвращает существующий.
    """
    body = db.query(WaterBody).filter(func.lower(WaterBody.name) == name.lower()).first()
    if not body:
        body = WaterBody(name=name, type=body_type, location=location)
        db.add(body)
        db.commit()
        db.refresh(body)
        print(f"✅ Добавлен новый водоем: {name}")
    return body

def start_session(db: Session, water_body_id: int, weather: str = None, notes: str = None) -> FishingSession:
    """
    Начинает новую рыболовную сессию.
    """
    session = FishingSession(
        water_body_id=water_body_id,
        weather_conditions=weather,
        notes=notes
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    print(f"🎣 Начата новая рыболовная сессия (ID: {session.id}) на водоеме ID: {water_body_id}")
    return session

def log_catch(db: Session, session_id: int, lure_id: int, fish_type: str, size_cm: float = None, weight_kg: float = None) -> Catch:
    """
    Логирует пойманную рыбу в рамках сессии.
    """
    catch = Catch(
        session_id=session_id,
        lure_id=lure_id,
        fish_type=fish_type.capitalize(),
        size_cm=size_cm,
        weight_kg=weight_kg
    )
    db.add(catch)
    db.commit()
    db.refresh(catch)
    print(f"🐟 Записан улов: {fish_type.capitalize()} на приманку ID: {lure_id} (Сессия ID: {session_id})")
    return catch

def get_session_catches(db: Session, session_id: int) -> list[Catch]:
    """
    Возвращает все уловы для указанной сессии.
    """
    return db.query(Catch).filter(Catch.session_id == session_id).all()

def list_sessions(db: Session):
    """
    Выводит информацию о всех рыболовных сессиях.
    """
    return db.query(FishingSession).all()


if __name__ == '__main__':
    db = SessionLocal()
    try:
        print("--- ЛОГИРОВАНИЕ РЫБАЛКИ ---")

        # 1. Добавляем водоем
        water_body = add_or_get_water_body(db, name="Ока", body_type="река", location="Московская область")

        # 2. Получаем первую попавшуюся приманку из инвентаря для теста
        lure = db.query(Lure).first()
        if not lure:
            print("⚠️ В инвентаре нет приманок. Добавьте их через inventory_manager.py")
            # Для теста добавим одну, если инвентарь пуст
            from inventory.inventory_manager import add_lure
            lure = add_lure(db, lure_type='воблер', brand='Megabass', model='Vision 110', color='mat tiger')

        # 3. Начинаем сессию
        session = start_session(db, water_body_id=water_body.id, weather="Пасмурно, +15C, ветер 5 м/с")

        # 4. Логируем несколько уловов
        log_catch(db, session_id=session.id, lure_id=lure.id, fish_type="Щука", size_cm=55, weight_kg=1.2)
        log_catch(db, session_id=session.id, lure_id=lure.id, fish_type="Окунь", size_cm=25)

        print("\n--- СТАТИСТИКА СЕССИИ ---")
        catches = get_session_catches(db, session.id)
        session_info = db.query(FishingSession).filter(FishingSession.id == session.id).first()
        
        print(f"Сессия ID: {session.id} на водоеме: {session_info.water_body.name}")
        print(f"Погода: {session_info.weather_conditions}")
        print("Уловы:")
        for c in catches:
            print(f"  - {c.fish_type}, {c.size_cm} см, поймана на {c.lure.brand} {c.lure.model}")

    finally:
        db.close()
