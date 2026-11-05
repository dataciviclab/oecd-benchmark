-- mart_benchmark.sql: Spesa sanitaria — benchmark
--
-- Confronto spesa sanitaria totale per paese (funzione totale, schema totale),
-- prezzi correnti. mode_provision='_T' e price_base IN ('V','_Z') evitano le
-- righe duplicate da serie con prezzi/modi diversi sulla stessa chiave.
-- NOTA: il raw è filtrato REF_AREA=ITA, quindi oggi il "benchmark" contiene
-- solo l'Italia (follow-up: rimuovere il filtro per un confronto reale).

SELECT
    anno,
    ref_area,
    paese,
    misura,
    misura_label,
    unita,
    valore
FROM clean_input
WHERE misura = 'EXP_HEALTH'
  AND financing_scheme = '_T'
  AND provider = '_T'
  AND function_code = '_T'
  AND mode_provision = '_T'
  AND price_base IN ('V', '_Z')
ORDER BY anno, ref_area
