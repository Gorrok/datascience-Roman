#!/usr/bin/env python3
import json

# Загружаем workflow
with open('full_personal_reports_workflow_fixed.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Исправляем все Format ноды
for node in workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.function' and 'Format' in node['name'] and 'Report' in node['name']:
        # Получаем текущий код
        code = node['parameters']['functionCode']

        # Исправляем экранированные символы
        code = code.replace('\\n', '\n')
        code = code.replace("\\'", "'")

        # Сохраняем исправленный код
        node['parameters']['functionCode'] = code

# Сохраняем исправленный workflow
with open('full_personal_reports_final.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, ensure_ascii=False, indent=2)

print('✅ Исправлены экранированные кавычки во всех Format нодах')
print('📁 Создан файл: full_personal_reports_final.json')