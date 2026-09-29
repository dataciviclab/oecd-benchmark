-- clean.sql: OECD Labour Force — Monthly Unemployment Rate
--
-- raw_input: OECD csvfilewithlabels
-- 9 dimensions: REF_AREA, MEASURE, UNIT_MEASURE, TRANSFORMATION, ADJUSTMENT, SEX, AGE, ACTIVITY, FREQ

SELECT
    cast_int(SUBSTR(normalize_string(TIME_PERIOD), 1, 4)) AS anno,
    normalize_string(TIME_PERIOD) AS mese_str,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string("Reference area") AS paese,
    normalize_string(MEASURE) AS misura,
    normalize_string("Measure") AS misura_label,
    normalize_string(SEX) AS sesso,
    normalize_string("Sex") AS sesso_label,
    normalize_string(AGE) AS eta,
    normalize_string("Age") AS eta_label,
    normalize_string(ACTIVITY) AS attivita,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string("Unit of measure") AS unita_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND normalize_string(TIME_PERIOD) ~ '^\d{4}-\d{2}$'
ORDER BY anno, ref_area, sesso, eta
