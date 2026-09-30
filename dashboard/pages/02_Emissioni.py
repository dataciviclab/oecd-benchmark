"""
Emissioni GHG — Analisi emissioni per città.
"""

import sys
from pathlib import Path

import altair as alt
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from sources import load_mart

st.title("🏭 Emissioni GHG Città")
st.markdown("Emissioni di gas a effetto serra per Functional Urban Area (FUA).")

# --- Filtri ---
col1, col2 = st.columns(2)
with col1:
    anno = st.slider("Anno", min_value=1990, max_value=2024, value=2022)
with col2:
    top_n = st.slider("Top N città", min_value=5, max_value=30, value=15)

# --- Top città mondiali ---
st.markdown(f"### Top {top_n} città mondiali ({anno})")

try:
    df = load_mart("ghg", "mart_benchmark")
    top = df[
        (df["anno"] == anno) &
        (df["unita"] == "T_CO2E") &
        (df["pollutante"] == "GHG_TOTAL")
    ].nlargest(top_n, "valore")

    top["gruppo"] = top["fua_code"].apply(lambda x: "Italia" if str(x).startswith("IT") else "OCSE")

    chart = alt.Chart(top).mark_bar().encode(
        x=alt.X("valore:Q", title="Mt CO2e"),
        y=alt.Y("citta:N", title="Città", sort="-x"),
        color=alt.Color("gruppo:N", title="Gruppo", scale=alt.Scale(domain=["Italia", "OCSE"], range=["#e63946", "#457b9d"])),
        tooltip=["citta", "valore"]
    ).properties(height=max(300, top_n * 25))

    st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Italia dettaglio ---
st.markdown("### 🇮🇹 Città italiane")

try:
    italy = df[
        (df["anno"] == anno) &
        (df["unita"] == "T_CO2E") &
        (df["pollutante"] == "GHG_TOTAL") &
        (df["fua_code"].str.startswith("IT"))
    ].sort_values("valore", ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        chart2 = alt.Chart(italy.head(15)).mark_bar().encode(
            x=alt.X("valore:Q", title="Mt CO2e"),
            y=alt.Y("citta:N", title="Città", sort="-x"),
            color=alt.value("#2a9d8f"),
            tooltip=["citta", "valore", "ranking"]
        ).properties(height=400)
        st.altair_chart(chart2, use_container_width=True)

    with col2:
        st.dataframe(
            italy[["citta", "valore", "ranking"]].head(15).rename(columns={
                "citta": "Città",
                "valore": "Mt CO2e",
                "ranking": "Ranking"
            }),
            use_container_width=True,
            hide_index=True
        )
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Evoluzione temporale ---
st.markdown("### Evoluzione temporale (1990-2024)")

try:
    df_cities = load_mart("ghg", "mart_italia")
    cities = sorted(df_cities[df_cities["fua_code"].str.endswith("F")]["citta"].unique())
except Exception:
    cities = []

cities_to_show = st.multiselect(
    "Seleziona città",
    options=cities,
    default=[c for c in ["Roma", "Milano", "Torino", "Napoli"] if c in cities]
)

if cities_to_show:
    try:
        df_trend = load_mart("ghg", "mart_italia")
        trend = df_trend[
            (df_trend["citta"].isin(cities_to_show)) &
            (df_trend["unita"] == "T_CO2E") &
            (df_trend["pollutante"] == "GHG_TOTAL")
        ][["anno", "citta", "valore"]]

        chart3 = alt.Chart(trend).mark_line(point=True).encode(
            x=alt.X("anno:Q", title="Anno"),
            y=alt.Y("valore:Q", title="Mt CO2e"),
            color=alt.Color("citta:N", title="Città"),
            tooltip=["anno", "citta", "valore"]
        ).properties(height=350)

        st.altair_chart(chart3, use_container_width=True)
    except Exception as e:
        st.warning(f"Errore: {e}")

# --- Emissioni per settore ---
st.markdown("---")
st.markdown("### Emissioni per settore (Italia, media FUA)")

try:
    from sources import query as _query
    sector = _query("ghg", """
        SELECT pollutante_label, AVG(valore) as valore
        FROM clean_input
        WHERE fua_code LIKE 'IT%'
          AND anno = 2022
          AND unita = 'T_CO2E'
          AND pollutante != 'GHG_TOTAL'
        GROUP BY pollutante_label
        ORDER BY valore
    """)

    chart4 = alt.Chart(sector).mark_bar().encode(
        x=alt.X("valore:Q", title="Media Mt CO2e"),
        y=alt.Y("pollutante_label:N", title="Settore", sort="-x"),
        color=alt.value("#264653"),
        tooltip=["pollutante_label", "valore"]
    ).properties(height=250)

    st.altair_chart(chart4, use_container_width=True)
except Exception as e:
    st.warning(f"Errore: {e}")

st.caption("Fonte: OECD ENV.EPI · FUA Environment GHG")
