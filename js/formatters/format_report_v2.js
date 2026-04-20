function formatAll(results, field) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  // Показываем максимум 10 менеджеров, отсортированных по count DESC
  const sorted = results.sort((a, b) => (b[field] || 0) - (a[field] || 0));
  return sorted.slice(0, 10).map(row => '• ' + row.Ima_otvetstvennogo + ': ' + row[field]).join('\\n');
}

function formatBookings(results) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  // Показываем максимум 10 менеджеров, отсортированных по count DESC
  const sorted = results.sort((a, b) => (b.count || 0) - (a.count || 0));
  return sorted.slice(0, 10).map(row => '• ' + row.Ima_otvetstvennogo + ': ' + row.count + ' (П:' + (row.booking_details ? row.booking_details.split(',')[0].split(':')[1] : '0') + ', Б:' + (row.booking_details ? row.booking_details.split(',')[1].split(':')[1] : '0') + ')').join('\\n');
}

const data = $json;
const html = '\\n✨ <b>📊 ОТЧЕТ ЗА ВЧЕРА - PLEADA</b> ✨\\n📅 Дата: ' + data.yesterday + '\\n🕐 Автоматическая отправка: ' + new Date().toLocaleString('ru-RU') + '\\n\\n━━━━━\\n\\n' +
'<b>🎯 ПЕРВЫЕ ВСТРЕЧИ:</b> <code>' + data.firstMeetings.total + '</code>\\n' + formatAll(data.firstMeetings.results, 'count') + '\\n' +
'<b>🔄 ПОВТОРНЫЕ ВСТРЕЧИ:</b> <code>' + data.secondMeetings.total + '</code>\\n' + formatAll(data.secondMeetings.results, 'count') + '\\n' +
'<b>📅 НАЗНАЧЕННЫЕ ВСТРЕЧИ:</b> <code>' + data.appointedMeetings.total + '</code>\\n' + formatAll(data.appointedMeetings.results, 'count') + '\\n' +
'<b>🏠 БРОНИ:</b> <code>' + data.bookings.total + '</code>\\n' + formatBookings(data.bookings.results) + '\\n' +
'<b>💰 СДЕЛКИ:</b> <code>' + data.deals.total + '</code>\\n' + formatAll(data.deals.results, 'count') + '\\n' +
'<b>🎯 ЗАЯВКИ ОТ 1 МЛН:</b> <code>' + data.qualifiedLeads.total + '</code>\\n' + formatAll(data.qualifiedLeads.results, 'count') + '\\n' +
'<b>📝 ВЗЯТЫЕ В РАБОТУ ЗАЯВКИ:</b> <code>' + data.takenLeads.total + '</code>\\n' + formatAll(data.takenLeads.results, 'count') + '\\n' +
'<b>👥 КЛИЕНТОВ В РАБОТЕ:</b> <code>' + data.clientsInWork.total + '</code>\\n\\n' +
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
