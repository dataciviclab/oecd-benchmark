"""Fonti dati per la dashboard OECD Benchmark."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
from lab_connectors.duckdb.queries import load_mart_table, query_clean
from lab_connectors.registry import load_registry

_registry = load_registry(Path(__file__).parent.parent / "registry" / "registry.json")
PREFIX = "oecd-benchmark/"

DATASETS = {
    "ghg": "oecd_fua_ghg",
    "economy": "oecd_fua_economy",
    "health": "oecd_health_expenditure",
    "gdp": "oecd_regional_gdp",
    "education": "oecd_education_attainment",
    "unemployment": "oecd_unemployment",
    "tax_revenue": "oecd_tax_revenue",
    "taxing_wages": "oecd_taxing_wages",
}


def _slug(alias: str) -> str:
    return DATASETS.get(alias, alias)


@st.cache_data(ttl=300, show_spinner=False)
def load_mart(slug: str, table: str, year: int = 2026) -> pd.DataFrame:
    return load_mart_table(_slug(slug), table, year, prefix=PREFIX)


@st.cache_data(ttl=300, show_spinner=False)
def query(slug: str, sql: str, years: list[int] | None = None) -> pd.DataFrame:
    return query_clean(_slug(slug), sql, years or [2026], prefix=PREFIX)


