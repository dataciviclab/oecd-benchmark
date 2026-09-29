-- clean.sql: OECD Tax Revenue — Italy
--
-- raw_input: OECD csvfilewithlabels
-- 7 dimensions: REF_AREA, MEASURE, SECTOR, STANDARD_REVENUE, CTRY_SPECIFIC_REVENUE, UNIT_MEASURE, FREQ

SELECT
    CAST(TIME_PERIOD AS INTEGER) AS anno,
    CAST(REF_AREA AS VARCHAR) AS ref_area,
    CAST("Reference area" AS VARCHAR) AS paese,
    CAST(MEASURE AS VARCHAR) AS misura,
    CAST("Measure" AS VARCHAR) AS misura_label,
    CAST(SECTOR AS VARCHAR) AS settore,
    CAST("Institutional sector" AS VARCHAR) AS settore_label,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST("Unit of measure" AS VARCHAR) AS unita_label,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND CAST(TIME_PERIOD AS VARCHAR) ~ '^\d{4}$'
ORDER BY anno, misura, settore
