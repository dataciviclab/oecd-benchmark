-- clean.sql: OECD ENV.EPI — Air Emissions (Italy)
--
-- raw_input schema from OECD csvfilewithlabels:
--   STRUCTURE, STRUCTURE_ID, STRUCTURE_NAME, ACTION,
--   REF_AREA, "Reference area", FREQ, "Frequency of observation",
--   POLLUTANT, "Pollutant", MEASURE, "Measure",
--   UNIT_MEASURE, "Unit of measure", TIME_PERIOD, "Time period",
--   OBS_VALUE, "Observation value", OBS_STATUS, ...

SELECT
    CAST(TIME_PERIOD AS INTEGER) AS anno,
    CAST(POLLUTANT AS VARCHAR) AS inquinante,
    CAST("Pollutant" AS VARCHAR) AS inquinante_label,
    CAST(MEASURE AS VARCHAR) AS misura,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
ORDER BY anno, inquinante
