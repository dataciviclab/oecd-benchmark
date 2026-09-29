-- mart_benchmark.sql: Cuneo fiscale — Italia vs G7
--
-- Confronto indicatori fiscali per paese (single, no children)

SELECT
    anno,
    ref_area,
    paese,
    misura,
    misura_label,
    unita,
    valore
FROM clean_input
WHERE ref_area IN ('ITA', 'DEU', 'FRA', 'GBR', 'USA', 'JPN', 'CAN')
  AND tipo_famiglia = 'S_C0'
  AND reddito_principale = 'AW100'
ORDER BY anno, ref_area, misura
