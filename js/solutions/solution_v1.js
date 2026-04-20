const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Гарантируем, что queryResults является массивом
const resultsArray = Array.isArray(queryResults) ? queryResults : [queryResults];

// Получаем totals из первой строки (они одинаковые во всех строках)
const firstRow = resultsArray[0] || {};
const totals = {
  total_first_meetings: parseInt(firstRow.total_first_meetings) || 0,
  total_second_meetings: parseInt(firstRow.total_second_meetings) || 0,
  total_appointed_meetings: parseInt(firstRow.total_appointed_meetings) || 0,
  total_bookings: parseInt(firstRow.total_bookings) || 0,
  total_deals: parseInt(firstRow.total_deals) || 0,
  total_qualified_leads: parseInt(firstRow.total_qualified_leads) || 0,
  total_taken_leads: parseInt(firstRow.total_taken_leads) || 0,
  clients_in_work: parseInt(firstRow.clients_in_work) || 0
};

// Группируем все строки по metric_type, пропуская только те, где metric_type пустое/null
const metrics = {};
resultsArray.forEach((row) => {
  // Проверяем, что metric_type существует и не пустое
  const metricType = row.metric_type;
  if (metricType && metricType.trim() !== '' && metricType !== 'null' && metricType !== null) {
    if (!metrics[metricType]) {
      metrics[metricType] = [];
    }
    metrics[metricType].push({
      Ima_otvetstvennogo: row.Ima_otvetstvennogo,
      count: parseInt(row.count_value) || 0,
      booking_details: row.booking_details
    });
  }
});

// Для отладки - выводим информацию
console.log('Total rows processed:', resultsArray.length);
console.log('Metrics found:', Object.keys(metrics));
console.log('Sample first_meetings:', metrics.first_meetings?.length || 0);

return {
  yesterday,
  firstMeetings: { total: totals.total_first_meetings, results: metrics.first_meetings || [] },
  secondMeetings: { total: totals.total_second_meetings, results: metrics.second_meetings || [] },
  appointedMeetings: { total: totals.total_appointed_meetings, results: metrics.appointed_meetings || [] },
  bookings: { total: totals.total_bookings, results: metrics.bookings || [] },
  deals: { total: totals.total_deals, results: metrics.deals || [] },
  qualifiedLeads: { total: totals.total_qualified_leads, results: metrics.qualified_leads || [] },
  takenLeads: { total: totals.total_taken_leads, results: metrics.taken_leads || [] },
  clientsInWork: { total: totals.clients_in_work }
};
