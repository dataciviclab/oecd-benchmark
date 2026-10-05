-- clean.sql: OECD Tax Revenue — Comparative
--
-- raw_input: OECD csvfilewithlabels
-- 7 dimensions: REF_AREA, MEASURE, SECTOR, STANDARD_REVENUE, CTRY_SPECIFIC_REVENUE, UNIT_MEASURE, FREQ

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS ref_area,
    normalize_string("Reference area") AS paese,
    normalize_string(MEASURE) AS misura,
    normalize_string("Measure") AS misura_label,
    normalize_string(SECTOR) AS settore,
    normalize_string("Institutional sector") AS settore_label,
    normalize_string(STANDARD_REVENUE) AS revenue_category,
    normalize_string("Revenue category") AS revenue_category_label,
    normalize_string(CTRY_SPECIFIC_REVENUE) AS revenue_specific,
    normalize_string(UNIT_MEASURE) AS unita,
    normalize_string("Unit of measure") AS unita_label,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE TIME_PERIOD IS NOT NULL
  AND OBS_VALUE IS NOT NULL
  AND OBS_VALUE != ''
  AND normalize_string(TIME_PERIOD) ~ '^\d{4}$'
ORDER BY anno, misura, settore, revenue_category
