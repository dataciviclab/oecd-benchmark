-- mart_benchmark.sql: Entrate fiscali — Italia vs G7
--
-- Confronto entrate totali per paese

SELECT
    anno,
    ref_area,
    paese,
    misura,
    valore
FROM clean_input
WHERE ref_area IN ('ITA', 'DEU', 'FRA', 'GBR', 'USA', 'JPN', 'CAN')
  AND settore = 'S13'
  AND unita = 'EUR'
ORDER BY anno, ref_area
