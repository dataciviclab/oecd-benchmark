-- mart_emissioni_italia.sql: Emissioni Italia per inquinante e anno
--
-- La clean produce già la granularità giusta: 1 riga per (anno, inquinante, misura, unita).

SELECT
    anno,
    inquinante,
    inquinante_label,
    misura,
    unita,
    valore
FROM clean_input
WHERE misura = 'T_EM_MM'  -- Total emissions, mass balance
  AND unita = 'KG_PS'     -- Kg per unit GDP (PPP)
ORDER BY anno, inquinante
