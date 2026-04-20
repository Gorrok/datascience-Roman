const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Убеждаемся, что queryResults является массивом
const resultsArray = Array.isArray(queryResults) ? queryResults : [queryResults];

// Извлекаем итоговые данные (первая строка)
const totals = resultsArray[0] || {};

// Группируем данные по метрикам (начиная со второй строки)
const groupedData = {};
for (let i = 1; i < resultsArray.length; i++) {
  const row = resultsArray[i];
  if (row.metric_type) {
    if (!groupedData[row.metric_type]) {
      groupedData[row.metric_type] = [];
    }
    groupedData[row.metric_type].push({
      Ima_otvetstvennogo: row.Ima_otvetstvennogo,
      count: row.count_value,
      booking_details: row.booking_details
    });
  }
}

return {
  yesterday,
  firstMeetings: { total: parseInt(totals.total_first_meetings) || 0, results: groupedData.first_meetings || [] },
  secondMeetings: { total: parseInt(totals.total_second_meetings) || 0, results: groupedData.second_meetings || [] },
  appointedMeetings: { total: parseInt(totals.total_appointed_meetings) || 0, results: groupedData.appointed_meetings || [] },
  bookings: { total: parseInt(totals.total_bookings) || 0, results: groupedData.bookings || [] },
  deals: { total: parseInt(totals.total_deals) || 0, results: groupedData.deals || [] },
  qualifiedLeads: { total: parseInt(totals.total_qualified_leads) || 0, results: groupedData.qualified_leads || [] },
  takenLeads: { total: parseInt(totals.total_taken_leads) || 0, results: groupedData.taken_leads || [] },
  clientsInWork: { total: parseInt(totals.clients_in_work) || 0 }
};
