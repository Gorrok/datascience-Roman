function formatAll(results, field) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  // Данные уже отсортированы по count DESC в Python, просто форматируем
  return results.map(row => '• ' + row.name + ': ' + row[field]).join('\\n');
}

function formatBookings(results) {
  if (!results || !Array.isArray(results) || results.length === 0) return '';
  // Данные уже отсортированы по count DESC в Python, просто форматируем
  return results.map(row => '• ' + row.name + ': ' + row.count + ' (П:' + (row.paid || 0) + ', Б:' + (row.free || 0) + ')').join('\\n');
}

function formatGroupReport(data) {
  const teamEmoji = {
    'ЛУЧ': '⭐',
    'MAXIMUM': '💎',
    'MORE': '🔥'
  };

  const emoji = teamEmoji[data.team_name] || '📊';

  const text = `\\n${emoji} <b>ЕЖЕДНЕВНЫЙ ОТЧЕТ ГРУППЫ ${data.team_name}</b> ${emoji}\\n📅 Дата: ${data.yesterday}\\n🕐 Автоматическая отправка: ${new Date().toLocaleString('ru-RU')}\\n\\n━━━━━\\n\\n` +

  `<b>🎯 ПЕРВЫЕ ВСТРЕЧИ:</b> <code>${data.total_first_meetings}</code>\\n` +
  `${formatAll(data.first_meetings, 'count')}\\n\\n` +

  `<b>🔄 ПОВТОРНЫЕ ВСТРЕЧИ:</b> <code>${data.total_second_meetings}</code>\\n` +
  `${formatAll(data.second_meetings, 'count')}\\n\\n` +

  `<b>📅 НАЗНАЧЕННЫЕ ВСТРЕЧИ:</b> <code>${data.total_appointed_meetings}</code>\\n` +
  `${formatAll(data.appointed_meetings, 'count')}\\n\\n` +

  `<b>🏠 БРОНИ:</b> <code>${data.total_bookings}</code>\\n` +
  `${formatBookings(data.bookings)}\\n\\n` +

  `<b>💰 СДЕЛКИ:</b> <code>${data.total_deals}</code>\\n` +
  `${formatAll(data.deals, 'count')}\\n\\n` +

  `<b>🎯 ЗАЯВКИ ОТ 1 МЛН:</b> <code>${data.total_qualified_leads}</code>\\n` +
  `${formatAll(data.qualified_leads, 'count')}\\n\\n` +

  `<b>📝 ВЗЯТЫЕ В РАБОТУ ЗАЯВКИ:</b> <code>${data.total_taken_leads}</code>\\n` +
  `${formatAll(data.taken_leads, 'count')}\\n\\n` +

  `<b>👥 КЛИЕНТОВ В РАБОТЕ:</b> <code>${data.clients_in_work}</code>\\n\\n` +

  `📊━━━━━📈\\n\\n<b>📈 КРАТКИЕ ИТОГИ:</b>\\n` +
  `🎯 Первые встречи: ${data.total_first_meetings}\\n` +
  `🔄 Повторные встречи: ${data.total_second_meetings}\\n` +
  `📅 Назначенные: ${data.total_appointed_meetings}\\n` +
  `🏠 Брони: ${data.total_bookings}\\n` +
  `💰 Сделки: ${data.total_deals}\\n` +
  `🎯 Заявки 1 млн: ${data.total_qualified_leads}\\n` +
  `📝 Взятые в работу: ${data.total_taken_leads}\\n` +
  `👥 Клиентов в работе: ${data.clients_in_work}\\n\\n` +

  `━━━━━\\n\\n` +
  `<i>🤖 Автоматический отчет группы ${data.team_name} n8n</i>\\n` +
  `<a href="https://pleada.amocrm.ru/leads/list/pipeline/437595/">📊 Ссылка на AmoCRM</a>`;

  return {
    chat_id: data.chat_id,
    text: text,
    parse_mode: 'HTML',
    disable_web_page_preview: true
  };
}

// Для n8n - обработка данных из Python
const groupData = $node["Group Report Data"].json;

return formatGroupReport(groupData);