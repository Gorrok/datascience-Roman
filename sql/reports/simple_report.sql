-- Простой SQL без UNION - только totals
SELECT
    (SELECT SUM(first_meetings_count) FROM (
        SELECT COUNT(CASE WHEN DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as first_meetings_count
        FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t) as total_first_meetings,

    (SELECT SUM(second_meetings_count) FROM (
        SELECT COUNT(CASE WHEN DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as second_meetings_count
        FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t) as total_second_meetings,

    (SELECT COUNT(*) FROM Leads
     WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
     AND Data_peredaci_v_OP IS NOT NULL
     AND CLSD IS NULL
     AND ID_voronki = 437595
     AND Ima_otvetstvennogo IS NOT NULL
     AND Ima_otvetstvennogo != ''
     AND Ima_otvetstvennogo != 'Никита Пестерев') as clients_in_work,

    'first_meetings' as metric_type,
    'Test Manager' as Ima_otvetstvennogo,
    5 as count_value,
    null as booking_details
