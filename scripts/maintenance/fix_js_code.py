#!/usr/bin/env python3
import json

# Загружаем workflow
with open('full_personal_reports_final_fixed.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Шаблон JavaScript кода с правильными кавычками
template_code = '''function formatAll(results, field) {
  if (!results || !Array.isArray(results) || results.length === 0) return "";
  return results.map(row => "• " + row.name + ": " + row[field]).join("\\n");
}

function formatBookings(results) {
  if (!results || !Array.isArray(results) || results.length === 0) return "";
  return results.map(row => "• " + row.name + ": " + row.count + " (платная: " + row.paid + ", бесплатная: " + row.free + ")").join("\\n");
}

function formatPersonalReport(data) {
  const expertName = "EXPERT_NAME_PLACEHOLDER";
  const text = "\\n👤 <b>ЛИЧНЫЙ ОТЧЕТ: " + expertName + "</b> 👤\\n📅 Дата: " + data.yesterday + "\\n🕐 Автоматическая отправка: " + new Date().toLocaleString("ru-RU") + "\\n\\n━━━━━\\n\\n" +
    "<b>🎯 ПЕРВЫЕ ВСТРЕЧИ:</b> <code>" + data.firstMeetings.total + "</code>\\n" +
    formatAll(data.firstMeetings.results, "count") + "\\n\\n" +
    "<b>🔄 ПОВТОРНЫЕ ВСТРЕЧИ:</b> <code>" + data.secondMeetings.total + "</code>\\n" +
    formatAll(data.secondMeetings.results, "count") + "\\n\\n" +
    "<b>📅 НАЗНАЧЕННЫЕ ВСТРЕЧИ:</b> <code>" + data.appointedMeetings.total + "</code>\\n" +
    formatAll(data.appointedMeetings.results, "count") + "\\n\\n" +
    "<b>🏠 БРОНИ:</b> <code>" + data.bookings.total + "</code>\\n" +
    formatBookings(data.bookings.results) + "\\n\\n" +
    "<b>💰 СДЕЛКИ:</b> <code>" + data.deals.total + "</code>\\n" +
    formatAll(data.deals.results, "count") + "\\n\\n" +
    "<b>🎯 ЗАЯВКИ ОТ 1 МЛН:</b> <code>" + data.qualifiedLeads.total + "</code>\\n" +
    formatAll(data.qualifiedLeads.results, "count") + "\\n\\n" +
    "<b>📝 ВЗЯТЫЕ В РАБОТУ ЗАЯВКИ:</b> <code>" + data.takenLeads.total + "</code>\\n" +
    formatAll(data.takenLeads.results, "count") + "\\n\\n" +
    "<b>👥 КЛИЕНТОВ В РАБОТЕ:</b> <code>" + data.clientsInWork.total + "</code>\\n\\n" +
    "━━━━━\\n\\n" +
    "<i>🤖 Личный автоматический отчет n8n</i>\\n" +
    "<a href=\\"https://pleada.amocrm.ru/leads/list/pipeline/437595/\\">📊 Ссылка на AmoCRM</a>";

  return {
    chat_id: "CHAT_ID_PLACEHOLDER",
    text: text,
    parse_mode: "HTML",
    disable_web_page_preview: true
  };
}

const expertData = $json;
return formatPersonalReport(expertData);'''

# Список экспертов с их данными
experts_data = {
    'Егор Петров': {'name': 'Егор Петров', 'chat_id': '-824634764'},
    'Александр Голубов': {'name': 'Александр Голубов', 'chat_id': '-4153209962'},
    'Иван Солоненко': {'name': 'Иван Солоненко', 'chat_id': '-792923541'},
    'Максим Прокофьев': {'name': 'Максим Прокофьев', 'chat_id': '-4653752440'},
    'Эдуард Осин': {'name': 'Эдуард Осин', 'chat_id': '-4615184393'},
    'Михаил Мордвин': {'name': 'Михаил Мордвин', 'chat_id': '-4583806767'},
    'Надежда Данилова': {'name': 'Надежда Данилова', 'chat_id': '-4518803988'},
    'Ульяна Процюк': {'name': 'Ульяна Процюк', 'chat_id': '-4560907350'},
    'Юлия Трифонова': {'name': 'Юлия Трифонова', 'chat_id': '-4611175380'},
    'Владислав Какорин': {'name': 'Владислав Какорин', 'chat_id': '-4681925498'},
    'Седа Барсегян': {'name': 'Седа Барсегян', 'chat_id': '-4617024494'},
    'Егор Храновский': {'name': 'Егор Храновский', 'chat_id': '-4211864137'},
    'Анна Савелова': {'name': 'Анна Савелова', 'chat_id': '-4806109676'},
    'Маргарита Осипова': {'name': 'Маргарита Осипова', 'chat_id': '-4615703838'}
}

# Исправляем все Format ноды
for node in workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.function' and 'Format' in node['name'] and 'Report' in node['name']:
        # Определяем имя эксперта из названия ноды
        node_name = node['name']
        expert_name = node_name.replace('Format ', '').replace(' Report', '')

        if expert_name in experts_data:
            expert_data = experts_data[expert_name]
            # Заменяем placeholders в шаблоне
            custom_code = template_code.replace('EXPERT_NAME_PLACEHOLDER', expert_data['name'])
            custom_code = custom_code.replace('CHAT_ID_PLACEHOLDER', expert_data['chat_id'])
            node['parameters']['functionCode'] = custom_code

# Сохраняем исправленный workflow
with open('full_personal_reports_final_js_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, ensure_ascii=False, indent=2)

print('✅ Полностью переписан JavaScript код в Format нодах')
print('📁 Создан файл: full_personal_reports_final_js_fixed.json')