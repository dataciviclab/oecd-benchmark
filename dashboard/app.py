"""
OECD Data Explorer · Dashboard Streamlit
Benchmark internazionale: emissioni, PIL, salute, istruzione, lavoro, fisco.
"""

import streamlit as st
from lab_connectors.branding import apply_branding

st.set_page_config(
    page_title="OECD Data Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_branding()

pages = {
    "Panoramica": [
        st.Page("pages/01_Panoramica.py", title="Panoramica", icon="📊", default=True),
    ],
    "Dati per tema": [
        st.Page("pages/02_Emissioni.py", title="Emissioni GHG", icon="🏭"),
        st.Page("pages/03_Economia.py", title="PIL FUA", icon="💰"),
        st.Page("pages/04_Salute.py", title="Spesa Sanitaria", icon="🏥"),
        st.Page("pages/05_Istruzione.py", title="Istruzione", icon="🎓"),
        st.Page("pages/07_Disoccupazione.py", title="Disoccupazione", icon="👷"),
        st.Page("pages/08_Fisco.py", title="Fisco (Entrate + Cuneo)", icon="🏛️"),
    ],
    "Esplorazione": [
        st.Page("pages/06_SQL.py", title="Query SQL", icon="🧪"),
    ],
}

pg = st.navigation(pages, position="sidebar")

st.sidebar.markdown("---")
st.sidebar.caption("Dati: OECD SDMX API")
st.sidebar.caption(
    "Dataset: GHG, Economy, Health, Education, Unemployment, Tax"
)
st.sidebar.caption("[DataCivicLab](https://dataciviclab.org/) · CC BY 4.0")

pg.run()
