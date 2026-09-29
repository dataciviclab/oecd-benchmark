"""
OECD Data Explorer — Data Sources
Loader per i 5 dataset OECD processati.
"""

from pathlib import Path

import streamlit as st

# Base path per i parquet
BASE = Path(__file__).parent.parent / "out" / "data"

# Dataset config
DATASETS = {
    "ghg": {
        "slug": "oecd_fua_ghg",
        "clean": BASE / "clean" / "oecd_fua_ghg" / "2026",
        "mart_italia": BASE / "mart" / "oecd_fua_ghg" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_fua_ghg" / "2026",
        "title": "Emissioni GHG Città",
    },
    "economy": {
        "slug": "oecd_fua_economy",
        "clean": BASE / "clean" / "oecd_fua_economy" / "2026",
        "mart_italia": BASE / "mart" / "oecd_fua_economy" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_fua_economy" / "2026",
        "title": "PIL FUA",
    },
    "health": {
        "slug": "oecd_health_expenditure",
        "clean": BASE / "clean" / "oecd_health_expenditure" / "2026",
        "mart_italia": BASE / "mart" / "oecd_health_expenditure" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_health_expenditure" / "2026",
        "title": "Spesa Sanitaria",
    },
    "gdp": {
        "slug": "oecd_regional_gdp",
        "clean": BASE / "clean" / "oecd_regional_gdp" / "2026",
        "mart_italia": BASE / "mart" / "oecd_regional_gdp" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_regional_gdp" / "2026",
        "title": "PIL Regionale",
    },
    "education": {
        "slug": "oecd_education_attainment",
        "clean": BASE / "clean" / "oecd_education_attainment" / "2026",
        "mart_italia": BASE / "mart" / "oecd_education_attainment" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_education_attainment" / "2026",
        "title": "Istruzione",
    },
    "unemployment": {
        "slug": "oecd_unemployment",
        "clean": BASE / "clean" / "oecd_unemployment" / "2026",
        "mart_italia": BASE / "mart" / "oecd_unemployment" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_unemployment" / "2026",
        "title": "Disoccupazione",
    },
    "tax_revenue": {
        "slug": "oecd_tax_revenue",
        "clean": BASE / "clean" / "oecd_tax_revenue" / "2026",
        "mart_italia": BASE / "mart" / "oecd_tax_revenue" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_tax_revenue" / "2026",
        "title": "Entrate Fiscali",
    },
    "taxing_wages": {
        "slug": "oecd_taxing_wages",
        "clean": BASE / "clean" / "oecd_taxing_wages" / "2026",
        "mart_italia": BASE / "mart" / "oecd_taxing_wages" / "2026",
        "mart_benchmark": BASE / "mart" / "oecd_taxing_wages" / "2026",
        "title": "Cuneo Fiscale",
    },
}


def _glob_parquet(directory: Path, pattern: str = "*.parquet") -> list[Path]:
    """Trova tutti i file parquet in una directory."""
    return sorted(directory.glob(pattern))


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart(dataset: str, table: str = "mart_italia"):
    """Carica una tabella mart da parquet e restituisce un DataFrame."""
    import duckdb
    config = DATASETS[dataset]
    directory = config[table]
    # Cerca il file specifico per il nome tabella
    pattern = f"{table}*.parquet"
    files = sorted(directory.glob(pattern))
    if not files:
        # Fallback: cerca qualsiasi parquet
        files = sorted(directory.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"Nessun parquet trovato in {directory}")
    paths = [str(f) for f in files]
    if len(paths) == 1:
        return duckdb.sql(f"SELECT * FROM read_parquet('{paths[0]}')").fetchdf()
    else:
        return duckdb.sql(f"SELECT * FROM read_parquet({paths}, union_by_name=true)").fetchdf()


@st.cache_data(ttl=3600, show_spinner=False)
def load_clean(dataset: str):
    """Carica i dati clean da parquet e restituisce un DataFrame."""
    import duckdb
    config = DATASETS[dataset]
    files = _glob_parquet(config["clean"])
    if not files:
        raise FileNotFoundError(f"Nessun parquet trovato in {config['clean']}")
    paths = [str(f) for f in files]
    return duckdb.sql(f"SELECT * FROM read_parquet({paths})").fetchdf()


@st.cache_data(ttl=3600, show_spinner=False)
def query_data(sql: str):
    """Esegui una query SQL arbitraria sui dati OECD e restituisce un DataFrame."""
    import duckdb
    return duckdb.sql(sql).fetchdf()


# --- Funzioni di formattazione ---

def fmt_num(x: float, decimals: int = 1) -> str:
    """Formatta un numero con separatore migliaia."""
    if x is None:
        return "-"
    return f"{x:,.{decimals}f}"


def fmt_pct(x: float, decimals: int = 1) -> str:
    """Formatta una percentuale."""
    if x is None:
        return "-"
    return f"{x:.{decimals}f}%"


def fmt_mt(x: float) -> str:
    """Formatta emissioni in milioni di tonnellate."""
    if x is None:
        return "-"
    return f"{x:,.1f} Mt"


# --- Query predefinite ---

QUERY_GHG_TOP_CITIES = """
SELECT citta, valore as mt_co2e
FROM {table}
WHERE anno = :anno
  AND unita = 'T_CO2E'
  AND pollutante = 'GHG_TOTAL'
ORDER BY valore DESC
LIMIT :limit
"""

QUERY_GHG_TREND = """
SELECT anno, citta, valore as mt_co2e
FROM {table}
WHERE citta IN :cities
  AND unita = 'T_CO2E'
  AND pollutante = 'GHG_TOTAL'
ORDER BY anno, citta
"""

QUERY_ECONOMY_GDP = """
SELECT citta, valore as gdp_per_capita, unita
FROM {table}
WHERE anno = :anno
  AND misura = 'LAB_PROD'
ORDER BY valore DESC
LIMIT :limit
"""

QUERY_HEALTH_EVOLUTION = """
SELECT anno, valore as pct_pil
FROM {table}
WHERE ref_area = 'ITA'
  AND unita = 'PT_B1GQ'
  AND function_code = '_T'
ORDER BY anno
"""

QUERY_EDUCATION_REGIONS = """
SELECT paese as regione, valore as pct_tertiaria
FROM {table}
WHERE anno = :anno
  AND eta = 'Y25T64'
  AND sesso = '_T'
ORDER BY valore DESC
"""
