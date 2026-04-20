// ============================================================================
// КОД ДЛЯ НОДЫ "ЛУЧ Aggregate"
// ============================================================================
// Скопируй весь этот код и вставь в поле "JavaScript Code" ноды "ЛУЧ Aggregate"

const queryResults = $node["ЛУЧ Query"].json;
const now = new Date();
const yesterday = new Date(now);
yesterday.setDate(now.getDate() - 1);
const yesterdayFormatted = yesterday.toLocaleDateString('ru-RU');

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
  yesterday: yesterdayFormatted,
  team_name: 'ЛУЧ',
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

// ============================================================================
// КОД ДЛЯ НОДЫ "MAXIMUM Aggregate"
// ============================================================================
// Скопируй весь этот код и вставь в поле "JavaScript Code" ноды "MAXIMUM Aggregate"

const queryResults = $node["MAXIMUM Query"].json;
const now = new Date();
const yesterday = new Date(now);
yesterday.setDate(now.getDate() - 1);
const yesterdayFormatted = yesterday.toLocaleDateString('ru-RU');

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
  yesterday: yesterdayFormatted,
  team_name: 'MAXIMUM',
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

// ============================================================================
// КОД ДЛЯ НОДЫ "MORE Aggregate"
// ============================================================================
// Скопируй весь этот код и вставь в поле "JavaScript Code" ноды "MORE Aggregate"

const queryResults = $node["MORE Query"].json;
const now = new Date();
const yesterday = new Date(now);
yesterday.setDate(now.getDate() - 1);
const yesterdayFormatted = yesterday.toLocaleDateString('ru-RU');

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
  yesterday: yesterdayFormatted,
  team_name: 'MORE',
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
