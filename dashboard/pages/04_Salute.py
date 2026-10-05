"""
Salute — Spesa sanitaria Italia.
"""

import sys
from pathlib import Path

import altair as alt
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from lab_connectors.formatters import fmt_pct
from sources import load_mart

st.title("🏥 Spesa Sanitaria")
st.markdown("Spesa sanitaria italiana — evoluzione storica.")

# --- Evoluzione Italia ---
st.markdown("### Spesa sanitaria Italia (% PIL, 1988-2025)")

try:
    df = load_mart("health", "mart_italia")
    italia = df[
        (df["ref_area"] == "ITA") &
        (df["unita"] == "PT_B1GQ") &
        (df["function_code"] == "_T") &
        (df["financing_scheme"] == "_T")
    ][["anno", "valore"]].sort_values("anno")

    chart = alt.Chart(italia).mark_line(point=True).encode(
        x=alt.X("anno:Q", title="Anno"),
        y=alt.Y("valore:Q", title="% PIL", scale=alt.Scale(domain=[5, 11])),
        tooltip=["anno", "valore"]
    ).properties(height=350)

    # Annotazione COVID
    covid_line = alt.Chart({"values": [{"anno": 2020}]}).mark_rule(color="red", strokeDash=[4, 4]).encode(
        x="anno:Q"
    )
    covid_text = alt.Chart({"values": [{"anno": 2020, "valore": 10.5}]}).mark_text(
        text="COVID", color="red", dy=-10
    ).encode(x="anno:Q", y="valore:Q")

    st.altair_chart(chart + covid_line + covid_text, width="stretch")

    # KPI
    col1, col2, col3 = st.columns(3)
    latest = italia[italia["anno"] == italia["anno"].max()]
    prev = italia[italia["anno"] == italia["anno"].max() - 1]
    if len(latest) > 0 and len(prev) > 0:
        val = latest["valore"].values[0]
        prev_val = prev["valore"].values[0]
        delta = val - prev_val
        col1.metric(f"Spesa {int(latest['anno'].values[0])}", fmt_pct(val), f"{delta:+.2f} pp")
    col2.metric("Picco COVID (2020)", fmt_pct(italia[italia["anno"] == 2020]["valore"].values[0]) if len(italia[italia["anno"] == 2020]) > 0 else "N/D")
    col3.metric("Minimo storico", fmt_pct(italia["valore"].min()))
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Spesa pro capite ---
st.markdown("### Spesa sanitaria pro capite (USD PPP)")

try:
    procapite = df[
        (df["ref_area"] == "ITA") &
        (df["unita"] == "USD_PPP_PS") &
        (df["function_code"] == "_T") &
        (df["financing_scheme"] == "_T")
    ][["anno", "valore"]].sort_values("anno").drop_duplicates("anno")

    chart4 = alt.Chart(procapite).mark_line(point=True).encode(
        x=alt.X("anno:Q", title="Anno"),
        y=alt.Y("valore:Q", title="USD PPP pro capite"),
        tooltip=["anno", "valore"]
    ).properties(height=300)

    st.altair_chart(chart4, width="stretch")
except Exception as e:
    st.warning(f"Errore: {e}")

st.caption("Fonte: OECD ELS.HD · Health Expenditure (SHA) · Benchmark G7 richiede re-download dati OECD")

st.markdown("---")

# --- Benchmark G7 ---
st.markdown("### Benchmark G7 — Spesa sanitaria (% PIL)")

try:
    bm = load_mart("health", "mart_benchmark")
    benchmark = bm[bm["unita"] == "PT_B1GQ"][
        ["anno", "ref_area", "valore"]
    ].dropna()

    if len(benchmark) > 0:
        # Country names mapping
        country_names = {
            "ITA": "Italia", "DEU": "Germania", "FRA": "Francia",
            "GBR": "Regno Unito", "USA": "USA", "JPN": "Giappone", "CAN": "Canada"
        }
        benchmark["paese"] = benchmark["ref_area"].map(country_names).fillna(benchmark["ref_area"])

        # Line chart
        chart = alt.Chart(benchmark).mark_line(point=True).encode(
            x=alt.X("anno:Q", title="Anno"),
            y=alt.Y("valore:Q", title="% PIL"),
            color=alt.Color("paese:N", title="Paese"),
            tooltip=["paese", "anno", "valore"]
        ).properties(height=400)

        st.altair_chart(chart, width="stretch")

        # Latest year comparison
        latest_year = benchmark["anno"].max()
        latest = benchmark[benchmark["anno"] == latest_year].sort_values("valore", ascending=False)

        st.markdown(f"**Confronto {int(latest_year)}:**")
        cols = st.columns(min(len(latest), 7))
        for idx, (_, row) in enumerate(latest.iterrows()):
            if idx < 7:
                cols[idx].metric(
                    row["paese"],
                    fmt_pct(row["valore"]),
                    delta=f"vs ITA: {row['valore'] - latest[latest['ref_area']=='ITA']['valore'].values[0]:+.2f} pp" if row["ref_area"] != "ITA" and len(latest[latest['ref_area']=='ITA']) > 0 else None
                )
    else:
        st.info("Nessun dato benchmark disponibile.")
except Exception as e:
    st.warning(f"Errore benchmark: {e}")

st.caption("Fonte: OECD ELS.HD · Health Expenditure (SHA) · Benchmark G7 (ITA, DEU, FRA, GBR, USA, JPN, CAN)")
