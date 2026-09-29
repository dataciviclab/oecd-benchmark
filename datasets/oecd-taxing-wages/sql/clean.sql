-- clean.sql: OECD Taxing Wages — Comparative indicators
--
-- raw_input: OECD csvfilewithlabels
-- 8 dimensions: REF_AREA, MEASURE, UNIT_MEASURE, HOUSEHOLD_TYPE, INCOME_PRINCIPAL, INCOME_SPOUSE, FREQ, TAX_INTERVAL

SELECT
    CAST(TIME_PERIOD AS INTEGER) AS anno,
    CAST(REF_AREA AS VARCHAR) AS ref_area,
    CAST("Reference area" AS VARCHAR) AS paese,
    CAST(MEASURE AS VARCHAR) AS misura,
    CAST("Measure" AS VARCHAR) AS misura_label,
    CAST(HOUSEHOLD_TYPE AS VARCHAR) AS tipo_famiglia,
    CAST("Household type" AS VARCHAR) AS tipo_famiglia_label,
    CAST(INCOME_PRINCIPAL AS VARCHAR) AS reddito_principale,
    CAST("Earnings of the principal" AS VARCHAR) AS reddito_principale_label,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST("Unit of measure" AS VARCHAR) AS unita_label,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND CAST(TIME_PERIOD AS VARCHAR) ~ '^\d{4}$'
ORDER BY anno, misura, tipo_famiglia
