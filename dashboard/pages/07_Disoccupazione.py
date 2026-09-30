"""
Disoccupazione — Tasso di disoccupazione Italia vs G7.
"""

import sys
from pathlib import Path

import altair as alt
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from lab_connectors.formatters import fmt_pct
from sources import load_mart

st.title("👷 Disoccupazione")
st.markdown("Tasso di disoccupazione Italia confrontato con paesi G7.")

# --- Evoluzione Italia ---
st.markdown("### Tasso di disoccupazione Italia (2000-2025)")

try:
    df = load_mart("unemployment", "mart_italia")
    df["anno"] = df["anno"].astype(int)

    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("anno:Q", title="Anno"),
        y=alt.Y("media_annuale:Q", title="% forza lavoro"),
        tooltip=["anno", "media_annuale"]
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)

    # KPI
    col1, col2, col3 = st.columns(3)
    latest = df[df["anno"] == df["anno"].max()]
    if len(latest) > 0:
        col1.metric(f"Disoccupazione {int(latest['anno'].values[0])}", fmt_pct(latest['media_annuale'].values[0]))
    col2.metric("Minimo storico", fmt_pct(df["media_annuale"].min()))
    col3.metric("Massimo storico", fmt_pct(df["media_annuale"].max()))
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Confronto G7 ---
st.markdown("### Confronto paesi G7 (ultimi dati disponibili)")

try:
    df_bench = load_mart("unemployment", "mart_benchmark")
    g7_codes = ["ITA", "DEU", "FRA", "GBR", "USA", "JPN", "CAN", "OECD"]
    g7_names = {
        "ITA": "Italia", "DEU": "Germania", "FRA": "Francia",
        "GBR": "UK", "USA": "USA", "JPN": "Giappone", "CAN": "Canada",
        "OECD": "Media OCSE"
    }
    g7_colors = {
        "ITA": "#e63946", "DEU": "#457b9d", "FRA": "#457b9d",
        "GBR": "#457b9d", "USA": "#457b9d", "JPN": "#457b9d",
        "CAN": "#457b9d", "OECD": "#2a9d8f"
    }

    g7 = df_bench[df_bench["ref_area"].isin(g7_codes)].copy()
    g7["paese"] = g7["ref_area"].map(g7_names)
    g7["colore"] = g7["ref_area"].map(g7_colors)

    # Prendi ultimo anno disponibile per ogni paese
    latest = g7.sort_values("anno", ascending=False).drop_duplicates("ref_area")

    chart2 = alt.Chart(latest).mark_bar().encode(
        x=alt.X("media_annuale:Q", title="% forza lavoro"),
        y=alt.Y("paese:N", title="Paese", sort="-x"),
        color=alt.Color("colore:N", scale=None, legend=None),
        tooltip=["paese", "anno", "media_annuale"]
    ).properties(height=300)

    st.altair_chart(chart2, use_container_width=True)

    # Tabella dettaglio
    st.dataframe(
        latest[["paese", "anno", "media_annuale"]].rename(columns={
            "paese": "Paese",
            "anno": "Anno",
            "media_annuale": "% Disoccupazione"
        }).sort_values("% Disoccupazione", ascending=False),
        use_container_width=True,
        hide_index=True
    )
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Trend confronto ---
st.markdown("### Evoluzione disoccupazione (2000-2025)")

try:
    countries_to_show = st.multiselect(
        "Seleziona paesi",
        options=g7_codes,
        default=["ITA", "DEU", "FRA", "GBR", "USA"]
    )

    if countries_to_show:
        trend = g7[g7["ref_area"].isin(countries_to_show)].copy()
        trend["anno"] = trend["anno"].astype(int)

        chart3 = alt.Chart(trend).mark_line(point=True).encode(
            x=alt.X("anno:Q", title="Anno"),
            y=alt.Y("media_annuale:Q", title="% forza lavoro"),
            color=alt.Color("paese:N", title="Paese"),
            tooltip=["anno", "paese", "media_annuale"]
        ).properties(height=350)

        st.altair_chart(chart3, use_container_width=True)
except Exception as e:
    st.warning(f"Errore: {e}")

st.caption("Fonte: OECD SDD.TPS · Labour Force Survey")
