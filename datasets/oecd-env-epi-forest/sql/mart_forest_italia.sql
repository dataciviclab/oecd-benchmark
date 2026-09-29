-- mart_forest_italia.sql: Indicatori forestali Italia per anno
--
-- La clean produce già la granularità giusta: 1 riga per (anno, indicatore, unita).

SELECT
    anno,
    indicatore,
    indicatore_label,
    unita,
    valore
FROM clean_input
ORDER BY anno, indicatore
