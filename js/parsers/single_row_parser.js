// Парсер для одной строки со всеми данными
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
    results: [] // Пока пустые, можно добавить аналогично
  },
  bookings: {
    total: parseInt(row.total_bookings) || 0,
    results: []
  },
  deals: {
    total: parseInt(row.total_deals) || 0,
    results: []
  },
  qualifiedLeads: {
    total: parseInt(row.total_qualified_leads) || 0,
    results: []
  },
  takenLeads: {
    total: parseInt(row.total_taken_leads) || 0,
    results: []
  },
  clientsInWork: {
    total: parseInt(row.clients_in_work) || 0
  }
};
