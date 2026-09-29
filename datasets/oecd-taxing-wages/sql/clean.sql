-- clean.sql: OECD Taxing Wages — Comparative indicators
--
-- raw_input: OECD csvfilewithlabels
-- 8 dimensions: REF_AREA, MEASURE, UNIT_MEASURE, HOUSEHOLD_TYPE, INCOME_PRINCIPAL, INCOME_SPOUSE, FREQ, TAX_INTERVAL

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string("Reference area") AS paese,
    normalize_string(MEASURE) AS misura,
    normalize_string("Measure") AS misura_label,
    normalize_string(HOUSEHOLD_TYPE) AS tipo_famiglia,
    normalize_string("Household type") AS tipo_famiglia_label,
    normalize_string(INCOME_PRINCIPAL) AS reddito_principale,
    normalize_string("Earnings of the principal") AS reddito_principale_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string("Unit of measure") AS unita_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND normalize_string(TIME_PERIOD) ~ '^\d{4}$'
ORDER BY anno, misura, tipo_famiglia
