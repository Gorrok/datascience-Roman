-- Простой подход: вернуть JSON строку
SELECT CONCAT(
    '{"totals":{',
    '"first_meetings":', (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t), ',',
    '"second_meetings":', (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t), ',',
    '"clients_in_work":', (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND Data_peredaci_v_OP IS NOT NULL AND CLSD IS NULL AND ID_voronki = 437595 AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев') , '},',
    '"first_meetings":[', GROUP_CONCAT(CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')), '],',
    '"second_meetings":[', (SELECT GROUP_CONCAT(CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')) FROM (SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo HAVING cnt > 0) t), ']',
    '}'
) as json_data

FROM (
    SELECT Ima_otvetstvennogo, COUNT(*) as cnt
    FROM Leads
    WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
    AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
    GROUP BY Ima_otvetstvennogo
    HAVING cnt > 0
) t
