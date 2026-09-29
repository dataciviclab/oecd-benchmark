"""
SQL — Query interattiva sui dati OECD.
"""

import sys
from pathlib import Path

import duckdb
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from sources import DATASETS

st.title("🧪 Query SQL")
st.markdown("Esegui query SQL sui dati OECD processati.")

# --- Selezione dataset ---
dataset = st.selectbox(
    "Seleziona dataset",
    options=list(DATASETS.keys()),
    format_func=lambda x: DATASETS[x]["title"]
)

config = DATASETS[dataset]

# --- Carica dati ---
@st.cache_data(ttl=3600, show_spinner=False)
def load_all_data(dataset_key: str):
    """Carica tutti i parquet del dataset in DuckDB."""
    config = DATASETS[dataset_key]
    con = duckdb.connect()

    # Carica clean
    clean_files = sorted(config["clean"].glob("*.parquet"))
    if clean_files:
        con.execute(f"CREATE VIEW clean AS SELECT * FROM read_parquet({[str(f) for f in clean_files]})")

    # Carica mart_italia
    mart_it_files = sorted(config["mart_italia"].glob("mart_italia*.parquet"))
    if mart_it_files:
        con.execute(f"CREATE VIEW mart_italia AS SELECT * FROM read_parquet({[str(f) for f in mart_it_files]})")

    # Carica mart_benchmark
    mart_bm_files = sorted(config["mart_benchmark"].glob("mart_benchmark*.parquet"))
    if mart_bm_files:
        con.execute(f"CREATE VIEW mart_benchmark AS SELECT * FROM read_parquet({[str(f) for f in mart_bm_files]})")

    return con

try:
    con = load_all_data(dataset)

    # Mostra tabelle disponibili
    st.markdown("### Tabelle disponibili")
    tables = con.execute("SHOW TABLES").fetchall()
    for t in tables:
        count = con.execute(f"SELECT count(*) FROM {t[0]}").fetchone()[0]
        st.info(f"**{t[0]}**: {count:,} righe")

    st.markdown("---")

    # Query predefinite
    st.markdown("### Query predefinite")

    queries = {
        "ghg": {
            "Top 10 città emissioni 2022": """
                SELECT citta, valore as mt_co2e
                FROM mart_benchmark
                WHERE anno = 2022 AND unita = 'T_CO2E' AND pollutante = 'GHG_TOTAL'
                ORDER BY valore DESC LIMIT 10
            """,
            "Trend emissioni Roma": """
                SELECT anno, valore as mt_co2e
                FROM mart_italia
                WHERE citta = 'Roma' AND unita = 'T_CO2E' AND pollutante = 'GHG_TOTAL'
                ORDER BY anno
            """,
            "Emissioni per settore (Italia 2022)": """
                SELECT pollutante_label as settore, ROUND(AVG(valore), 2) as media_mt
                FROM clean
                WHERE fua_code LIKE 'IT%F' AND anno = 2022 AND unita = 'T_CO2E' AND pollutante != 'GHG_TOTAL'
                GROUP BY pollutante_label ORDER BY media_mt DESC
            """,
        },
        "economy": {
            "Top 10 FUA PIL pro capite": """
                SELECT citta, valore as usd_ppp
                FROM mart_italia
                WHERE anno = 2022 AND misura = 'LAB_PROD'
                ORDER BY valore DESC LIMIT 10
            """,
            "Confronto Milano vs europee": """
                SELECT citta, valore as gdp_mln
                FROM mart_benchmark
                WHERE anno = 2022 AND misura = 'GDP'
                ORDER BY valore DESC
            """,
        },
        "health": {
            "Evoluzione spesa sanitaria % PIL": """
                SELECT anno, valore as pct_pil
                FROM mart_italia
                WHERE ref_area = 'ITA' AND unita = 'PT_B1GQ' AND function_code = '_T'
                ORDER BY anno
            """,
        },
        "gdp": {
            "Top 10 regioni PIL": """
                SELECT paese, valore as gdp_mln
                FROM mart_italia
                WHERE anno = 2022 AND misura = 'GDP'
                ORDER BY valore DESC LIMIT 10
            """,
        },
        "education": {
            "Regioni italiane istruzione": """
                SELECT paese as regione, valore as pct_tertiaria
                FROM mart_italia
                WHERE anno = 2022 AND eta = 'Y25T64' AND sesso = '_T'
                ORDER BY valore DESC
            """,
        },
    }

    selected_query = st.selectbox("Seleziona query", options=list(queries.get(dataset, {}).keys()))
    sql = st.text_area("SQL", value=queries.get(dataset, {}).get(selected_query, ""), height=150)

    if st.button("Esegui", type="primary"):
        try:
            result = con.execute(sql).fetchdf()
            st.dataframe(result, use_container_width=True, hide_index=True)
            st.caption(f"{len(result)} righe restituite")
        except Exception as e:
            st.error(f"Errore SQL: {e}")

except Exception as e:
    st.error(f"Errore nel caricamento dati: {e}")

st.markdown("---")
st.caption("Scrivi SQL direttamente o usa le query predefinite. Le tabelle disponibili dipendono dal dataset selezionato.")
