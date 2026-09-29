-- mart_italia.sql: Spesa sanitaria Italia per funzione
--
-- Vista Italia: spesa totale per funzione

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
ORDER BY anno, function_code
