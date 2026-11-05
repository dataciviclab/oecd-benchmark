-- mart_italia.sql: Spesa sanitaria Italia per funzione
--
-- Vista Italia: spesa totale per funzione, prezzi correnti.
-- mode_provision='_T' = totale per modo di erogazione; price_base IN ('V','_Z')
-- = prezzi correnti per le unità monetarie e ratio (%PIL, %spesa) per le altre.
-- Senza questi filtri il clean proietta più serie per la stessa chiave
-- (prezzi correnti vs costanti, totale vs per modo) → righe duplicate.

SELECT
    anno,
    ref_area,
    paese,
    misura,
    misura_label,
    unita,
    financing_scheme,
    financing_scheme_label,
    function_code,
    function_label,
    provider,
    valore
FROM clean_input
WHERE ref_area = 'ITA'
  AND financing_scheme = '_T'
  AND provider = '_T'
  AND mode_provision = '_T'
  AND price_base IN ('V', '_Z')
ORDER BY anno, function_code
