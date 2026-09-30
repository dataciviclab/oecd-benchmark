"""
Istruzione — Livello istruzione popolazione italiana.
"""

import sys
from pathlib import Path

import altair as alt
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from lab_connectors.formatters import fmt_pct
from sources import load_mart

st.title("🎓 Istruzione")
st.markdown("Livello di istruzione della popolazione italiana confrontato con regioni OCSE.")

# --- Filtri ---
col1, col2 = st.columns(2)
with col1:
    anno = st.slider("Anno", min_value=2000, max_value=2023, value=2022)
with col2:
    eta = st.selectbox("Fascia d'età", ["Y25T64", "Y25T34"], format_func=lambda x: "25-64 anni" if x == "Y25T64" else "25-34 anni")

# --- Regioni italiane ---
st.markdown(f"### Regioni italiane — Istruzione terziaria ({anno})")

try:
    df = load_mart("education", "mart_italia")
    regions = df[
        (df["anno"] == anno) &
        (df["eta"] == eta) &
        (df["sesso"] == "_T")
    ].sort_values("valore", ascending=True)

    regions["livello"] = regions["valore"].apply(lambda x: "Alto (≥22%)" if x >= 22 else "Basso (<22%)")

    chart = alt.Chart(regions).mark_bar().encode(
        x=alt.X("valore:Q", title="% popolazione"),
        y=alt.Y("paese:N", title="Regione", sort="-x"),
        color=alt.Color("livello:N", title="Livello", scale=alt.Scale(domain=["Alto (≥22%)", "Basso (<22%)"], range=["#2a9d8f", "#e76f51"])),
        tooltip=["paese", "valore"]
    ).properties(height=500)

    # Linea media
    mean_line = alt.Chart({"values": [{"x": regions["valore"].mean()}]}).mark_rule(
        color="black", strokeDash=[4, 4]
    ).encode(x="x:Q")

    st.altair_chart(chart + mean_line, use_container_width=True)

    # Statistiche
    col1, col2, col3 = st.columns(3)
    col1.metric("Media nazionale", fmt_pct(regions["valore"].mean()))
    col2.metric("Migliore", f"{regions.iloc[-1]['paese']} ({fmt_pct(regions.iloc[-1]['valore'])})")
    col3.metric("Peggiore", f"{regions.iloc[0]['paese']} ({fmt_pct(regions.iloc[0]['valore'])})")
except Exception as e:
    st.warning(f"Errore: {e}")

st.markdown("---")

# --- Gap Nord-Sud ---
st.markdown("### Disuguaglianza Nord-Sud")

nord = ["Lombardy", "Piedmont", "Veneto", "Emilia-Romagna", "Liguria", "Tuscany", "Friuli-Venezia Giulia"]
sud = ["Campania", "Calabria", "Apulia", "Sicily", "Sardinia", "Basilicata", "Molise", "Abruzzo"]

try:
    regions_list = regions["paese"].tolist()
    nord_vals = regions[regions["paese"].isin(nord)]["valore"]
    sud_vals = regions[regions["paese"].isin(sud)]["valore"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Nord Italia", fmt_pct(nord_vals.mean()) if len(nord_vals) > 0 else "N/D")
    col2.metric("Sud Italia", fmt_pct(sud_vals.mean()) if len(sud_vals) > 0 else "N/D")
    col3.metric("Gap", f"{(nord_vals.mean() - sud_vals.mean()):.1f} pp" if len(nord_vals) > 0 and len(sud_vals) > 0 else "N/D")
except Exception as e:
    st.warning(f"Errore nel calcolo gap: {e}")

st.markdown("---")

# --- Evoluzione temporale ---
st.markdown("### Evoluzione istruzione terziaria (Italia)")

try:
    trend = df[
        (df["ref_area"].str.startswith("IT")) &
        (df["eta"] == "Y25T64") &
        (df["sesso"] == "_T")
    ].groupby("anno")["valore"].mean().reset_index()

    chart2 = alt.Chart(trend).mark_line(point=True).encode(
        x=alt.X("anno:Q", title="Anno"),
        y=alt.Y("valore:Q", title="% popolazione", scale=alt.Scale(domain=[8, 24])),
        tooltip=["anno", "valore"]
    ).properties(height=300)

    st.altair_chart(chart2, use_container_width=True)
except Exception as e:
    st.warning(f"Errore: {e}")

# --- Confronto con selected regions OCSE ---
st.markdown("---")
st.markdown("### Confronto con regioni OCSE selezionate")

selected_regions = st.multiselect(
    "Seleziona regioni da confrontare",
    options=["District of Columbia", "Greater London", "Stockholm", "Capital Region (KR)", "Ontario", "Massachusetts"],
    default=["Greater London", "Stockholm", "Ontario"]
)

if selected_regions:
    try:
        # Query diretta sui dati clean per regioni OCSE
        from sources import query as _query
        regions_str = ", ".join([f"'{r}'" for r in selected_regions + ["Lazio", "Lombardy"]])
        ocse = _query("education", f"""
            SELECT paese, valore
            FROM clean_input
            WHERE anno = {anno}
              AND eta = '{eta}'
              AND sesso = '_T'
              AND paese IN ({regions_str})
        """)

        ocse["gruppo"] = ocse["paese"].apply(lambda x: "Italia" if x in ["Lazio", "Lombardy"] else "OCSE")

        chart3 = alt.Chart(ocse).mark_bar().encode(
            x=alt.X("valore:Q", title="% terziaria"),
            y=alt.Y("paese:N", title="Regione", sort="-x"),
            color=alt.Color("gruppo:N", title="Gruppo", scale=alt.Scale(domain=["Italia", "OCSE"], range=["#e63946", "#457b9d"])),
            tooltip=["paese", "valore"]
        ).properties(height=250)

        st.altair_chart(chart3, use_container_width=True)
    except Exception as e:
        st.warning(f"Errore: {e}")

st.caption("Fonte: OECD CFE.EDS · Education Attainment")
