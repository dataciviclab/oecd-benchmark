-- mart_italia.sql: PIL e produttività per FUA italiana
--
-- Filtro diretto su codici FUA italiani

SELECT
    anno,
    fua_code,
    citta,
    misura,
    misura_label,
    unita,
    valore
FROM clean_input
WHERE fua_code LIKE 'IT%'
  AND misura IN ('GDP', 'LAB_PROD')
ORDER BY anno, citta
