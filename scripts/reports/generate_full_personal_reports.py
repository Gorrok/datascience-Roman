#!/usr/bin/env python3
import json

# Список всех экспертов с их chat_id
experts = [
    {"name": "Егор Петров", "chat_id": "-824634764"},
    {"name": "Александр Голубов", "chat_id": "-4153209962"},
    {"name": "Иван Солоненко", "chat_id": "-792923541"},
    {"name": "Максим Прокофьев", "chat_id": "-4653752440"},
    {"name": "Эдуард Осин", "chat_id": "-4615184393"},
    {"name": "Михаил Мордвин", "chat_id": "-4583806767"},
    {"name": "Надежда Данилова", "chat_id": "-4518803988"},
    {"name": "Ульяна Процюк", "chat_id": "-4560907350"},
    {"name": "Юлия Трифонова", "chat_id": "-4611175380"},
    {"name": "Владислав Какорин", "chat_id": "-4681925498"},
    {"name": "Седа Барсегян", "chat_id": "-4617024494"},
    {"name": "Егор Храновский", "chat_id": "-4211864137"},
    {"name": "Анна Савелова", "chat_id": "-4806109676"},
    {"name": "Маргарита Осипова", "chat_id": "-4615703838"}
]

def generate_query_sql(expert_name):
    return f"""SELECT
  (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}') as total_first_meetings,
  (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}') as total_second_meetings,
  (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}') as total_appointed_meetings,
  (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}') as total_bookings,
  (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}') as total_deals,
  (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Dengi_na_rukah >= 1000000 AND ID_statusa NOT IN (142, 143) AND Ima_otvetstvennogo = '{expert_name}') as total_qualified_leads,
  (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}') as total_taken_leads,
  (SELECT COUNT(*) FROM Leads WHERE ID_voronki = 437595 AND CLSD IS NULL AND ID_statusa NOT IN (142, 143) AND Ima_otvetstvennogo = '{expert_name}') as clients_in_work,
  (SELECT CONCAT('[', GROUP_CONCAT(CONCAT('{{\"name\":\"', Ima_otvetstvennogo, '\",\"count\":', cnt, '}}') ORDER BY cnt DESC SEPARATOR ','), ']') FROM (SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}' GROUP BY Ima_otvetstvennogo HAVING cnt > 0 ORDER BY cnt DESC LIMIT 10) t) as first_meetings_json,
  (SELECT CONCAT('[', GROUP_CONCAT(CONCAT('{{\"name\":\"', Ima_otvetstvennogo, '\",\"count\":', cnt, '}}') ORDER BY cnt DESC SEPARATOR ','), ']') FROM (SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}' GROUP BY Ima_otvetstvennogo HAVING cnt > 0 ORDER BY cnt DESC LIMIT 10) t) as second_meetings_json,
  (SELECT CONCAT('[', GROUP_CONCAT(CONCAT('{{\"name\":\"', Ima_otvetstvennogo, '\",\"count\":', cnt, '}}') ORDER BY cnt DESC SEPARATOR ','), ']') FROM (SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}' GROUP BY Ima_otvetstvennogo HAVING cnt > 0 ORDER BY cnt DESC LIMIT 10) t) as appointed_meetings_json,
  (SELECT CONCAT('[', GROUP_CONCAT(CONCAT('{{\"name\":\"', Ima_otvetstvennogo, '\",\"count\":', total_cnt, ',\"paid\":', paid_cnt, ',\"free\":', free_cnt, '}}') ORDER BY total_cnt DESC SEPARATOR ','), ']') FROM (SELECT Ima_otvetstvennogo, COUNT(*) as total_cnt, SUM(CASE WHEN Bron = 'Платная' THEN 1 ELSE 0 END) as paid_cnt, SUM(CASE WHEN Bron = 'Бесплатная' THEN 1 ELSE 0 END) as free_cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}' GROUP BY Ima_otvetstvennogo HAVING total_cnt > 0 ORDER BY total_cnt DESC LIMIT 10) t) as bookings_json,
  (SELECT CONCAT('[', GROUP_CONCAT(CONCAT('{{\"name\":\"', Ima_otvetstvennogo, '\",\"count\":', cnt, '}}') ORDER BY cnt DESC SEPARATOR ','), ']') FROM (SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}' GROUP BY Ima_otvetstvennogo HAVING cnt > 0 ORDER BY cnt DESC LIMIT 10) t) as deals_json,
  (SELECT CONCAT('[', GROUP_CONCAT(CONCAT('{{\"name\":\"', Ima_otvetstvennogo, '\",\"count\":', cnt, '}}') ORDER BY cnt DESC SEPARATOR ','), ']') FROM (SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Dengi_na_rukah >= 1000000 AND ID_statusa NOT IN (142, 143) AND Ima_otvetstvennogo = '{expert_name}' GROUP BY Ima_otvetstvennogo HAVING cnt > 0 ORDER BY cnt DESC LIMIT 10) t) as qualified_leads_json,
  (SELECT CONCAT('[', GROUP_CONCAT(CONCAT('{{\"name\":\"', Ima_otvetstvennogo, '\",\"count\":', cnt, '}}') ORDER BY cnt DESC SEPARATOR ','), ']') FROM (SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo = '{expert_name}' GROUP BY Ima_otvetstvennogo HAVING cnt > 0 ORDER BY cnt DESC LIMIT 10) t) as taken_leads_json"""

