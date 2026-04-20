function formatAll(results, field) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  return results.map(row => '• ' + row.name + ': ' + row[field]).join('\\n');
}

function formatBookings(results) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  return results.map(row => '• ' + row.name + ': ' + row.count + ' (П:' + (row.paid || 0) + ', Б:' + (row.free || 0) + ')').join('\\n');
}

const data = $json;
const text = `📊 ОТЧЕТ ЗА ВЧЕРА - PLEADA
📅 Дата: ${data.yesterday}
🕐 Автоматическая отправка: ${new Date().toLocaleString('ru-RU')}

━━━━━

🎯 ПЕРВЫЕ ВСТРЕЧИ: ${data.firstMeetings.total}
${formatAll(data.firstMeetings.results, 'count')}

🔄 ПОВТОРНЫЕ ВСТРЕЧИ: ${data.secondMeetings.total}
${formatAll(data.secondMeetings.results, 'count')}

📅 НАЗНАЧЕННЫЕ ВСТРЕЧИ: ${data.appointedMeetings.total}
${formatAll(data.appointedMeetings.results, 'count')}

🏠 БРОНИ: ${data.bookings.total}
${formatBookings(data.bookings.results)}

💰 СДЕЛКИ: ${data.deals.total}
${formatAll(data.deals.results, 'count')}

🎯 ЗАЯВКИ ОТ 1 МЛН: ${data.qualifiedLeads.total}
${formatAll(data.qualifiedLeads.results, 'count')}

📝 ВЗЯТЫЕ В РАБОТУ ЗАЯВКИ: ${data.takenLeads.total}
${formatAll(data.takenLeads.results, 'count')}

👥 КЛИЕНТОВ В РАБОТЕ: ${data.clientsInWork.total}

📊━━━━━📈

📈 КРАТКИЕ ИТОГИ:
🎯 Первые встречи: ${data.firstMeetings.total}
🔄 Повторные встречи: ${data.secondMeetings.total}
📅 Назначенные: ${data.appointedMeetings.total}
🏠 Брони: ${data.bookings.total}
💰 Сделки: ${data.deals.total}
🎯 Заявки 1 млн: ${data.qualifiedLeads.total}
📝 Взятые в работу: ${data.takenLeads.total}
👥 Клиентов в работе: ${data.clientsInWork.total}

━━━━━

🤖 Автоматический отчет PLEADA n8n
📊 Ссылка на AmoCRM: https://pleada.amocrm.ru/leads/list/pipeline/437595/`;

return {
  chat_id: '-4807348681',
  text: text,
  disable_web_page_preview: true
};
