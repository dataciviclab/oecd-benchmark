-- clean.sql: OECD Labour Force — Monthly Unemployment Rate
--
-- raw_input: OECD csvfilewithlabels
-- 9 dimensions: REF_AREA, MEASURE, UNIT_MEASURE, TRANSFORMATION, ADJUSTMENT, SEX, AGE, ACTIVITY, FREQ

SELECT
    CAST(SUBSTR(CAST(TIME_PERIOD AS VARCHAR), 1, 4) AS INTEGER) AS anno,
    CAST(TIME_PERIOD AS VARCHAR) AS mese_str,
    CAST(REF_AREA AS VARCHAR) AS ref_area,
    CAST("Reference area" AS VARCHAR) AS paese,
    CAST(MEASURE AS VARCHAR) AS misura,
    CAST("Measure" AS VARCHAR) AS misura_label,
    CAST(SEX AS VARCHAR) AS sesso,
    CAST("Sex" AS VARCHAR) AS sesso_label,
    CAST(AGE AS VARCHAR) AS eta,
    CAST("Age" AS VARCHAR) AS eta_label,
    CAST(ACTIVITY AS VARCHAR) AS attivita,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST("Unit of measure" AS VARCHAR) AS unita_label,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND CAST(TIME_PERIOD AS VARCHAR) ~ '^\d{4}-\d{2}$'
ORDER BY anno, ref_area, sesso, eta
