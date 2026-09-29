-- mart_italia.sql: Istruzione popolazione italiana
--
-- Vista Italia: livello istruzione per età e sesso

SELECT
    anno,
    ref_area,
    paese,
    livello_territoriale,
    tipo_territorio,
    misura,
    misura_label,
    eta,
    eta_label,
    sesso,
    sesso_label,
    educazione,
    educazione_label,
    unita,
    valore
FROM clean_input
WHERE ref_area LIKE 'IT%'
  AND livello_territoriale = 'TL2'
  AND educazione = 'ISCED11_5T8'
ORDER BY anno, ref_area, eta, sesso
