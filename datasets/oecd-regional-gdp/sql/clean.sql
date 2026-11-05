-- clean.sql: OECD Regional GDP
--
-- raw_input: OECD csvfilewithlabels
-- REF_AREA in posizione 3 (dots: ..ITA.....)

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string(REF_AREA_label) AS paese,
    normalize_string(TERRITORIAL_LEVEL) AS livello_territoriale,
    normalize_string(TERRITORIAL_TYPE) AS tipo_territorio,
    normalize_string(MEASURE) AS misura,
    normalize_string(MEASURE_label) AS misura_label,
    normalize_string(ACTIVITY) AS attivita,
    normalize_string(ACTIVITY_label) AS attivita_label,
    normalize_string(PRICES) AS prezzi,
    normalize_string(PRICES_label) AS prezzi_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string(UNIT_MEASURE_label) AS unita_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND cast_int(TIME_PERIOD) <= 2025
ORDER BY anno, ref_area, misura, attivita
