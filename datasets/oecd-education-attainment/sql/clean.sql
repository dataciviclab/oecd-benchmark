-- clean.sql: OECD Education Attainment
--
-- raw_input: OECD csvfilewithlabels
-- REF_AREA in posizione 3 (dots: ..ITA........)

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string("Reference area") AS paese,
    normalize_string(TERRITORIAL_LEVEL) AS livello_territoriale,
    normalize_string(TERRITORIAL_TYPE) AS tipo_territorio,
    normalize_string(MEASURE) AS misura,
    normalize_string("Measure") AS misura_label,
    normalize_string(AGE) AS eta,
    normalize_string("Age") AS eta_label,
    normalize_string(SEX) AS sesso,
    normalize_string("Sex") AS sesso_label,
    normalize_string(EDUCATION_LEV) AS educazione,
    normalize_string("Education level") AS educazione_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string("Unit of measure") AS unita_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND cast_int(TIME_PERIOD) <= 2025
ORDER BY anno, ref_area, misura, eta, sesso, educazione
