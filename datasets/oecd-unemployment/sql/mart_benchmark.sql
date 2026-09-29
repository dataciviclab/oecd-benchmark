-- mart_benchmark.sql: Disoccupazione — Italia vs G7 vs OCSE
--
-- Confronto tasso disoccupazione totale per paese

SELECT
    anno,
    ref_area,
    paese,
    AVG(valore) AS media_annuale
FROM clean_input
WHERE ref_area IN ('ITA', 'DEU', 'FRA', 'GBR', 'USA', 'JPN', 'CAN', 'OECD')
  AND sesso = '_T'
  AND eta = 'Y_GE15'
  AND unita = 'PT_LF_SUB'
GROUP BY anno, ref_area, paese
ORDER BY anno, ref_area
