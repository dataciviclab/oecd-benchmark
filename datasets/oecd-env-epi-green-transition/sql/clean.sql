-- clean.sql: OECD ENV.EPI — Green Transition (Italy)
--
-- raw_input schema from OECD csvfilewithlabels

SELECT
    CAST(TIME_PERIOD AS INTEGER) AS anno,
    CAST(MEASURE AS VARCHAR) AS indicatore,
    CAST("Measure" AS VARCHAR) AS indicatore_label,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND CAST(TIME_PERIOD AS INTEGER) <= 2025
ORDER BY anno, indicatore
