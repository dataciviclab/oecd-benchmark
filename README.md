# OECD Benchmark

**Come si confronta l'Italia con i principali paesi OCSE su emissioni, PIL, salute, istruzione, lavoro e fisco?**

Questi dati rispondono a domande concrete: quanto inquina Roma rispetto a Londra? Quanto spende l'Italia in sanità rispetto alla Germania? Qual è il tasso di disoccupazione italiano rispetto alla media OCSE?

## Cosa contengono

| Dataset | Righe | Periodo | Paesi | Granularità |
|---|---|---|---|---|
| Emissioni GHG | 2.800 | 1990–2024 | Globale (FUA) | Città |
| PIL FUA | 2.250 | 2000–2022 | Europa (FUA) | Città |
| Spesa Sanitaria | 6.755 | 1988–2025 | Italia | Nazionale |
| PIL Regionale | 7.575 | 2000–2024 | Globale (TL2) | Regioni |
| Istruzione | 3.186 | 2000–2025 | Globale (TL2) | Regioni |
| Disoccupazione | 233 | 2000–2025 | G7 + OCSE | Nazionale |
| Entrate Fiscali | 4.707 | 2000–2024 | Italia | Nazionale |
| Cuneo Fiscale | 3.120 | 2000–2025 | G7 | Nazionale |

**Fonte**: [OECD Data Explorer](https://data-explorer.oecd.org/) — SDMX API pubblica, nessuna chiave richiesta.

## Esempi di domande

- Quanto inquina la Lombardia rispetto alla Baviera?
- Come si confronta la spesa sanitaria italiana con quella tedesca?
- Qual è il tasso di disoccupazione giovanile italiano rispetto alla media OCSE?
- Quanto incide il cuneo fiscale sul reddito da lavoro in Italia vs Germania?
- Come è cambiata la composizione delle entrate fiscali italiane in 20 anni?

## Come accedere

### Dashboard interattiva
```bash
cd oecd-benchmark
pip install -e ".[dashboard]"
streamlit run dashboard/app.py
```

### Query SQL (DuckDB)
```python
import duckdb
duckdb.sql("SELECT * FROM read_parquet('out/data/mart/oecd_fua_ghg/2026/mart_italia.parquet')")
```

### Parquet (download diretto)
I dati processati sono in `out/data/mart/` e `out/data/clean/` — file Parquet leggibili da qualsiasi tool (DuckDB, pandas, Polars, DuckDB).

## Approfondimenti

- [Discussion](https://github.com/dataciviclab/oecd-benchmark/discussions) — domande, suggerimenti, idee
- [Analisi OECD](docs/ANALYSIS_REPORT.md) — principali findings dai dati
- [Intelligence OECD](docs/OECD_INTELLIGENCE.md) — note tecniche sull'API e strategia di selezione dataset

## Partecipa

- **Hai una domanda** su questi dati? Aprila nelle [Discussion](https://github.com/dataciviclab/oecd-benchmark/discussions)
- **Hai trovato un errore**? Apri un'issue
- **Vuoi aggiungere un dataset**? Guarda `CONTRIBUTING.md`

## Licenza

[MIT](LICENSE)

---

[DataCivicLab](https://dataciviclab.org/) · Dati aperti per il bene comune
