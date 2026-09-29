-- clean.sql: OECD ENV.EPI — Forest (Italy)
--
-- raw_input schema from OECD csvfilewithlabels

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(MEASURE) AS indicatore,
    normalize_string("Measure") AS indicatore_label,
    normalize_string(UNIT_MEASURE) AS unita,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
ORDER BY anno, indicatore
