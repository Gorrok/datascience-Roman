# -*- coding: utf-8 -*-
import sys

# Добавляем корневую директорию проекта в sys.path
sys.path.append('.')

from database.database import SessionLocal
from inventory.inventory_manager import add_lure, list_inventory, remove_lure

def print_menu():
    """Выводит главное меню."""
    print("\n--- МЕНЕДЖЕР ИНВЕНТАРЯ ---")
    print("1. Показать все приманки")
    print("2. Добавить новую приманку")
    print("3. Удалить приманку")
    print("4. Выйти")

def show_all_lures():
    """Показывает все приманки из инвентаря."""
    db = SessionLocal()
    try:
        inventory = list_inventory(db)
        if not inventory:
            print("\n>> Инвентарь пуст.")
        else:
            print("\n--- ВАШ АРСЕНАЛ ---")
            for lure in inventory:
                details = f"ID: {lure.id}, {lure.brand.capitalize()} {lure.model.capitalize()} ({lure.lure_type})"
                if lure.size: details += f", Размер: {lure.size}"
                if lure.color: details += f", Цвет: {lure.color}"
                if lure.weight: details += f", Вес: {lure.weight}г"
                print(details)
    finally:
        db.close()

def add_new_lure():
    """Запрашивает у пользователя информацию и добавляет новую приманку."""
    db = SessionLocal()
    try:
        print("\n--- ДОБАВЛЕНИЕ НОВОЙ ПРИМАНКИ ---")
        lure_type = input("Тип приманки (воблер, блесна, силикон): ").strip()
        brand = input("Бренд: ").strip()
        model = input("Модель: ").strip()

        if not all([lure_type, brand, model]):
            print("\n>> Ошибка: Тип, Бренд и Модель являются обязательными полями.")
            return

        # Дополнительные, необязательные параметры
        kwargs = {}
        size = input("Размер (опционально): ").strip()
        if size: kwargs['size'] = size
        
        color = input("Цвет (опционально): ").strip()
        if color: kwargs['color'] = color
        
        weight_str = input("Вес в граммах (опционально): ").strip()
        if weight_str:
            try:
                kwargs['weight'] = float(weight_str)
            except ValueError:
                print(">> Вес должен быть числом.")

        quantity_str = input("Количество (опционально, по умолчанию 1): ").strip()
        if quantity_str:
            try:
                kwargs['quantity'] = int(quantity_str)
            except ValueError:
                print(">> Количество должно быть целым числом.")

        add_lure(db, lure_type=lure_type, brand=brand, model=model, **kwargs)

    finally:
        db.close()

def delete_lure():
    """Запрашивает ID и удаляет приманку."""
    db = SessionLocal()
    try:
        lure_id_str = input("\nВведите ID приманки для удаления: ").strip()
        if not lure_id_str.isdigit():
            print(">> ID должен быть числом.")
            return
        
        remove_lure(db, int(lure_id_str))
    finally:
        db.close()


def main():
    """Основной цикл программы."""
    while True:
        print_menu()
        choice = input("Выберите действие (1-4): ").strip()

        if choice == '1':
            show_all_lures()
        elif choice == '2':
            add_new_lure()
        elif choice == '3':
            delete_lure()
        elif choice == '4':
            print("Выход...")
            break
        else:
            print("\n>> Неверный выбор. Пожалуйста, введите число от 1 до 4.")

if __name__ == '__main__':
    main()
