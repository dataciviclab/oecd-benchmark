-- mart_italia.sql: PIL regionale italiano
--
-- Vista Italia: PIL a livello TL2 (regione)

SELECT
    anno,
    ref_area,
    paese,
    livello_territoriale,
    tipo_territorio,
    misura,
    misura_label,
    attivita,
    attivita_label,
    prezzi,
    unita,
    valore
FROM clean_input
WHERE ref_area LIKE 'IT%'
  AND livello_territoriale = 'TL2'
  AND misura = 'GDP'
ORDER BY anno, ref_area
