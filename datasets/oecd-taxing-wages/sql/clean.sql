-- clean.sql: OECD Taxing Wages — Comparative indicators
--
-- raw_input: OECD csvfilewithlabels
-- 8 dimensioni: REF_AREA, MEASURE, UNIT_MEASURE, HOUSEHOLD_TYPE,
-- INCOME_PRINCIPAL, INCOME_SPOUSE, CIVIL_STATUS, FREQ.
-- INCOME_SPOUSE e CIVIL_STATUS distinguono serie diverse sulla stessa chiave:
-- senza di esse il clean collassa più osservazioni per anno (es. sposa a
-- reddito 0/67/100% e stato civile).

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string(REF_AREA_label) AS paese,
    normalize_string(MEASURE) AS misura,
    normalize_string(MEASURE_label) AS misura_label,
    normalize_string(HOUSEHOLD_TYPE) AS tipo_famiglia,
    normalize_string(HOUSEHOLD_TYPE_label) AS tipo_famiglia_label,
    normalize_string(INCOME_PRINCIPAL) AS reddito_principale,
    normalize_string(INCOME_PRINCIPAL_label) AS reddito_principale_label,
    normalize_string(INCOME_SPOUSE) AS reddito_secondo,
    normalize_string(INCOME_SPOUSE_label) AS reddito_secondo_label,
    normalize_string(CIVIL_STATUS) AS stato_civile,
    normalize_string(CIVIL_STATUS_label) AS stato_civile_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string(UNIT_MEASURE_label) AS unita_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND normalize_string(TIME_PERIOD) ~ '^\d{4}$'
ORDER BY anno, misura, tipo_famiglia
