// Код для обработки простого формата с реальными менеджерами
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Гарантируем массив
const resultsArray = Array.isArray(queryResults) ? queryResults : [queryResults];

// Найдем строку с totals (где section IS NULL)
const totalsRow = resultsArray.find(row => !row.section) || resultsArray[0] || {};

const totals = {
  total_first_meetings: parseInt(totalsRow.total_first_meetings) || 0,
  total_second_meetings: parseInt(totalsRow.total_second_meetings) || 0,
  total_appointed_meetings: parseInt(totalsRow.total_appointed_meetings) || 0,
  total_bookings: parseInt(totalsRow.total_bookings) || 0,
  total_deals: parseInt(totalsRow.total_deals) || 0,
  total_qualified_leads: parseInt(totalsRow.total_qualified_leads) || 0,
  total_taken_leads: parseInt(totalsRow.total_taken_leads) || 0,
  clients_in_work: parseInt(totalsRow.clients_in_work) || 0
};

// Группируем менеджеров по секциям
const metrics = {};
resultsArray.forEach((row) => {
  if (row.section) {
    const section = row.section;
    if (!metrics[section]) {
      metrics[section] = [];
    }
    metrics[section].push({
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
