-- mart_benchmark.sql: Entrate fiscali — benchmark paesi OCSE
--
-- Confronto entrate fiscali totali (T_SPLIT) come % del PIL

SELECT
    anno,
    ref_area,
    paese,
    misura,
    valore
FROM clean_input
WHERE settore = 'S13'
  AND misura = 'TAX_REV'
  AND unita = 'PT_B1GQ'
  AND revenue_category = 'T_SPLIT'
ORDER BY anno, ref_area
