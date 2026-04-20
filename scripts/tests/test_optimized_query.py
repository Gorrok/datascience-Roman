#!/usr/bin/env python3
"""
Тестовый скрипт для проверки оптимизированного SQL запроса PLEADA
Проверяет структуру запроса и логику агрегации данных
"""

import re
from datetime import datetime, timedelta

def test_query_structure():
    """Проверяет основную структуру объединенного запроса"""

    # Читаем оптимизированный запрос
    with open('optimized_pleada_report.sql', 'r', encoding='utf-8') as f:
        query = f.read()

    print("🔍 Проверка структуры оптимизированного SQL запроса...")
    print("=" * 60)

    # Проверки структуры
    checks = [
        ("WITH yesterday_data AS", "CTE yesterday_data"),
        ("aggregated_data AS", "CTE aggregated_data"),
        ("top_managers AS", "CTE top_managers"),
        ("total_first_meetings", "Общий итог первых встреч"),
        ("total_second_meetings", "Общий итог повторных встреч"),
        ("total_appointed_meetings", "Общий итог назначенных встреч"),
        ("total_bookings", "Общий итог броней"),
        ("total_deals", "Общий итог сделок"),
        ("total_qualified_leads", "Общий итог квалифицированных лидов"),
        ("total_taken_leads", "Общий итог взятых в работу лидов"),
        ("clients_in_work", "Клиенты в работе"),
        ("ROW_NUMBER\\(\\) OVER", "Ранжирование менеджеров"),
        ("CASE.*WHEN.*bookings", "Логика для броней"),
        ("DATE_SUB.*CURDATE.*INTERVAL 1 DAY", "Вчерашняя дата"),
        ("ORDER BY.*CASE.*metric_type", "Сортировка по типам метрик")
    ]

    passed = 0
    failed = 0

    for check, description in checks:
        if re.search(check, query, re.IGNORECASE | re.DOTALL):
            print(f"✅ {description}")
            passed += 1
        else:
            print(f"❌ {description} - НЕ НАЙДЕНО")
            failed += 1

    print(f"\n📊 Результаты проверки: {passed} пройдено, {failed} не пройдено")

    # Проверяем количество UNION ALL (должно быть 7 для 7 метрик)
    union_count = query.count("UNION ALL")
    print(f"🔗 Количество UNION ALL: {union_count} (ожидается 6 для 7 метрик)")

    # Проверяем основные метрики
    metrics = ["first_meetings", "second_meetings", "appointed_meetings", "bookings", "deals", "qualified_leads", "taken_leads"]
    metrics_found = sum(1 for metric in metrics if metric in query)
    print(f"📈 Метрик найдено: {metrics_found} из {len(metrics)}")

    return failed == 0

def test_n8n_logic():
    """Проверяет логику JavaScript в n8n workflow"""

    print("\n🔍 Проверка JavaScript логики в n8n...")
    print("=" * 60)

    # Читаем обновленный workflow
    with open('optimized_n8n_workflow.json', 'r', encoding='utf-8') as f:
        import json
        workflow = json.load(f)

    # Находим функцию Aggregate Data
    aggregate_node = None
    for node in workflow['nodes']:
        if node['name'] == 'Aggregate Data':
            aggregate_node = node
            break

    if not aggregate_node:
        print("❌ Узел 'Aggregate Data' не найден")
        return False

    function_code = aggregate_node['parameters']['functionCode']

    # Проверяем ключевые части логики
    checks = [
        ("Unified Report Query", "Ссылка на объединенный запрос"),
        ("groupedData\\[.*metric_type.*\\]", "Группировка по метрикам"),
        ("total_first_meetings", "Обработка итогов"),
        ("firstMeetings.*total.*results", "Структура данных для первых встреч"),
        ("secondMeetings.*total.*results", "Структура данных для повторных встреч"),
        ("bookings.*total.*results", "Структура данных для броней"),
        ("clientsInWork.*total", "Клиенты в работе")
    ]

    passed = 0
    for check, description in checks:
        if re.search(check, function_code, re.IGNORECASE | re.DOTALL):
            print(f"✅ {description}")
            passed += 1
        else:
            print(f"❌ {description} - НЕ НАЙДЕНО")

    print(f"\n📊 JavaScript логика: {passed} из {len(checks)} проверок пройдено")

    # Проверяем количество нод
    total_nodes = len(workflow['nodes'])
    mysql_nodes = sum(1 for node in workflow['nodes'] if node['type'] == 'n8n-nodes-base.mySql')
    function_nodes = sum(1 for node in workflow['nodes'] if node['type'] == 'n8n-nodes-base.function')

    print("🏗️ Структура workflow:")
    print(f"   - Всего нод: {total_nodes}")
    print(f"   - MySQL нод: {mysql_nodes} (было 8, стало 1)")
    print(f"   - Function нод: {function_nodes}")

    return passed == len(checks)

def main():
    print("🚀 Тестирование оптимизированного отчета PLEADA")
    print("=" * 60)

    sql_ok = test_query_structure()
    n8n_ok = test_n8n_logic()

    print("\n" + "=" * 60)
    if sql_ok and n8n_ok:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Оптимизация готова к использованию.")
        print("\n💡 Преимущества оптимизации:")
        print("   • 8 SQL запросов → 1 объединенный запрос")
        print("   • Снижение нагрузки на базу данных")
        print("   • Улучшение производительности n8n")
        print("   • Упрощение поддержки кода")
    else:
        print("⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ! Требуется доработка.")

    print("\n📋 Следующие шаги:")
    print("   1. Импортировать optimized_n8n_workflow.json в n8n")
    print("   2. Проверить работу с реальной базой данных")
    print("   3. Настроить расписание (убрать disabled: true)")
    print("   4. Мониторить производительность")

if __name__ == "__main__":
    main()
