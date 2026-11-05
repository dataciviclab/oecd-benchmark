# OECD Benchmark

**Come si confronta l'Italia con i principali paesi OCSE su emissioni, PIL, salute, istruzione, lavoro e fisco?**

Questi dati rispondono a domande concrete: quanto inquina Roma rispetto a Londra? Quanto spende l'Italia in sanità rispetto alla Germania? Qual è il tasso di disoccupazione italiano rispetto alla media OCSE?

## Cosa contengono

| Dataset | Righe (clean) | Periodo | Copertura | Unità | Granularità |
|---|---|---|---|---|---|
| Emissioni GHG (FUA) | 1.586.970 | 1990–2024 | Globale (FUA) | t CO₂ eq | Città |
| Emissioni inquinanti (EPI) | 3.920 | 1990–2024 | Italia | t, indici | Nazionale |
| Foreste | 49 | 1950–2015 | Italia | m³, % | Nazionale |
| Transizione verde | 1.150 | 1990–2024 | Italia | mista | Nazionale |
| PIL FUA | 57.331 | 2000–2023 | Europa (FUA) | USD PPP | Città |
| PIL Regionale | 966.046 | 1980–2025 | Globale (TL2) | USD PPP | Regioni |
| Spesa Sanitaria | 71.240 | 1970–2025 | Italia | % PIL, USD PPP | Nazionale |
| Istruzione | 328.485 | 2000–2025 | Globale (TL2) | % | Regioni |
| Disoccupazione | 323.577 | 1953–2026 | G7 + OCSE | % | Nazionale |
| Entrate Fiscali | 1.496.211 | 1965–2022 | 20 OCSE | % PIL | Nazionale |
| Cuneo Fiscale | 123.968 | 2000–2025 | G7 | % | Nazionale |
| Prezzi Azionari | 4.663 | 1955–2026 | Italia + 5 benchmark | Indice 2015=100 | Nazionale |

> **Nota unità**: Entrate fiscali sono espresse come **% del PIL** (T_SPLIT, settore S13). Non più miliardi EUR — il cambio rende il confronto internazionale diretto.

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
