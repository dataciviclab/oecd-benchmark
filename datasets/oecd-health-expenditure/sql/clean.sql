-- clean.sql: OECD Health Expenditure (SHA)
--
-- raw_input: OECD csvfilewithlabels
-- 12 dimensioni: REF_AREA, FREQ, MEASURE, UNIT_MEASURE, FINANCING_SCHEME, etc.

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string("Reference area") AS paese,
    normalize_string(MEASURE) AS misura,
    normalize_string("Measure") AS misura_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string("Unit of measure") AS unita_label,
    normalize_string(FINANCING_SCHEME) AS financing_scheme,
    normalize_string("Financing scheme") AS financing_scheme_label,
    normalize_string(FUNCTION) AS function_code,
    normalize_string("Function") AS function_label,
    normalize_string(PROVIDER) AS provider,
    normalize_string("Provider") AS provider_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND cast_int(TIME_PERIOD) <= 2025
ORDER BY anno, misura, financing_scheme, function_code
