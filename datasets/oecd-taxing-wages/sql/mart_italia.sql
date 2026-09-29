-- mart_italia.sql: Cuneo fiscale Italia — overview
--
-- Indicatori principali per confronto internazionale (single, no children)

SELECT
    anno,
    ref_area,
    paese,
    misura,
    misura_label,
    tipo_famiglia,
    unita,
    valore
FROM clean_input
WHERE ref_area = 'ITA'
  AND tipo_famiglia = 'S_C0'
  AND reddito_principale = 'AW100'
ORDER BY anno, misura
