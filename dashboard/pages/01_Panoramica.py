"""
Panoramica — Visione d'insieme dei dati OECD.
"""

import sys
from pathlib import Path

import altair as alt
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from sources import fmt_mt, fmt_num, fmt_pct, load_mart

st.title("🌍 OECD Data Explorer")
st.markdown("**Benchmark internazionale**: emissioni, PIL, salute, istruzione — dati OCSE per l'Italia.")

# --- KPI Cards ---
st.markdown("### Indicatori chiave (2022)")

col1, col2, col3, col4 = st.columns(4)

# Emissioni Roma
try:
    df_ghg = load_mart("ghg", "mart_benchmark")
    roma_2022 = df_ghg[(df_ghg["citta"] == "Roma") & (df_ghg["anno"] == 2022)]["valore"].values
    roma_val = roma_2022[0] if len(roma_2022) > 0 else 0
    col1.metric("🏭 Roma", fmt_mt(roma_val), "Mt CO2e")
except Exception:
    col1.metric("🏭 Roma", "N/D")

# PIL Milano
try:
    df_eco = load_mart("economy", "mart_italia")
    milano_2022 = df_eco[(df_eco["citta"] == "Milano") & (df_eco["anno"] == 2022) & (df_eco["misura"] == "LAB_PROD")]["valore"].values
    milano_val = milano_2022[0] if len(milano_2022) > 0 else 0
    col2.metric("💰 Milano", f"${fmt_num(milano_val, 0)}", "PIL pro capite PPP")
except Exception:
    col2.metric("💰 Milano", "N/D")

# Spesa sanitaria
try:
    df_health = load_mart("health", "mart_italia")
    health_2022 = df_health[
        (df_health["anno"] == 2022) &
        (df_health["unita"] == "PT_B1GQ") &
        (df_health["function_code"] == "_T")
    ]["valore"].values
    health_val = health_2022[0] if len(health_2022) > 0 else 0
    col3.metric("🏥 Italia", fmt_pct(health_val), "Spesa sanitaria % PIL")
except Exception:
    col3.metric("🏥 Italia", "N/D")

# Istruzione
try:
    df_edu = load_mart("education", "mart_italia")
    edu_2022 = df_edu[(df_edu["anno"] == 2022) & (df_edu["eta"] == "Y25T64")]["valore"].values
    edu_val = edu_2022.mean() if len(edu_2022) > 0 else 0
    col4.metric("🎓 Italia", fmt_pct(edu_val), "Istruzione terziaria")
except Exception:
    col4.metric("🎓 Italia", "N/D")

st.markdown("---")

# --- Trend emissioni 30 anni ---
st.markdown("### Trend emissioni GHG (1990-2024)")

try:
    df_trend = load_mart("ghg", "mart_italia")
    cities = ["Roma", "Milano", "Torino", "Napoli"]
    trend_data = df_trend[
        (df_trend["citta"].isin(cities)) &
        (df_trend["unita"] == "T_CO2E") &
        (df_trend["pollutante"] == "GHG_TOTAL")
    ][["anno", "citta", "valore"]]

    chart = alt.Chart(trend_data).mark_line(point=True).encode(
        x=alt.X("anno:Q", title="Anno"),
        y=alt.Y("valore:Q", title="Mt CO2e"),
        color=alt.Color("citta:N", title="Città"),
        tooltip=["anno", "citta", "valore"]
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.warning(f"Errore nel caricamento trend: {e}")

# --- Confronto emissioni con Europa ---
st.markdown("### Emissioni GHG — Confronto città europee (2022)")

try:
    df_bench = load_mart("ghg", "mart_benchmark")
    europe = df_bench[
        (df_bench["anno"] == 2022) &
        (df_bench["unita"] == "T_CO2E") &
        (df_bench["pollutante"] == "GHG_TOTAL") &
        (df_bench["fua_code"].isin([
            "IT001F", "IT002F", "IT004F",  # Roma, Milano, Torino
            "UK001F", "FR001F", "DE001F",  # London, Paris, Berlin
            "ES001F", "ES002F"             # Madrid, Barcelona
        ]))
    ][["citta", "valore"]].sort_values("valore", ascending=True)

    europe["gruppo"] = europe["citta"].apply(lambda x: "Italia" if x in ["Roma", "Milano", "Torino"] else "OCSE")

    chart2 = alt.Chart(europe).mark_bar().encode(
        x=alt.X("valore:Q", title="Mt CO2e"),
        y=alt.Y("citta:N", title="Città", sort="-x"),
        color=alt.Color("gruppo:N", title="Gruppo", scale=alt.Scale(domain=["Italia", "OCSE"], range=["#e63946", "#457b9d"])),
        tooltip=["citta", "valore"]
    ).properties(height=300)

    st.altair_chart(chart2, use_container_width=True)
except Exception as e:
    st.warning(f"Errore nel caricamento benchmark: {e}")

# --- Note ---
st.markdown("---")
st.caption("""
**Fonte**: OECD Data Explorer (SDMX API) · Dati: 1990-2024 · Aggiornato: 2026-09-27
""")
