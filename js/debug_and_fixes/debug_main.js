// Отладочный код для финальной диагностики
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Логируем входные данные
console.log('Input data length:', queryResults.length);
console.log('First row sample:', {
  metric_type: queryResults[0]?.metric_type,
  Ima_otvetstvennogo: queryResults[0]?.Ima_otvetstvennogo,
  count_value: queryResults[0]?.count_value
});

// Гарантируем, что queryResults является массивом
const resultsArray = Array.isArray(queryResults) ? queryResults : [queryResults];

// Берем totals из первой строки
const totals = {
  total_first_meetings: parseInt(resultsArray[0].total_first_meetings) || 0,
  total_second_meetings: parseInt(resultsArray[0].total_second_meetings) || 0,
  total_appointed_meetings: parseInt(resultsArray[0].total_appointed_meetings) || 0,
  total_bookings: parseInt(resultsArray[0].total_bookings) || 0,
  total_deals: parseInt(resultsArray[0].total_deals) || 0,
  total_qualified_leads: parseInt(resultsArray[0].total_qualified_leads) || 0,
  total_taken_leads: parseInt(resultsArray[0].total_taken_leads) || 0,
  clients_in_work: parseInt(resultsArray[0].clients_in_work) || 0
};

console.log('Extracted totals:', totals);

// Группируем ВСЕ строки по metric_type
const metrics = {};
resultsArray.forEach((row, index) => {
  console.log(`Row ${index}: metric_type = "${row.metric_type}", has value:`, !!row.metric_type);

  if (row.metric_type) {
    const metricType = row.metric_type;
    console.log(`Processing metric: ${metricType}`);

    if (!metrics[metricType]) {
      metrics[metricType] = [];
    }
    metrics[metricType].push({
      Ima_otvetstvennogo: row.Ima_otvetstvennogo,
      count: parseInt(row.count_value) || 0,
      booking_details: row.booking_details
    });
    console.log(`Added to ${metricType}:`, row.Ima_otvetstvennogo);
  }
});

console.log('Final metrics object:', metrics);

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
