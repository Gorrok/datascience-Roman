function formatAll(results, field) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  // Данные уже отсортированы по count DESC в SQL, просто форматируем
  return results.map(row => '• ' + row.name + ': ' + row[field]).join('\\n');
}

function formatBookings(results) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  // Данные уже отсортированы по count DESC в SQL, просто форматируем
  return results.map(row => '• ' + row.name + ': ' + row.count + ' (П:' + (row.paid || 0) + ', Б:' + (row.free || 0) + ')').join('\\n');
}

function formatSection(title, total, content) {
  const listContent = content ? '\\n' + content : '';
  return '<b>' + title + ':</b> <code>' + total + '</code>' + listContent + '\\n';
}

const data = $json;
const html = '\\n✨ <b>📊 ОТЧЕТ ЗА ВЧЕРА - PLEADA</b> ✨\\n📅 Дата: ' + data.yesterday + '\\n🕐 Автоматическая отправка: ' + new Date().toLocaleString('ru-RU') + '\\n\\n━━━━━\\n\\n' +
formatSection('🎯 ПЕРВЫЕ ВСТРЕЧИ', data.firstMeetings.total, formatAll(data.firstMeetings.results, 'count')) +
formatSection('🔄 ПОВТОРНЫЕ ВСТРЕЧИ', data.secondMeetings.total, formatAll(data.secondMeetings.results, 'count')) +
formatSection('📅 НАЗНАЧЕННЫЕ ВСТРЕЧИ', data.appointedMeetings.total, formatAll(data.appointedMeetings.results, 'count')) +
formatSection('🏠 БРОНИ', data.bookings.total, formatBookings(data.bookings.results)) +
formatSection('💰 СДЕЛКИ', data.deals.total, formatAll(data.deals.results, 'count')) +
formatSection('🎯 ЗАЯВКИ ОТ 1 МЛН', data.qualifiedLeads.total, formatAll(data.qualifiedLeads.results, 'count')) +
formatSection('📝 ВЗЯТЫЕ В РАБОТУ ЗАЯВКИ', data.takenLeads.total, formatAll(data.takenLeads.results, 'count')) +
formatSection('👥 КЛИЕНТОВ В РАБОТЕ', data.clientsInWork.total, '') +
'📊━━━━━📈\\n\\n<b>📈 КРАТКИЕ ИТОГИ:</b>\\n' +
'🎯 Первые встречи: ' + data.firstMeetings.total + '\\n' +
'🔄 Повторные встречи: ' + data.secondMeetings.total + '\\n' +
'📅 Назначенные: ' + data.appointedMeetings.total + '\\n' +
'🏠 Брони: ' + data.bookings.total + '\\n' +
'💰 Сделки: ' + data.deals.total + '\\n' +
'🎯 Заявки 1 млн: ' + data.qualifiedLeads.total + '\\n' +
'📝 Взятые в работу: ' + data.takenLeads.total + '\\n' +
'👥 Клиентов в работе: ' + data.clientsInWork.total + '\\n\\n' +
'━━━━━\\n\\n' +
'<i>🤖 Автоматический отчет PLEADA n8n</i>\\n' +
'<a href=\"https://pleada.amocrm.ru/leads/list/pipeline/437595/\">📊 Ссылка на AmoCRM</a>';

return {
  chat_id: '-4807348681',
  text: html,
  parse_mode: 'HTML',
  disable_web_page_preview: true
};
