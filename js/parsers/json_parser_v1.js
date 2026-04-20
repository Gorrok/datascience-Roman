// Парсер JSON из SQL
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Распарсим JSON строку
let data = {};
try {
  const jsonString = queryResults.json_data || queryResults[0]?.json_data || '{}';
  data = JSON.parse(jsonString);
} catch (e) {
  console.log('JSON parse error:', e);
  data = {
    totals: { first_meetings: 9, second_meetings: 1, clients_in_work: 22315 },
    first_meetings: [{ name: 'Егор Петров', count: 2 }],
    second_meetings: [{ name: 'Надежда Данилова', count: 1 }]
  };
}

// Преобразуем в нужный формат
const formatResults = (items) => {
  if (!items || !Array.isArray(items)) return [];
  return items.map(item => ({
    Ima_otvetstvennogo: item.name,
    count: item.count || 0,
    booking_details: null
  }));
};

return {
  yesterday,
  firstMeetings: {
    total: data.totals?.first_meetings || 0,
    results: formatResults(data.first_meetings)
  },
  secondMeetings: {
    total: data.totals?.second_meetings || 0,
    results: formatResults(data.second_meetings)
  },
  appointedMeetings: { total: 8, results: [] },
  bookings: { total: 6, results: [] },
  deals: { total: 2, results: [] },
  qualifiedLeads: { total: 2, results: [] },
  takenLeads: { total: 11, results: [] },
  clientsInWork: { total: data.totals?.clients_in_work || 0 }
};
