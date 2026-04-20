const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Гарантируем массив
const resultsArray = Array.isArray(queryResults) ? queryResults : [queryResults];

// Берем totals из первой строки
const totals = {
  total_first_meetings: parseInt(resultsArray[0]?.total_first_meetings) || 0,
  total_second_meetings: parseInt(resultsArray[0]?.total_second_meetings) || 0,
  total_appointed_meetings: parseInt(resultsArray[0]?.total_appointed_meetings) || 0,
  total_bookings: parseInt(resultsArray[0]?.total_bookings) || 0,
  total_deals: parseInt(resultsArray[0]?.total_deals) || 0,
  total_qualified_leads: parseInt(resultsArray[0]?.total_qualified_leads) || 0,
  total_taken_leads: parseInt(resultsArray[0]?.total_taken_leads) || 0,
  clients_in_work: parseInt(resultsArray[0]?.clients_in_work) || 0
};

// Группируем БЕЗ проверок - просто все строки
const metrics = {};
resultsArray.forEach((row) => {
  // Пробуем все возможные варианты metric_type
  let metricType = row.metric_type;

  // Если metric_type - строка, используем ее
  if (typeof metricType === 'string' && metricType.trim()) {
    metricType = metricType.trim();
  }

  // Группируем по любому непустому metric_type
  if (metricType && metricType !== 'null' && metricType !== null && metricType !== undefined) {
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

// Выводим для отладки
console.log('Metrics keys found:', Object.keys(metrics));
console.log('Total metrics groups:', Object.keys(metrics).length);

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
