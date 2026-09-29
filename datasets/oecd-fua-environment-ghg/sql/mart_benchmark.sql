-- mart_benchmark.sql: Confronto emissioni GHG città OCSE
--
-- Top 20 città per emissioni totali, incluse italiane

SELECT
    anno,
    fua_code,
    citta,
    pollutante,
    unita,
    valore,
    ROW_NUMBER() OVER (PARTITION BY anno ORDER BY valore DESC) as ranking
FROM clean_input
WHERE pollutante = 'GHG_TOTAL'
  AND unita = 'T_CO2E'
  AND livello = 'FUA'
ORDER BY anno, ranking
