-- mart_benchmark.sql: Spesa sanitaria — Italia vs OCSE vs G7
--
-- Confronto spesa sanitaria totale per paese (funzione totale, schema totale)

SELECT
    anno,
    ref_area,
    paese,
    misura,
    misura_label,
    unita,
    valore
FROM clean_input
WHERE misura = 'EXP_HEALTH'
  AND financing_scheme = '_T'
  AND provider = '_T'
  AND function_code = '_T'
ORDER BY anno, ref_area
