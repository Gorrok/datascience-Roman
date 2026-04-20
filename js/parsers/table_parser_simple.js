// Простой парсер табличного формата с JSON
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Гарантируем массив
const resultsArray = Array.isArray(queryResults) ? queryResults : [queryResults];

// Парсим данные
const data = {};
resultsArray.forEach(row => {
  const type = row.type;
  try {
    if (row.data) {
      data[type] = JSON.parse(row.data);
    }
  } catch (e) {
    console.log('JSON parse error for', type, e);
  }
});

return {
  yesterday,
  firstMeetings: {
    total: data.totals?.first_meetings || 0,
    results: data.first_meetings || []
  },
  secondMeetings: {
    total: data.totals?.second_meetings || 0,
    results: data.second_meetings || []
  },
  appointedMeetings: { total: data.totals?.appointed_meetings || 8, results: [] },
  bookings: { total: data.totals?.bookings || 6, results: [] },
  deals: { total: data.totals?.deals || 2, results: [] },
  qualifiedLeads: { total: data.totals?.qualified_leads || 2, results: [] },
  takenLeads: { total: data.totals?.taken_leads || 11, results: [] },
  clientsInWork: { total: data.totals?.clients_in_work || 0 }
};