def generate_aggregate_code(expert_name):
    safe_name = expert_name.lower().replace(' ', '-')
    return f"""const queryResults = $node["{expert_name} Query"].json;
const now = new Date();
const yesterday = new Date(now);
yesterday.setDate(now.getDate() - 1);
const yesterdayFormatted = yesterday.toLocaleDateString('ru-RU');

const row = Array.isArray(queryResults) ? queryResults[0] : queryResults;

const parseJsonArray = (jsonString) => {{
  try {{
    return jsonString ? JSON.parse(jsonString) : [];
  }} catch (e) {{
    console.log('JSON parse error:', e);
    return [];
  }}
}};

return {{
  yesterday: yesterdayFormatted,
  expert_name: '{expert_name}',
  firstMeetings: {{
    total: parseInt(row.total_first_meetings) || 0,
    results: parseJsonArray(row.first_meetings_json)
  }},
  secondMeetings: {{
    total: parseInt(row.total_second_meetings) || 0,
    results: parseJsonArray(row.second_meetings_json)
  }},
  appointedMeetings: {{
    total: parseInt(row.total_appointed_meetings) || 0,
    results: parseJsonArray(row.appointed_meetings_json)
  }},
  bookings: {{
    total: parseInt(row.total_bookings) || 0,
    results: parseJsonArray(row.bookings_json)
  }},
  deals: {{
    total: parseInt(row.total_deals) || 0,
    results: parseJsonArray(row.deals_json)
  }},
  qualifiedLeads: {{
    total: parseInt(row.total_qualified_leads) || 0,
    results: parseJsonArray(row.qualified_leads_json)
  }},
  takenLeads: {{
    total: parseInt(row.total_taken_leads) || 0,
    results: parseJsonArray(row.taken_leads_json)
  }},
  clientsInWork: {{
    total: parseInt(row.clients_in_work) || 0
  }}
}};"""

def generate_format_code(expert_name, chat_id):
    return f"""function formatAll(results, field) {{
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  return results.map(row => '• ' + row.name + ': ' + row[field]).join('\\n');
}}

function formatBookings(results) {{
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  return results.map(row => '• ' + row.name + ': ' + row.count + ' (платная: ' + row.paid + ', бесплатная: ' + row.free + ')').join('\\n');
}}

function formatPersonalReport(data) {{
  const expertName = '{expert_name}';
  const text = '\\n👤 <b>ЛИЧНЫЙ ОТЧЕТ: ' + expertName + '</b> 👤\\n📅 Дата: ' + data.yesterday + '\\n🕐 Автоматическая отправка: ' + new Date().toLocaleString('ru-RU') + '\\n\\n━━━━━\\n\\n' +
  '<b>🎯 ПЕРВЫЕ ВСТРЕЧИ:</b> <code>' + data.firstMeetings.total + '</code>\\n' +
  formatAll(data.firstMeetings.results, 'count') + '\\n\\n' +
  '<b>🔄 ПОВТОРНЫЕ ВСТРЕЧИ:</b> <code>' + data.secondMeetings.total + '</code>\\n' +
  formatAll(data.secondMeetings.results, 'count') + '\\n\\n' +
  '<b>📅 НАЗНАЧЕННЫЕ ВСТРЕЧИ:</b> <code>' + data.appointedMeetings.total + '</code>\\n' +
  formatAll(data.appointedMeetings.results, 'count') + '\\n\\n' +
  '<b>🏠 БРОНИ:</b> <code>' + data.bookings.total + '</code>\\n' +
  formatBookings(data.bookings.results) + '\\n\\n' +
  '<b>💰 СДЕЛКИ:</b> <code>' + data.deals.total + '</code>\\n' +
  formatAll(data.deals.results, 'count') + '\\n\\n' +
  '<b>🎯 ЗАЯВКИ ОТ 1 МЛН:</b> <code>' + data.qualifiedLeads.total + '</code>\\n' +
  formatAll(data.qualifiedLeads.results, 'count') + '\\n\\n' +
  '<b>📝 ВЗЯТЫЕ В РАБОТУ ЗАЯВКИ:</b> <code>' + data.takenLeads.total + '</code>\\n' +
  formatAll(data.takenLeads.results, 'count') + '\\n\\n' +
  '<b>👥 КЛИЕНТОВ В РАБОТЕ:</b> <code>' + data.clientsInWork.total + '</code>\\n\\n' +
  '━━━━━\\n\\n' +
  '<i>🤖 Личный автоматический отчет n8n</i>\\n' +
  '<a href=\"https://pleada.amocrm.ru/leads/list/pipeline/437595/\">📊 Ссылка на AmoCRM</a>';

  return {{
    chat_id: '{chat_id}',
    text: text,
    parse_mode: 'HTML',
    disable_web_page_preview: true
  }};
}}

const expertData = $json;
return formatPersonalReport(expertData);"""

