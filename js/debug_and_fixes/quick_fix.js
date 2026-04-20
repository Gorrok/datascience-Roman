// Быстрое решение - берем totals из объекта
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// queryResults - это объект с totals
const totals = {
  total_first_meetings: parseInt(queryResults.total_first_meetings) || 0,
  total_second_meetings: parseInt(queryResults.total_second_meetings) || 0,
  total_appointed_meetings: parseInt(queryResults.total_appointed_meetings) || 0,
  total_bookings: parseInt(queryResults.total_bookings) || 0,
  total_deals: parseInt(queryResults.total_deals) || 0,
  total_qualified_leads: parseInt(queryResults.total_qualified_leads) || 0,
  total_taken_leads: parseInt(queryResults.total_taken_leads) || 0,
  clients_in_work: parseInt(queryResults.clients_in_work) || 0
};

// Пока что results оставим пустыми - главное, что totals работают
return {
  yesterday,
  firstMeetings: { total: totals.total_first_meetings, results: [] },
  secondMeetings: { total: totals.total_second_meetings, results: [] },
  appointedMeetings: { total: totals.total_appointed_meetings, results: [] },
  bookings: { total: totals.total_bookings, results: [] },
  deals: { total: totals.total_deals, results: [] },
  qualifiedLeads: { total: totals.total_qualified_leads, results: [] },
  takenLeads: { total: totals.total_taken_leads, results: [] },
  clientsInWork: { total: totals.clients_in_work }
};
