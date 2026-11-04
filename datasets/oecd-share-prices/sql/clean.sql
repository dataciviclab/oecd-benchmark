-- clean.sql: OECD Financial Market — Share Prices
--
-- raw_input: OECD csvfilewithlabels
-- dimensioni: REF_AREA, FREQ, MEASURE, UNIT_MEASURE, ACTIVITY, ADJUSTMENT,
--             TRANSFORMATION, TIME_HORIZ, METHODOLOGY
--
-- Serie: indice dei prezzi azionari, base 2015=100, frequenza mensile.

SELECT
    cast_int(SUBSTR(normalize_string(TIME_PERIOD), 1, 4)) AS anno,
    cast_int(SUBSTR(normalize_string(TIME_PERIOD), 6, 2)) AS mese,
    normalize_string(TIME_PERIOD) AS periodo,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string("Reference area") AS paese,
    normalize_string(MEASURE) AS misura,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string(BASE_PER) AS base_periodo,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND normalize_string(TIME_PERIOD) ~ '^\d{4}-\d{2}$'
ORDER BY anno, mese, ref_area
