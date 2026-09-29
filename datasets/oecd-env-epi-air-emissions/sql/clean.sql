-- clean.sql: OECD ENV.EPI — Air Emissions (Italy)
--
-- raw_input schema from OECD csvfilewithlabels:
--   STRUCTURE, STRUCTURE_ID, STRUCTURE_NAME, ACTION,
--   REF_AREA, "Reference area", FREQ, "Frequency of observation",
--   POLLUTANT, "Pollutant", MEASURE, "Measure",
--   UNIT_MEASURE, "Unit of measure", TIME_PERIOD, "Time period",
--   OBS_VALUE, "Observation value", OBS_STATUS, ...

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(POLLUTANT) AS inquinante,
    normalize_string("Pollutant") AS inquinante_label,
    normalize_string(MEASURE) AS misura,
    normalize_string(UNIT_MEASURE) AS unita,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
ORDER BY anno, inquinante
