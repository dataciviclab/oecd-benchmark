-- mart_italia.sql: Disoccupazione Italia — overview
--
-- Tasso di disoccupazione totale per anno (15+)

SELECT
    anno,
    ref_area,
    paese,
    sesso,
    eta,
    unita,
    AVG(valore) AS media_annuale
FROM clean_input
WHERE ref_area = 'ITA'
  AND sesso = '_T'
  AND eta = 'Y_GE15'
  AND unita = 'PT_LF_SUB'
GROUP BY anno, ref_area, paese, sesso, eta, unita
ORDER BY anno
