-- clean.sql: OECD ENV.EPI — Green Transition (Italy)
--
-- raw_input schema from OECD csvfilewithlabels
-- Esclude i placeholder temporali 1900/1901: la fonte li usa per indicatori
-- non-serie (unità "Y"/per-mille, valore puntuale). Non sono osservazioni
-- annuali e inquinano la serie storica 1990-2024.

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(MEASURE) AS indicatore,
    normalize_string(MEASURE_label) AS indicatore_label,
    normalize_string(UNIT_MEASURE) AS unita,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND cast_int(TIME_PERIOD) BETWEEN 1990 AND 2025
ORDER BY anno, indicatore
