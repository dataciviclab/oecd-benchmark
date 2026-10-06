-- mart_italia.sql: Entrate fiscali Italia — overview
--
-- Entrate fiscali totali (T_SPLIT) come % del PIL

SELECT
    anno,
    ref_area,
    paese,
    misura,
    misura_label,
    settore,
    unita,
    valore
FROM clean_input
WHERE ref_area = 'ITA'
  AND settore = 'S13'
  AND misura = 'TAX_REV'
  AND unita = 'PT_B1GQ'
  AND revenue_category = 'T_SPLIT'
ORDER BY anno
