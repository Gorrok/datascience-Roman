// Отладка финального кода
const queryResults = $node["Unified Report Query"].json;
const yesterday = $node["Date Logic"].json.yesterday;

// Гарантируем массив
const resultsArray = Array.isArray(queryResults) ? queryResults : [queryResults];

console.log('=== DEBUG AGGREGATE ===');
console.log('Total rows in resultsArray:', resultsArray.length);
console.log('First row section:', resultsArray[0]?.section);
console.log('First row Ima_otvetstvennogo:', resultsArray[0]?.Ima_otvetstvennogo);

// Берем totals из ПЕРВОЙ строки (они одинаковые во всех)
const totalsRow = resultsArray[0];
const totals = {
  total_first_meetings: parseInt(totalsRow.total_first_meetings) || 0,
  total_second_meetings: parseInt(totalsRow.total_second_meetings) || 0,
  total_appointed_meetings: parseInt(totalsRow.total_appointed_meetings) || 0,
  total_bookings: parseInt(totalsRow.total_bookings) || 0,
  total_deals: parseInt(totalsRow.total_deals) || 0,
  total_qualified_leads: parseInt(totalsRow.total_qualified_leads) || 0,
  total_taken_leads: parseInt(totalsRow.total_taken_leads) || 0,
  clients_in_work: parseInt(totalsRow.clients_in_work) || 0
};

console.log('Totals extracted:', totals);

// Группируем ВСЕ строки по section
const metrics = {};
let processedRows = 0;
resultsArray.forEach((row, index) => {
  console.log(`Row ${index}: section="${row.section}", Ima="${row.Ima_otvetstvennogo}", count=${row.count_value}`);

  if (row.section) {
    processedRows++;
    const section = row.section;
    if (!metrics[section]) {
      metrics[section] = [];
    }
    metrics[section].push({
      Ima_otvetstvennogo: row.Ima_otvetstvennogo,
      count: parseInt(row.count_value) || 0,
      booking_details: row.booking_details
    });
    console.log(`Added to ${section}: ${row.Ima_otvetstvennogo}`);
  }
});

console.log('Processed rows with section:', processedRows);
console.log('Final metrics keys:', Object.keys(metrics));
console.log('First meetings count:', metrics.first_meetings?.length || 0);
console.log('Second meetings count:', metrics.second_meetings?.length || 0);

return {
  yesterday,
  firstMeetings: { total: totals.total_first_meetings, results: metrics.first_meetings || [] },
  secondMeetings: { total: totals.total_second_meetings, results: metrics.second_meetings || [] },
  appointedMeetings: { total: totals.total_appointed_meetings, results: metrics.appointed_meetings || [] },
  bookings: { total: totals.total_bookings, results: metrics.bookings || [] },
  deals: { total: totals.total_deals, results: metrics.deals || [] },
  qualifiedLeads: { total: totals.total_qualified_leads, results: metrics.qualified_leads || [] },
  takenLeads: { total: totals.total_taken_leads, results: metrics.taken_leads || [] },
  clientsInWork: { total: totals.clients_in_work }
};
