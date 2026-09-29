-- clean.sql: OECD FUA Economy — GDP and Productivity
--
-- raw_input: OECD csvfilewithlabels
-- REF_AREA = codice FUA (IT001F=Roma, IT002F=Milano, ...)
-- NOTA: TIME_PERIOD può contenere "Not applicable" — filtrare via

SELECT
    CAST(TIME_PERIOD AS INTEGER) AS anno,
    CAST(REF_AREA AS VARCHAR) AS fua_code,
    CAST("Reference area" AS VARCHAR) AS citta,
    CAST(MEASURE AS VARCHAR) AS misura,
    CAST("Measure" AS VARCHAR) AS misura_label,
    CAST(UNIT_MEASURE AS VARCHAR) AS unita,
    CAST("Unit of measure" AS VARCHAR) AS unita_label,
    CAST(TERRITORIAL_LEVEL AS VARCHAR) AS livello,
    CAST(OBS_VALUE AS DOUBLE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND CAST(TIME_PERIOD AS VARCHAR) ~ '^\d{4}$'  -- Solo anni validi (4 cifre)
ORDER BY anno, fua_code, misura
