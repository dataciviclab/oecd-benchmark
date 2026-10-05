"""
Economia — PIL e produttività per FUA.
"""

import sys
from pathlib import Path

import altair as alt
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from sources import load_mart

st.title("💰 PIL FUA")
st.markdown("PIL e produttività del lavoro per Functional Urban Area.")

# --- Filtri ---
col1, col2 = st.columns(2)
with col1:
    anno = st.slider("Anno", min_value=2000, max_value=2023, value=2022)
with col2:
    misura = st.selectbox("Indicatore", ["LAB_PROD", "GDP"], format_func=lambda x: "Produttività" if x == "LAB_PROD" else "PIL totale")

# --- Top FUA italiane ---
st.markdown(f"### Top FUA italiane — {('Produttività' if misura == 'LAB_PROD' else 'PIL')} ({anno})")

try:
    df = load_mart("economy", "mart_italia")
    top = df[
        (df["anno"] == anno) &
        (df["misura"] == misura) &
        (df["fua_code"].str.startswith("IT"))
    ].nlargest(15, "valore")

    chart = alt.Chart(top).mark_bar().encode(
        x=alt.X("valore:Q", title="USD PPP" if misura == "LAB_PROD" else "MLN USD PPP"),
        y=alt.Y("citta:N", title="Città", sort="-x"),
        color=alt.value("#2a9d8f"),
        tooltip=["citta", "valore"]
    ).properties(height=400)

    st.altair_chart(chart, width="stretch")
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Confronto con capitali europee ---
st.markdown("### Confronto con capitali europee")

try:
    df_bench = load_mart("economy", "mart_benchmark")
    europe = df_bench[
        (df_bench["anno"] == anno) &
        (df_bench["misura"] == "GDP")
    ][["citta", "valore"]].sort_values("valore", ascending=False)

    europe["gruppo"] = europe["citta"].apply(lambda x: "Italia" if x in ["Milano", "Roma"] else "OCSE")

    chart2 = alt.Chart(europe).mark_bar().encode(
        x=alt.X("valore:Q", title="MLN USD PPP"),
        y=alt.Y("citta:N", title="Città", sort="-x"),
        color=alt.Color("gruppo:N", title="Gruppo", scale=alt.Scale(domain=["Italia", "OCSE"], range=["#e63946", "#457b9d"])),
        tooltip=["citta", "valore"]
    ).properties(height=300)

    st.altair_chart(chart2, width="stretch")
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Trend produttività ---
st.markdown("### Trend produttività (2000-2023)")

cities = st.multiselect(
    "Seleziona città",
    options=["Milano", "Roma", "Torino", "Bologna", "Modena", "Napoli"],
    default=["Milano", "Roma", "Torino"]
)

if cities:
    try:
        trend = df[
            (df["citta"].isin(cities)) &
            (df["misura"] == "LAB_PROD")
        ][["anno", "citta", "valore"]]

        chart3 = alt.Chart(trend).mark_line(point=True).encode(
            x=alt.X("anno:Q", title="Anno"),
            y=alt.Y("valore:Q", title="USD PPP pro capite"),
            color=alt.Color("citta:N", title="Città"),
            tooltip=["anno", "citta", "valore"]
        ).properties(height=350)

        st.altair_chart(chart3, width="stretch")
    except Exception as e:
        st.warning(f"Errore: {e}")

# --- Top 10 regioni italiane PIL ---
st.markdown("---")
st.markdown("### 🇮🇹 Regioni italiane per PIL (TL2)")

try:
    df_gdp = load_mart("gdp", "mart_italia")
    regions = df_gdp[
        (df_gdp["anno"] == anno) &
        (df_gdp["misura"] == "GDP")
    ].sort_values("valore", ascending=False).head(10)

    chart4 = alt.Chart(regions).mark_bar().encode(
        x=alt.X("valore:Q", title="MLN USD"),
        y=alt.Y("paese:N", title="Regione", sort="-x"),
        color=alt.value("#264653"),
        tooltip=["paese", "valore"]
    ).properties(height=300)

    st.altair_chart(chart4, width="stretch")
except Exception as e:
    st.warning(f"Errore: {e}")

st.caption("Fonte: OECD CFE.EDS · FUA Economy + Regional GDP")
