"""SQL — Query interattiva sui dati OECD.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lab_connectors.duckdb.sql_page import render_sql_query
from sources import PREFIX, _registry

render_sql_query(
    registry=_registry,
    years=[2026],
    prefix=PREFIX,
    title="🧪 Query SQL",
    description=(
        "Scrivi query SQL sui dataset OECD. "
        "Usa ``clean_input`` come nome della tabella virtuale."
    ),
)
