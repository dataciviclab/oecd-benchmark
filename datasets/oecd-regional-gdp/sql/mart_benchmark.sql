-- mart_benchmark.sql: PIL sub-nazionale — regioni OCSE
--
-- Confronto regioni per PIL. prezzi e unita sono colonne di output: senza di
-- esse la stessa regione/anno collassa su più serie (prezzi correnti vs
-- costanti, valute diverse) → righe duplicate. Il ranking è per
-- (anno, unita, prezzi).

SELECT
    anno,
    ref_area,
    paese,
    livello_territoriale,
    tipo_territorio,
    misura,
    attivita,
    prezzi,
    unita,
    valore,
    ROW_NUMBER() OVER (PARTITION BY anno, unita, prezzi ORDER BY valore DESC) as ranking
FROM clean_input
WHERE livello_territoriale = 'TL2'
  AND misura = 'GDP'
  AND attivita = '_T'
ORDER BY anno, unita, prezzi, ranking
