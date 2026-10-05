"""Contract tests per i dataset OECD.

Verifica che ogni dataset.yml sia valido, che gli schema contrattati
esistano e che i campi obbligatori siano presenti.
"""

from __future__ import annotations

import pathlib

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATASETS_DIR = ROOT / "datasets"


def _load_dataset_yml(path: pathlib.Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def _all_dataset_ymls() -> list[tuple[str, pathlib.Path]]:
    results = []
    for d in sorted(DATASETS_DIR.iterdir()):
        yml = d / "dataset.yml"
        if yml.exists():
            results.append((d.name, yml))
    return results


DATASET_YMLS = _all_dataset_ymls()
IDS = [name for name, _ in DATASET_YMLS]


# -- Contract: dataset.yml structure --

@pytest.mark.contract
class TestDatasetYmlContract:
    """Ogni dataset.yml deve avere la struttura minima richiesta."""

    @pytest.fixture(params=DATASET_YMLS, ids=IDS)
    def dataset_entry(self, request):
        name, path = request.param
        data = _load_dataset_yml(path)
        return name, path, data

    def test_schema_version(self, dataset_entry):
        name, path, data = dataset_entry
        assert "schema_version" in data, f"{name}: manca schema_version"

    def test_dataset_section(self, dataset_entry):
        name, path, data = dataset_entry
        assert "dataset" in data, f"{name}: manca sezione dataset"
        ds = data["dataset"]
        for field in ("name", "years", "tags", "category"):
            assert field in ds, f"{name}: dataset manca campo '{field}'"

    def test_raw_section(self, dataset_entry):
        name, path, data = dataset_entry
        assert "raw" in data, f"{name}: manca sezione raw"
        raw = data["raw"]
        assert "sources" in raw, f"{name}: raw manca 'sources'"
        assert len(raw["sources"]) > 0, f"{name}: raw.sources vuoto"
        for src in raw["sources"]:
            assert "name" in src, f"{name}: source manca 'name'"
            assert "type" in src, f"{name}: source manca 'type'"

    def test_clean_section(self, dataset_entry):
        name, path, data = dataset_entry
        assert "clean" in data, f"{name}: manca sezione clean"
        clean = data["clean"]
        assert "sql" in clean, f"{name}: clean manca 'sql'"
        sql_path = path.parent / clean["sql"]
        assert sql_path.exists(), f"{name}: SQL file non trovato: {clean['sql']}"

    def test_mart_section(self, dataset_entry):
        name, path, data = dataset_entry
        if "mart" not in data:
            pytest.skip(f"{name}: nessun mart dichiarato")
        mart = data["mart"]
        assert "tables" in mart, f"{name}: mart manca 'tables'"
        for table in mart["tables"]:
            assert "name" in table, f"{name}: mart table manca 'name'"
            assert "sql" in table, f"{name}: mart table manca 'sql'"
            sql_path = path.parent / table["sql"]
            assert sql_path.exists(), f"{name}: mart SQL non trovato: {table['sql']}"

    def test_validation_section(self, dataset_entry):
        name, path, data = dataset_entry
        assert "validation" in data, f"{name}: manca sezione validation"
        val = data["validation"]
        assert "fail_on_error" in val, f"{name}: validation manca 'fail_on_error'"


# -- Contract: required columns --

@pytest.mark.contract
class TestRequiredColumns:
    """required_columns in clean e required_tables in mart devono essere dichiarati."""

    @pytest.fixture(params=DATASET_YMLS, ids=IDS)
    def dataset_entry(self, request):
        name, path = request.param
        data = _load_dataset_yml(path)
        return name, path, data

    def test_clean_required_columns(self, dataset_entry):
        name, path, data = dataset_entry
        clean = data.get("clean", {})
        rc = clean.get("required_columns", [])
        assert len(rc) > 0, f"{name}: clean.required_columns vuoto"

    def test_mart_required_tables(self, dataset_entry):
        name, path, data = dataset_entry
        mart = data.get("mart", {})
        rt = mart.get("required_tables", [])
        assert len(rt) > 0, f"{name}: mart.required_tables vuoto"
        table_names = {t["name"] for t in mart.get("tables", [])}
        for t in rt:
            assert t in table_names, f"{name}: required_table '{t}' non in mart.tables"


# -- Contract: primary key e min_rows --

@pytest.mark.contract
class TestValidationRules:
    """Ogni dataset deve avere primary_key e min_rows nella validazione."""

    @pytest.fixture(params=DATASET_YMLS, ids=IDS)
    def dataset_entry(self, request):
        name, path = request.param
        data = _load_dataset_yml(path)
        return name, path, data

    def test_clean_has_min_rows(self, dataset_entry):
        name, path, data = dataset_entry
        validate = data.get("clean", {}).get("validate", {})
        assert "min_rows" in validate, f"{name}: clean.validate manca min_rows"
        assert validate["min_rows"] > 0, f"{name}: min_rows deve essere > 0"

    def test_mart_table_rules(self, dataset_entry):
        name, path, data = dataset_entry
        mart = data.get("mart", {})
        validate = mart.get("validate", {})
        table_rules = validate.get("table_rules", {})
        for table in mart.get("tables", []):
            tname = table["name"]
            assert tname in table_rules, f"{name}: mart manca table_rules per '{tname}'"


# -- Contract: semantic filters (tax revenue) --

@pytest.mark.contract
class TestTaxRevenueSemanticFilters:
    """I mart SQL di tax revenue devono filtrare T_SPLIT + PT_B1GQ."""

    def test_mart_italia_filters(self):
        sql_path = DATASETS_DIR / "oecd-tax-revenue" / "sql" / "mart_italia.sql"
        sql = sql_path.read_text()
        assert "T_SPLIT" in sql, "mart_italia.sql: manca filtro revenue_category = 'T_SPLIT'"
        assert "PT_B1GQ" in sql, "mart_italia.sql: manca filtro unita = 'PT_B1GQ'"

    def test_mart_benchmark_filters(self):
        sql_path = DATASETS_DIR / "oecd-tax-revenue" / "sql" / "mart_benchmark.sql"
        sql = sql_path.read_text()
        assert "T_SPLIT" in sql, "mart_benchmark.sql: manca filtro revenue_category = 'T_SPLIT'"
        assert "PT_B1GQ" in sql, "mart_benchmark.sql: manca filtro unita = 'PT_B1GQ'"

    def test_clean_has_revenue_category(self):
        yml_path = DATASETS_DIR / "oecd-tax-revenue" / "dataset.yml"
        data = _load_dataset_yml(yml_path)
        rc = data.get("clean", {}).get("required_columns", [])
        assert "revenue_category" in rc, "clean.required_columns: manca revenue_category"
