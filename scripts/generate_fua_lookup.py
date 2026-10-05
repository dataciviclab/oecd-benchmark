#!/usr/bin/env python3
"""Genera fua_lookup.csv dall'API OECD SDMX.

Fonte: OECD.CFE.EDS/DSD_FUA_TERR@DF_DENSITY
Output: datasets/support/fua_lookup.csv
"""

import csv
import io
import sys
from pathlib import Path

import requests

OUTPUT = Path(__file__).parent.parent / "datasets" / "support" / "fua_lookup.csv"

URL = (
    "https://sdmx.oecd.org/public/rest/data/"
    "OECD.CFE.EDS,DSD_FUA_TERR@DF_DENSITY,1.0/"
    "?startPeriod=2022&endPeriod=2022"
    "&format=csvfilewithlabels"
    "&dimensionAtObservation=AllDimensions"
)


def fetch_fua_data() -> str:
    """Scarica dati FUA dall'API OECD."""
    print("Fetching FUA data from OECD...")
    r = requests.get(URL, timeout=60)
    r.raise_for_status()
    return r.text


def parse_fua_csv(csv_text: str) -> list[dict]:
    """Estrae codici FUA italiani con nomi."""
    reader = csv.reader(io.StringIO(csv_text))
    header = next(reader)

    ref_idx = header.index("REF_AREA")
    ref_label_idx = header.index("Reference area")

    fua_data = {}
    for row in reader:
        if len(row) > ref_label_idx:
            code = row[ref_idx]
            name = row[ref_label_idx]
            if code.startswith("IT"):
                # Solo FUA (F), non City (C)
                if code.endswith("F"):
                    fua_data[code] = name

    return fua_data


def write_lookup(fua_data: dict[str, str]) -> None:
    """Scrive il file CSV di lookup."""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fua_code", "fua_nome", "paese", "regione"])
        for code in sorted(fua_data.keys()):
            writer.writerow([code, fua_data[code], "Italia", ""])

    print(f"Written {len(fua_data)} FUA to {OUTPUT}")


def main() -> int:
    try:
        csv_text = fetch_fua_data()
        fua_data = parse_fua_csv(csv_text)
        write_lookup(fua_data)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
