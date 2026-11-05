-- clean.sql: OECD Education Attainment
--
-- raw_input: OECD csvfilewithlabels
-- REF_AREA in posizione 3 (dots: ..ITA........)
-- STATISTICAL_OPERATION distingue MEAN (media) da SE (standard error): senza
-- questa dimensione il clean collassa media ed errore standard sulla stessa chiave.

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string(REF_AREA_label) AS paese,
    normalize_string(TERRITORIAL_LEVEL) AS livello_territoriale,
    normalize_string(TERRITORIAL_TYPE) AS tipo_territorio,
    normalize_string(MEASURE) AS misura,
    normalize_string(MEASURE_label) AS misura_label,
    normalize_string(AGE) AS eta,
    normalize_string(AGE_label) AS eta_label,
    normalize_string(SEX) AS sesso,
    normalize_string(SEX_label) AS sesso_label,
    normalize_string(EDUCATION_LEV) AS educazione,
    normalize_string(EDUCATION_LEV_label) AS educazione_label,
    normalize_string(STATISTICAL_OPERATION) AS operazione_statistica,
    normalize_string(STATISTICAL_OPERATION_label) AS operazione_statistica_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string(UNIT_MEASURE_label) AS unita_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND cast_int(TIME_PERIOD) <= 2025
ORDER BY anno, ref_area, misura, eta, sesso, educazione
