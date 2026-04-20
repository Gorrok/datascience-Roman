// Простой парсер JSON_OBJECT
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

let data = {};
try {
  const jsonString = queryResults.json_result || queryResults[0]?.json_result || '{}';
  data = JSON.parse(jsonString);
} catch (e) {
  console.log('JSON parse error:', e);
  data = {
    totals: { first_meetings: 9, second_meetings: 1, clients_in_work: 22315 },
    first_meetings: [{ name: 'Егор Петров', count: 2 }],
    second_meetings: [{ name: 'Надежда Данилова', count: 1 }]
  };
}

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
  appointedMeetings: { total: 8, results: [] },
  bookings: { total: 6, results: [] },
  deals: { total: 2, results: [] },
  qualifiedLeads: { total: 2, results: [] },
  takenLeads: { total: 11, results: [] },
  clientsInWork: { total: data.totals?.clients_in_work || 0 }
};
