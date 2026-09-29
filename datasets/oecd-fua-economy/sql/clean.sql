-- clean.sql: OECD FUA Economy — GDP and Productivity
--
-- raw_input: OECD csvfilewithlabels
-- REF_AREA = codice FUA (IT001F=Roma, IT002F=Milano, ...)
-- NOTA: TIME_PERIOD può contenere "Not applicable" — filtrare via

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS fua_code,
    normalize_string("Reference area") AS citta,
    normalize_string(MEASURE) AS misura,
    normalize_string("Measure") AS misura_label,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string("Unit of measure") AS unita_label,
    normalize_string(TERRITORIAL_LEVEL) AS livello,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND normalize_string(TIME_PERIOD) ~ '^\d{4}$'  -- Solo anni validi (4 cifre)
ORDER BY anno, fua_code, misura
