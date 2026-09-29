-- clean.sql: OECD Education Attainment
--
-- raw_input: OECD csvfilewithlabels
-- REF_AREA in posizione 3 (dots: ..ITA........)

SELECT
    CAST(TIME_PERIOD AS INTEGER) AS anno,
    CAST(REF_AREA AS VARCHAR) AS ref_area,
    CAST("Reference area" AS VARCHAR) AS paese,
    CAST(TERRITORIAL_LEVEL AS VARCHAR) AS livello_territoriale,
    CAST(TERRITORIAL_TYPE AS VARCHAR) AS tipo_territorio,
    CAST(MEASURE AS VARCHAR) AS misura,
    CAST("Measure" AS VARCHAR) AS misura_label,
    CAST(AGE AS VARCHAR) AS eta,
    CAST("Age" AS VARCHAR) AS eta_label,
    CAST(SEX AS VARCHAR) AS sesso,
    CAST("Sex" AS VARCHAR) AS sesso_label,
    CAST(EDUCATION_LEV AS VARCHAR) AS educazione,
    CAST("Education level" AS VARCHAR) AS educazione_label,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST("Unit of measure" AS VARCHAR) AS unita_label,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND CAST(TIME_PERIOD AS INTEGER) <= 2025
ORDER BY anno, ref_area, misura, eta, sesso, educazione
