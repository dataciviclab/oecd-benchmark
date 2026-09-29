-- mart_green_transition_italia.sql: Indicatori transizione verde Italia per anno
--
-- La clean produce già la granularità giusta: 1 riga per (anno, indicatore, unita).

SELECT
    anno,
    indicatore,
    indicatore_label,
    unita,
    valore
FROM clean_input
WHERE unita = 'IX'  -- Indici (share, brevetti, etc.)
ORDER BY anno, indicatore
