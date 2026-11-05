-- clean.sql: OECD Health Expenditure (SHA)
--
-- raw_input: OECD csvfilewithlabels (header normalizzato dal toolkit:
-- colonne codice + colonne {DIM}_label).
-- 12 dimensioni SHA: REF_AREA, FREQ, MEASURE, UNIT_MEASURE, FINANCING_SCHEME,
-- FINANCING_SCHEME_REV, FUNCTION, MODE_PROVISION, PROVIDER, FACTOR_PROVISION,
-- ASSET_TYPE, PRICE_BASE.
-- Tutte le dimensioni non costanti sono proiettate: senza MODE_PROVISION e
-- PRICE_BASE il clean collassa serie distinte (totale vs per modo di erogazione,
-- prezzi correnti vs costanti) sulla stessa chiave.

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string(REF_AREA_label) AS paese,
    normalize_string(MEASURE) AS misura,
    normalize_string(MEASURE_label) AS misura_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string(UNIT_MEASURE_label) AS unita_label,
    normalize_string(FINANCING_SCHEME) AS financing_scheme,
    normalize_string(FINANCING_SCHEME_label) AS financing_scheme_label,
    normalize_string(FINANCING_SCHEME_REV) AS financing_scheme_rev,
    normalize_string(FINANCING_SCHEME_REV_label) AS financing_scheme_rev_label,
    normalize_string(FUNCTION) AS function_code,
    normalize_string(FUNCTION_label) AS function_label,
    normalize_string(MODE_PROVISION) AS mode_provision,
    normalize_string(MODE_PROVISION_label) AS mode_provision_label,
    normalize_string(PROVIDER) AS provider,
    normalize_string(PROVIDER_label) AS provider_label,
    normalize_string(FACTOR_PROVISION) AS factor_provision,
    normalize_string(FACTOR_PROVISION_label) AS factor_provision_label,
    normalize_string(ASSET_TYPE) AS asset_type,
    normalize_string(ASSET_TYPE_label) AS asset_type_label,
    normalize_string(PRICE_BASE) AS price_base,
    normalize_string(PRICE_BASE_label) AS price_base_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND cast_int(TIME_PERIOD) <= 2025
ORDER BY anno, misura, financing_scheme, function_code