def generate_node_id(name):
    return name.lower().replace(' ', '-')

# Загружаем базовый workflow
with open('personal_reports_workflow.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Добавляем ноды для всех экспертов
y_offset = -360  # Начинаем с позиции после первого эксперта

for i, expert in enumerate(experts[1:], 1):  # Пропускаем первого эксперта (уже есть в workflow)
    name = expert['name']
    chat_id = expert['chat_id']
    node_id = generate_node_id(name)

    # Query node
    query_node = {
        "parameters": {
            "operation": "executeQuery",
            "query": generate_query_sql(name),
            "options": {}
        },
        "name": f"{name} Query",
        "type": "n8n-nodes-base.mySql",
        "typeVersion": 2.5,
        "position": [680, y_offset + (i-1) * 160],
        "id": f"{node_id}-query",
        "credentials": {
            "mySql": {
                "id": "i9KxH8j4zE5Nq7R",
                "name": "MySQL account"
            }
        }
    }

    # Aggregate node
    aggregate_node = {
        "parameters": {
            "functionCode": generate_aggregate_code(name)
        },
        "name": f"{name} Aggregate",
        "type": "n8n-nodes-base.function",
        "typeVersion": 1,
        "position": [900, y_offset + (i-1) * 160],
        "id": f"{node_id}-aggregate"
    }

    # Format node
    format_node = {
        "parameters": {
            "functionCode": generate_format_code(name, chat_id)
        },
        "name": f"Format {name} Report",
        "type": "n8n-nodes-base.function",
        "typeVersion": 1,
        "position": [1120, y_offset + (i-1) * 160],
        "id": f"format-{node_id}-report"
    }

    # Send node
    send_node = {
        "parameters": {
            "method": "POST",
            "url": "https://api.telegram.org/bot7816133059:AAFglo-EXpUBOVD8jMCbJadfR1EaFaLxB_A/sendMessage",
            "sendBody": True,
            "bodyContentType": "json",
            "body": "={{ $json }}"
        },
        "name": f"Send {name} Report",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.1,
        "position": [1340, y_offset + (i-1) * 160],
        "id": f"send-{node_id}-report"
    }

    # Добавляем ноды в workflow
    workflow['nodes'].extend([query_node, aggregate_node, format_node, send_node])

    # Добавляем connections
    workflow['connections'][f"{name} Query"] = {
        "main": [[{"node": f"{name} Aggregate", "type": "main", "index": 0}]]
    }
    workflow['connections'][f"{name} Aggregate"] = {
        "main": [[{"node": f"Format {name} Report", "type": "main", "index": 0}]]
    }
    workflow['connections'][f"Format {name} Report"] = {
        "main": [[{"node": f"Send {name} Report", "type": "main", "index": 0}]]
    }

    # Добавляем в Schedule Trigger connections
    workflow['connections']["Schedule Trigger"]["main"][0].append({
        "node": f"{name} Query",
        "type": "main",
        "index": 0
    })

# Сохраняем полный workflow
with open('full_personal_reports_workflow.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, ensure_ascii=False, indent=2)

print(f"✅ Создан полный workflow с {len(experts)} экспертами")
print(f"📊 Всего нод: {len(workflow['nodes'])}")
print(f"🔗 Connections: {len(workflow['connections'])} связей")