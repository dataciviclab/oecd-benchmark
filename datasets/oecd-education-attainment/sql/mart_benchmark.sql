-- mart_benchmark.sql: Istruzione — Italia vs OCSE vs G7
--
-- Confronto percentuale popolazione con istruzione terziaria

SELECT
    anno,
    ref_area,
    paese,
    livello_territoriale,
    misura,
    eta,
    sesso,
    educazione,
    unita,
    valore
FROM clean_input
WHERE livello_territoriale = 'TL2'
  AND educazione = 'ISCED11_5T8'
  AND eta = 'Y25T64'
  AND sesso = '_T'
ORDER BY anno, ref_area
