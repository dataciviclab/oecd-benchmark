-- mart_italia.sql: Entrate fiscali Italia — overview
--
-- Entrate fiscali totali (valori assoluti EUR)
-- Prendiamo il massimo per anno (totale, non sotto-categorie)

SELECT
    anno,
    ref_area,
    paese,
    misura,
    misura_label,
    settore,
    unita,
    MAX(valore) AS valore
FROM clean_input
WHERE ref_area = 'ITA'
  AND settore = 'S13'
GROUP BY anno, ref_area, paese, misura, misura_label, settore, unita
ORDER BY anno
