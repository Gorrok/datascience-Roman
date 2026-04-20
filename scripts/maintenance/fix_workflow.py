#!/usr/bin/python3
import re

# Читаем файл
with open('daily_groups_reports_workflow.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем все ссылки на $node["Name"].json на $json
content = content.replace('const groupData = $node[\\"LUCH Group Data\\"].json;', 'const groupData = $json;')
content = content.replace('const groupData = $node[\\"MAXIMUM Group Data\\"].json;', 'const groupData = $json;')
content = content.replace('const groupData = $node[\\"MORE Group Data\\"].json;', 'const groupData = $json;')

# Записываем обратно
with open('daily_groups_reports_workflow.json', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Замена выполнена')