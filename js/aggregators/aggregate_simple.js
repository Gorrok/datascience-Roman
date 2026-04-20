const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Простой подход: найдем строку с totals и строки с метриками
let totals = {};
const metrics = {};

// Перебираем все строки
queryResults.forEach((row, index) => {
  // Если это строка с totals (metric_type = null)
  if (!row.metric_type || row.metric_type === null || row.metric_type === 'null') {
    totals = {
      total_first_meetings: parseInt(row.total_first_meetings) || 0,
      total_second_meetings: parseInt(row.total_second_meetings) || 0,
      total_appointed_meetings: parseInt(row.total_appointed_meetings) || 0,
      total_bookings: parseInt(row.total_bookings) || 0,
      total_deals: parseInt(row.total_deals) || 0,
      total_qualified_leads: parseInt(row.total_qualified_leads) || 0,
      total_taken_leads: parseInt(row.total_taken_leads) || 0,
      clients_in_work: parseInt(row.clients_in_work) || 0
    };
  } else {
    // Это строка с метрикой
    const metricType = row.metric_type;
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
