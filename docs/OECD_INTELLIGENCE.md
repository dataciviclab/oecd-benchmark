# OECD Intelligence — Piano di implementazione

## Contesto
Il Lab ha forte copertura su dati italiani (ISTAT, Eurostat, ANAC, ecc.) ma manca di benchmark internazionali. L'API OECD (sdmx.oecd.org) fornisce 1.548 dataflows con dati comparativi su economia, ambiente, salute, istruzione, governance.

## Stato attuale (aggiornato 2026-09-27)

### Dataset implementati — Fase 1 (ENV.EPI)
| Dataset | Flow |Dims | Stato |
|---|---|---|---|
| `oecd-env-epi-air-emissions` | `DSD_AIR_EMISSIONS@DF_AIR_EMISSIONS` | 5 | ✅ 62 righe mart |
| `oecd-env-epi-green-transition` | `DSD_GREEN_TRANSITION@DF_GREEN_TRANSITION` | 4 | ✅ 59 righe mart |
| `oecd-env-epi-forest` | `DSD_FOREST@DF_FOREST` | 4 | ✅ 49 righe mart |
| `oecd-health-expenditure` | `DSD_SHA@DF_SHA` | 12 | ✅ 168 righe mart |

### Dataset implementati — Fase 2 (CFE.EDS + benchmark)
| Dataset | Flow |Dims | Stato |
|---|---|---|---|
| `oecd-fua-environment-ghg` | `DSD_FUA_ENV@DF_GHG,1.5` | 8 | ✅ 1.6M clean, 5.7K mart_italia, 42K mart_benchmark |
| `oecd-fua-economy` | `DSD_FUA_ECO@DF_ECONOMY,1.1` | 5 | ✅ 58K clean, 2.2K mart_italia, 660 mart_benchmark |
| `oecd-health-expenditure` | `DSD_SHA@DF_SHA,1.1` | 12 | ✅ 71K clean, 6.7K mart_italia, 6.7K mart_benchmark |
| `oecd-regional-gdp` | `DSD_REG_ECO@DF_GDP,2.4` | 8 | ✅ 971K clean, 7.5K mart_italia, 211K mart_benchmark |
| `oecd-education-attainment` | `DSD_REG_EDU@DF_ATTAIN,2.5` | 10 | ✅ 338K clean, 3.1K mart_italia, 10K mart_benchmark |

### Dataset esplorati ma non funzionanti
| Dataset | Flow | Motivo |
|---|---|---|
| `DSD_REG_ECO@DF_GDP` | OECD.CFE.EDS | 404 — forse restricted o codici diversi |
| `DSD_REG_HEALTH@DF_HEALTH` | OECD.CFE.EDS | 404 — forse restricted o codici diversi |
| `DSD_NAAG@DF_NAAG_I` | OECD.SDD.NAD | 404 — forse restricted |
| `DSD_TIVA@DF_TIVA1` | OECD.TAD.TAD | Agency vuota (0 dataflows) |

## Struttura OECD API

### Regole chiave
```
Flow ref:  AGENCY,DATASET_ID@FLOW_ID,VERSION
Key:       DIM1.DIM2.DIM3... (punti tra le dimensioni)
Formato:   ?format=csvfilewithlabels (query param, non Accept header)
Versione:  Sempre nel path (unlike Eurostat)
Rate limit: ~10-15 req rapide prima di 429 (consigliare 5-10s pause)
```

### Pattern delle agenzie
| Agenzia | Tipo dati | REF_AREA | Esempio |
|---|---|---|---|
| `OECD.ELS.HD` | Nazionali | `ITA` (ISO 3166) | `DSD_SHA@DF_SHA` ✅ |
| `OECD.ENV.EPI` | Nazionali | `ITA` | `DSD_AIR_EMISSIONS` ✅ |
| `OECD.CFE.EDS` | **Città (FUA)** | Codici FUA | `DSD_FUA_ENV@DF_GHG` ✅ |
| `OECD.CFE.EDS` | Regionali (TL2) | `ITA` | `DSD_REG_ECO@DF_GDP` ✅ (versione 2.4) |
| `OECD.CTP.TPS` | Nazionali | `ITA` | `DSD_TAX_WAGES_COMP@DF_TW_COMP` ✅ |
| `OECD.SDD.NAD` | Nazionali | `IT` (ISO2) | `DSD_NAAG@DF_NAAG_I` ❌ |

