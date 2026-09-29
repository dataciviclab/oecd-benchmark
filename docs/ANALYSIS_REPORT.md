# OECD Data Analysis — Report

**Data**: 2026-09-27
**Dataset analizzati**: 5 (GHG, FUA Economy, Health Expenditure, Regional GDP, Education Attainment)

---

## 1. Emissioni GHG — Città italiane vs mondiali

### Posizionamento Italia
| Città | Emissioni 2022 (Mt CO2e) | Ranking mondiale |
|---|---|---|
| Roma | 20.0 | 67° |
| Milano | 18.9 | 72° |
| Torino | 8.9 | 170° |
| Ravenna | 7.4 | 203° |
| Brindisi | 7.0 | 220° |

### Confronto con capitali europee
| Città | Emissioni 2022 (Mt CO2e) |
|---|---|
| London | 37.0 |
| Paris | 36.1 |
| Berlin | 23.7 |
| **Roma** | **20.0** |
| **Milano** | **18.9** |
| Madrid | 18.8 |
| Barcelona | 14.5 |

**Insight**: Le città italiane sono nella media europea, molto più basse delle americane (LA: 131 Mt, NY: 112 Mt).

### Evoluzione temporale (1990-2024)
- Roma: -14% (22.0 → 18.9 Mt)
- Milano: -1% (18.1 → 17.8 Mt) — stagnante
- Trend positivo generale, ma lento

### Emissioni per settore (Italia, 2022)
| Settore | Media Mt CO2e | % del totale |
|---|---|---|
| Industria | 0.51 | 24.4% |
| Manifattura | 0.49 | 23.4% |
| Trasporto stradale | 0.45 | 21.4% |
| Trasporti | 0.45 | 21.6% |
| Edilizia | 0.45 | 21.4% |
| Energia | 0.44 | 21.1% |
| Rifiuti | 0.13 | 6.3% |
| Agricoltura | 0.11 | 5.2% |

### Variazione per settore (1990 vs 2022)
| Settore | Var % |
|---|---|
| Manifattura | **-43.9%** |
| Industria | **-42.6%** |
| Energia | -32.8% |
| Agricoltura | -31.3% |
| Edilizia | -15.4% |
| Rifiuti | -3.9% |
| Trasporti | **+6.4%** ⚠️ |

**Insight critico**: I trasporti sono l'unico settore in crescita (+6.4%). Industria e manifattura hanno ridotto le emissioni del 43%.

---

## 2. PIL Pro Capite — FUA italiane

### Top 10 città italiane (USD PPP, 2022)
| Città | PIL pro capite |
|---|---|
| Milano | $148,811 |
| Modena | $132,675 |
| Bologna | $130,882 |
| Roma | $130,468 |
| Reggio nell'Emilia | $129,948 |
| Brescia | $128,952 |
| Bergamo | $126,791 |
| Parma | $124,504 |
| Firenze | $123,982 |
| Genova | $119,752 |

**Insight**: L'Emilia-Romagna domina con 4 città nei top 10. Milano è competitiva con le capitali europee.

---

## 3. Istruzione Terziaria — Disuguaglianze regionali

### Regioni italiane (pop. 25-64 con istruzione terziaria, 2022)
| Regione | % |
|---|---|
| Lazio | 26.7% |
| Emilia-Romagna | 22.8% |
| Marche | 22.6% |
| Umbria | 22.5% |
| Liguria | 22.3% |
| Lombardy | 21.8% |
| ... | ... |
| Campania | 16.9% |
| Calabria | 16.6% |
| Apulia | 16.2% |
| Sicilia | 15.2% |

**Disuguaglianza Nord-Sud**: 21.3% vs 17.8% (3.5 punti)

**Insight**: Il divario è enorme — Lazio ha quasi il doppio della Sicilia. Media italiana (~20%) sotto la media OCSE (~35%).

---

## 4. Spesa Sanitaria — Italia in crescita

### Evoluzione % PIL
| Anno | % PIL |
|---|---|
| 1988 | 6.6% |
| 2000 | 7.5% |
| 2010 | 8.9% |
| 2020 | 9.6% (COVID) |
| 2024 | 8.5% |

**Insight**: La spesa è cresciuta del 29% in 36 anni. Il COVID ha causato un picco temporaneo al 9.6%.

---

## 5. Key Findings per il Lab

### 🎯 Priorità analisi
1. **Trasporti**: unico settore in crescita (+6.4%) — candidato per investigazione
2. **Disuguaglianza Nord-Sud**: istruzione e PIL mostrano divari strutturali
3. **Competitività Milano**: PIL pro capite al livello delle capitali europee
4. **Emissioni contenute**: l'Italia è sotto la media europea — potenziale narrative

### 🔗 Intrecci possibili con dataset Lab
- `terna_emissioni_co2`: confronto emissioni elettriche vs totali
- `rifiuti-urbani`: correlazione gestione rifiuti vs emissioni GHG
- `pil-intelligence`: confronto PIL regionale italiano con OECD
- `open-conto-annuale`: spesa sanitaria PA vs dati OECD

### 📊 Dataset pronti per pubblicazione
Tutti e 5 i dataset sono processati e validati, pronti per:
- Analisi SQL nel toolkit
- Export parquet per DuckDB
- Integrazione in dashboard o report

---

*Report generato automaticamente dai dati OECD processati il 2026-09-27*
