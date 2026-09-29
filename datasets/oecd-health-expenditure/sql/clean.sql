-- clean.sql: OECD Health Expenditure (SHA)
--
-- raw_input: OECD csvfilewithlabels
-- 12 dimensioni: REF_AREA, FREQ, MEASURE, UNIT_MEASURE, FINANCING_SCHEME, etc.

SELECT
    CAST(TIME_PERIOD AS INTEGER) AS anno,
    CAST(REF_AREA AS VARCHAR) AS ref_area,
    CAST("Reference area" AS VARCHAR) AS paese,
    CAST(MEASURE AS VARCHAR) AS misura,
    CAST("Measure" AS VARCHAR) AS misura_label,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST("Unit of measure" AS VARCHAR) AS unita_label,
    CAST(FINANCING_SCHEME AS VARCHAR) AS financing_scheme,
    CAST("Financing scheme" AS VARCHAR) AS financing_scheme_label,
    CAST(FUNCTION AS VARCHAR) AS function_code,
    CAST("Function" AS VARCHAR) AS function_label,
    CAST(PROVIDER AS VARCHAR) AS provider,
    CAST("Provider" AS VARCHAR) AS provider_label,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND CAST(TIME_PERIOD AS INTEGER) <= 2025
ORDER BY anno, misura, financing_scheme, function_code
