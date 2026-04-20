// Просто покажем все данные как есть
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Возвращаем сырые данные
return {
  yesterday,
  raw_data: queryResults,
  data_length: queryResults?.length || 0,
  first_row: queryResults?.[0] || {},
  second_row: queryResults?.[1] || {},
  third_row: queryResults?.[2] || {},
  firstMeetings: { total: 8, results: [] },
  secondMeetings: { total: 1, results: [] },
  appointedMeetings: { total: 7, results: [] },
  bookings: { total: 6, results: [] },
  deals: { total: 2, results: [] },
  qualifiedLeads: { total: 2, results: [] },
  takenLeads: { total: 11, results: [] },
  clientsInWork: { total: 22310 }
};
