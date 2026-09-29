-- mart_benchmark.sql: Confronto PIL FUA — Milano vs capitali europee
--
-- Filtro sulle principali FUA per confronto

SELECT
    anno,
    fua_code,
    citta,
    misura,
    unita,
    valore,
    ROW_NUMBER() OVER (PARTITION BY anno, misura ORDER BY valore DESC) as ranking
FROM clean_input
WHERE misura = 'GDP'
  AND livello = 'FUA'
  AND fua_code IN (
    'IT002F',  -- Milano
    'UK001F',  -- London
    'FR001F',  -- Paris
    'ES001F',  -- Madrid
    'ES002F',  -- Barcelona
    'DE002F',  -- Munich
    'NL001F',  -- Amsterdam
    'BE001F',  -- Brussels
    'SE001F',  -- Stockholm
    'IT001F'   -- Roma
  )
ORDER BY anno, misura, ranking