## Lesson learned — Fase 2

### 1. CSV problematici OECD
- **Righe con virgola nei nomi città**: `ignore_errors: true` + `nullstr: "Not applicable"` nel read config
- **TIME_PERIOD con "Not applicable"**: forzare `nullstr` nel read per gestire valori non-anno
- **31 colonne invece di 30**: causato da virgola non quotata nel nome città (es. "Puerto de Santa María, El")

### 2. FUA lookup — filtro `LIKE 'IT%'` funziona
- I codici FUA italiani iniziano con `IT` (es. IT001F=Roma, IT002F=Milano)
- Suffissi: `F` = FUA (area funzionale), `C` = City (nucleo urbano)
- `read_csv_auto()` in CTE DuckDB non funziona — usare filtro LIKE direttamente su clean_input

### 3. Nomenclatura OECD diversa da attesa
- **Pollutanti**: `GHG_TOTAL` (non `CO2`), `GHG_POWER`, `GHG_BUILDINGS`, ecc.
- **Unità**: `T_CO2E` (Tonnes of CO2-equivalent), `T_CO2E_PS` (per person)
- **Misura**: `B1GQ` (GDP), `PROD_L` (labour productivity)

### 4. Dati FUA Italiani nel dataset GHG
- **165 FUA italiane** trovate nei dati (1990-2024)
- **Top 5 emissioni 2024**: Roma (18.9 Mt), Milano (17.8 Mt), Torino (7.7 Mt), Ravenna (7.0 Mt), Napoli (5.0 Mt)
- **Benchmark**: Tokyo (136 Mt), Los Angeles (125 Mt), Seoul (116 Mt)

### 5. Rate limiting OECD
- API pubblica senza chiave ma rate limit stretto (~10-15 req rapide)
- Soluzione: pause 5-10s tra request, o meglio: scaricare tutti i dati in una volta con key vuota
- Per FUA dataset: ~560K righe raw (tutte le città OCSE) — gestibile

### 6. Nomenclatura diversa per dataset
- **Regional GDP**: ref_area = codici NUTS (ITC2, ITC34...) non `ITA`; misura = `GDP`, `EMP`, `POP`
- **Education**: educazione = `ISCED11_5T8` (non `ISCED11_5_8`); eta = `Y25T64` (non `25_64`); sesso = `_T` (non `T`)
- **Health**: misura = `EXP_HEALTH`; financing_scheme = `_T` (totale); provider = `_T` (totale)
- **FUA Economy**: misura = `GDP`, `LAB_PROD`, `EMPW` (non `GDP_L`, `PROD_L`)

## Script esplorativi
```bash
# 1. Lista tutti i dataflows
curl -s "https://sdmx.oecd.org/public/rest/dataflow" | python3 -c "
import json,sys; d=json.load(sys.stdin)
for f in d['data']['dataflows']:
    print(f'{f[\"agencyID\"]}/{f[\"id\"]} v{f.get(\"version\")}')
"

# 2. Struttura dati (dimensioni)
curl -s "https://sdmx.oecd.org/public/rest/datastructure/AGENCY/DSD_ID" | python3 -c "
import xml.etree.ElementTree as ET,sys
root=ET.fromstring(sys.stdin.read())
ns={'str':'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'}
dims=[d.attrib['id'] for d in root.findall('.//str:Dimension',ns) if d.attrib.get('id')]
print(f'{len(dims)} dims: {dims}')
"

# 3. Fetch dati
curl -s "https://sdmx.oecd.org/public/rest/data/AGENCY,FLOW_ID,VERSION/KEY?format=csvfilewithlabels"
```

## Prossimi passi
1. ✅ Eseguire `oecd-fua-economy` (PIL FUA) — completato
2. ✅ Eseguire `oecd-health-expenditure` (spesa sanitaria) — completato
3. ✅ Eseguire `oecd-regional-gdp` (PIL regionale) — completato
4. ✅ Eseguire `oecd-education-attainment` (istruzione) — completato
5. Intrecciare con dataset Lab esistenti (terna_emissioni_co2, pil-intelligence, BES)
6. Promuovere in incubation/ se i risultati sono interessanti
7. Aggiungere TiVA (Trade in Value Added) quando disponibile
