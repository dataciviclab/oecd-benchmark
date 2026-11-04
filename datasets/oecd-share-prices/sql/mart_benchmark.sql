-- mart_benchmark.sql: Prezzi azionari — media annua per paese
--
-- Confronto Italia vs paesi benchmark (FRA, DEU, ESP, GBR, USA).

SELECT
    anno,
    ref_area,
    paese,
    ROUND(AVG(valore), 2) AS media_annua,
    COUNT(*) AS mesi_osservati
FROM clean_input
WHERE unita = 'IX'
GROUP BY anno, ref_area, paese
ORDER BY anno, ref_area
