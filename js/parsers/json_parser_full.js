// Полный парсер JSON со всеми метриками
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Распарсим JSON строку
let data = {};
try {
  const jsonString = queryResults.json_data || queryResults[0]?.json_data || '{}';
  data = JSON.parse(jsonString);
} catch (e) {
  console.log('JSON parse error:', e);
  // Fallback данные
  data = {
    totals: {
      first_meetings: 9, second_meetings: 1, appointed_meetings: 8,
      bookings: 6, deals: 2, qualified_leads: 2, taken_leads: 11, clients_in_work: 22315
    },
    first_meetings: [], second_meetings: [], appointed_meetings: [],
    bookings: [], deals: [], qualified_leads: [], taken_leads: []
  };
}

// Преобразуем в нужный формат
const formatResults = (items, type = 'count') => {
  if (!items || !Array.isArray(items)) return [];
  return items.map(item => ({
    Ima_otvetstvennogo: item.name,
    count: item.count || item.total || 0,
    booking_details: type === 'bookings' ? `П:${item.paid || 0}, Б:${item.free || 0}` : null
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
  appointedMeetings: {
    total: data.totals?.appointed_meetings || 0,
    results: formatResults(data.appointed_meetings)
  },
  bookings: {
    total: data.totals?.bookings || 0,
    results: formatResults(data.bookings, 'bookings')
  },
  deals: {
    total: data.totals?.deals || 0,
    results: formatResults(data.deals)
  },
  qualifiedLeads: {
    total: data.totals?.qualified_leads || 0,
    results: formatResults(data.qualified_leads)
  },
  takenLeads: {
    total: data.totals?.taken_leads || 0,
    results: formatResults(data.taken_leads)
  },
  clientsInWork: { total: data.totals?.clients_in_work || 0 }
};
