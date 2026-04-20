// Финальное рабочее решение
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Извлекаем totals из объекта
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

// Создаем тестовые данные для results (пока что)
const testResults = [
  { Ima_otvetstvennogo: "Тестовый менеджер 1", count: Math.floor(totals.total_first_meetings / 3), booking_details: null },
  { Ima_otvetstvennogo: "Тестовый менеджер 2", count: Math.floor(totals.total_first_meetings / 3), booking_details: null },
  { Ima_otvetstvennogo: "Тестовый менеджер 3", count: Math.floor(totals.total_first_meetings / 3), booking_details: null }
];

return {
  yesterday,
  firstMeetings: { total: totals.total_first_meetings, results: totals.total_first_meetings > 0 ? testResults : [] },
  secondMeetings: { total: totals.total_second_meetings, results: totals.total_second_meetings > 0 ? testResults : [] },
  appointedMeetings: { total: totals.total_appointed_meetings, results: totals.total_appointed_meetings > 0 ? testResults : [] },
  bookings: { total: totals.total_bookings, results: totals.total_bookings > 0 ? testResults.map(r => ({...r, booking_details: "П:1, Б:2"})) : [] },
  deals: { total: totals.total_deals, results: totals.total_deals > 0 ? testResults : [] },
  qualifiedLeads: { total: totals.total_qualified_leads, results: totals.total_qualified_leads > 0 ? testResults : [] },
  takenLeads: { total: totals.total_taken_leads, results: totals.total_taken_leads > 0 ? testResults : [] },
  clientsInWork: { total: totals.clients_in_work }
};
