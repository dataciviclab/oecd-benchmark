"""
Fisco — Entrate fiscali e cuneo fiscale Italia vs G7.
"""

import sys
from pathlib import Path

import altair as alt
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from sources import load_mart

st.title("🏛️ Fisco")
st.markdown("Entrate fiscali e struttura del cuneo fiscale italiano.")

tab1, tab2 = st.tabs(["Entrate Fiscali", "Cuneo Fiscale"])

# --- TAB 1: Entrate Fiscali ---
with tab1:
    st.markdown("### Entrate fiscali Italia — Evoluzione")

    try:
        df = load_mart("tax_revenue", "mart_italia")

        # Entrate totali (S13 = General government)
        total = df[
            (df["misura"] == "TAX_REV") &
            (df["settore"] == "S13")
        ][["anno", "valore"]].sort_values("anno")
        total["valore_mld"] = total["valore"] / 1000  # Convert to billions

        chart = alt.Chart(total).mark_line(point=True).encode(
            x=alt.X("anno:Q", title="Anno"),
            y=alt.Y("valore_mld:Q", title="Miliardi EUR"),
            tooltip=["anno", "valore_mld"]
        ).properties(height=350)

        st.altair_chart(chart, use_container_width=True)

        # KPI
        col1, col2 = st.columns(2)
        if len(total) > 0:
            latest = total[total["anno"] == total["anno"].max()]
            prev = total[total["anno"] == total["anno"].max() - 1]
            if len(latest) > 0 and len(prev) > 0:
                val = latest["valore_mld"].values[0]
                prev_val = prev["valore_mld"].values[0]
                delta = (val - prev_val) / prev_val * 100
                col1.metric(f"Entrate {int(latest['anno'].values[0])}", f"€{val:.1f}B", f"{delta:+.1f}%")
            col2.metric("Crescita 20 anni", f"{(total['valore_mld'].iloc[-1] / total['valore_mld'].iloc[0] - 1) * 100:.0f}%" if len(total) > 1 else "N/D")
    except Exception as e:
        st.warning(f"Errore: {e}")

    st.markdown("---")

    st.markdown("### Composizione entrate per settore (Italia, 2022)")

    try:
        from sources import load_clean
        df_clean = load_clean("tax_revenue")
        composition = df_clean[
            (df_clean["anno"] == 2022) &
            (df_clean["settore"] != "S13") &
            (df_clean["valore"] > 0)
        ].groupby("settore_label")["valore"].max().reset_index()
        composition = composition.sort_values("valore", ascending=True)

        chart2 = alt.Chart(composition).mark_bar().encode(
            x=alt.X("valore:Q", title="EUR"),
            y=alt.Y("settore_label:N", title="Settore", sort="-x"),
            color=alt.value("#2a9d8f"),
            tooltip=["settore_label", "valore"]
        ).properties(height=300)

        st.altair_chart(chart2, use_container_width=True)
    except Exception as e:
        st.warning(f"Errore: {e}")

# --- TAB 2: Cuneo Fiscale ---
with tab2:
    st.markdown("### Cuneo fiscale — Confronto G7")

    try:
        df_wages = load_mart("taxing_wages", "mart_benchmark")
        g7_codes = ["ITA", "DEU", "FRA", "GBR", "USA", "JPN", "CAN"]
        g7_names = {
            "ITA": "Italia", "DEU": "Germania", "FRA": "Francia",
            "GBR": "UK", "USA": "USA", "JPN": "Giappone", "CAN": "Canada"
        }

        g7 = df_wages[df_wages["ref_area"].isin(g7_codes)].copy()
        g7["paese"] = g7["ref_area"].map(g7_names)

        # Seleziona indicatori chiave
        indicators = g7["misura"].unique()
        selected = st.selectbox("Seleziona indicatore", options=indicators[:10])

        if selected:
            data = g7[g7["misura"] == selected]
            latest = data.sort_values("anno", ascending=False).drop_duplicates("ref_area")

            chart3 = alt.Chart(latest).mark_bar().encode(
                x=alt.X("valore:Q", title="Valore"),
                y=alt.Y("paese:N", title="Paese", sort="-x"),
                color=alt.condition(
                    alt.datum.ref_area == "ITA",
                    alt.value("#e63946"),
                    alt.value("#457b9d")
                ),
                tooltip=["paese", "anno", "valore"]
            ).properties(height=300)

            st.altair_chart(chart3, use_container_width=True)
    except Exception as e:
        st.warning(f"Errore: {e}")

    st.markdown("---")

    st.markdown("### Evoluzione cuneo fiscale Italia vs G7")

    try:
        # Trend per paese
        trend_countries = st.multiselect(
            "Paesi da confrontare",
            options=g7_codes,
            default=["ITA", "DEU", "FRA", "GBR"],
            key="tax_trend"
        )

        if trend_countries:
            # Prendi il primo indicatore disponibile per il trend
            trend_data = g7[
                (g7["ref_area"].isin(trend_countries)) &
                (g7["misura"] == selected)
            ].copy()
            trend_data["anno"] = trend_data["anno"].astype(int)

            chart4 = alt.Chart(trend_data).mark_line(point=True).encode(
                x=alt.X("anno:Q", title="Anno"),
                y=alt.Y("valore:Q", title="Valore"),
                color=alt.Color("paese:N", title="Paese"),
                tooltip=["anno", "paese", "valore"]
            ).properties(height=350)

            st.altair_chart(chart4, use_container_width=True)
    except Exception as e:
        st.warning(f"Errore: {e}")

st.caption("Fonte: OECD CTP.TPS · Tax Revenue + Taxing Wages")
