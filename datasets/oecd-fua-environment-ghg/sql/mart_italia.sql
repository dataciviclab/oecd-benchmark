-- mart_italia.sql: Emissioni GHG totali per città italiane
--
-- Filtro diretto su codici FUA italiani (solo livello FUA, non City)

SELECT
    anno,
    fua_code,
    citta,
    pollutante,
    pollutante_label,
    unita,
    valore
FROM clean_input
WHERE fua_code LIKE 'IT%F'
  AND pollutante = 'GHG_TOTAL'
  AND unita = 'T_CO2E'
ORDER BY anno, citta
