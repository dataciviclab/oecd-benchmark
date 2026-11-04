-- mart_italia.sql: Prezzi azionari Italia — serie mensile
--
-- Indice base 2015=100 + variazione tendenziale (YoY).
-- Il confronto è un self-join sullo stesso mese dell'anno prima: se quel mese
-- manca, la variazione è NULL invece di essere calcolata su 12 righe qualsiasi
-- (LAG(12) darebbe un valore sbagliato in presenza di buchi nella serie).

WITH ita AS (
    SELECT
        anno,
        mese,
        periodo,
        valore
    FROM clean_input
    WHERE ref_area = 'ITA'
      AND unita = 'IX'
)
SELECT
    i.anno,
    i.mese,
    i.periodo,
    i.valore,
    ROUND((i.valore / p.valore - 1) * 100, 2) AS variazione_annua_pct
FROM ita i
LEFT JOIN ita p
  ON p.anno = i.anno - 1
 AND p.mese = i.mese
ORDER BY i.anno, i.mese
