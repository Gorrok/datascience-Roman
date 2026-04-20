// Финальный парсер для JSON строк из SQL
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Получаем данные из единственной строки
const row = Array.isArray(queryResults) ? queryResults[0] : queryResults;

const parseJsonArray = (jsonString) => {
  try {
    return jsonString ? JSON.parse(jsonString) : [];
  } catch (e) {
    console.log('JSON parse error:', e);
    return [];
  }
};

return {
  yesterday,
  firstMeetings: {
    total: parseInt(row.total_first_meetings) || 0,
    results: parseJsonArray(row.first_meetings_json)
  },
  secondMeetings: {
    total: parseInt(row.total_second_meetings) || 0,
    results: parseJsonArray(row.second_meetings_json)
  },
  appointedMeetings: {
    total: parseInt(row.total_appointed_meetings) || 0,
    results: parseJsonArray(row.appointed_meetings_json)
  },
  bookings: {
    total: parseInt(row.total_bookings) || 0,
    results: parseJsonArray(row.bookings_json)
  },
  deals: {
    total: parseInt(row.total_deals) || 0,
    results: parseJsonArray(row.deals_json)
  },
  qualifiedLeads: {
    total: parseInt(row.total_qualified_leads) || 0,
    results: parseJsonArray(row.qualified_leads_json)
  },
  takenLeads: {
    total: parseInt(row.total_taken_leads) || 0,
    results: parseJsonArray(row.taken_leads_json)
  },
  clientsInWork: {
    total: parseInt(row.clients_in_work) || 0
  }
};
