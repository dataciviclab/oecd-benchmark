-- mart_benchmark.sql: PIL sub-nazionale — regioni OCSE top 20
--
-- Confronto regioni per PIL

SELECT
    anno,
    ref_area,
    paese,
    livello_territoriale,
    tipo_territorio,
    misura,
    attivita,
    unita,
    valore,
    ROW_NUMBER() OVER (PARTITION BY anno ORDER BY valore DESC) as ranking
FROM clean_input
WHERE livello_territoriale = 'TL2'
  AND misura = 'GDP'
  AND attivita = '_T'
ORDER BY anno, ranking
