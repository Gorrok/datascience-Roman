// Просто выведем сырые данные без обработки
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

console.log('=== RAW DATA DEBUG ===');
console.log('Type of queryResults:', typeof queryResults);
console.log('Is Array:', Array.isArray(queryResults));
console.log('Length:', queryResults?.length);

if (queryResults && queryResults.length > 0) {
  console.log('First row keys:', Object.keys(queryResults[0]));
  console.log('First row metric_type:', queryResults[0].metric_type);
  console.log('First row Ima_otvetstvennogo:', queryResults[0].Ima_otvetstvennogo);
  console.log('First row count_value:', queryResults[0].count_value);

  // Проверим несколько строк
  for (let i = 0; i < Math.min(3, queryResults.length); i++) {
    console.log(`Row ${i}:`, {
      metric_type: queryResults[i].metric_type,
      Ima_otvetstvennogo: queryResults[i].Ima_otvetstvennogo,
      count_value: queryResults[i].count_value
    });
  }
}

// Возвращаем минимальный результат
return {
  yesterday,
  debug: 'Check console logs',
  firstMeetings: { total: 0, results: [] },
  secondMeetings: { total: 0, results: [] },
  appointedMeetings: { total: 0, results: [] },
  bookings: { total: 0, results: [] },
  deals: { total: 0, results: [] },
  qualifiedLeads: { total: 0, results: [] },
  takenLeads: { total: 0, results: [] },
  clientsInWork: { total: 0 }
};
