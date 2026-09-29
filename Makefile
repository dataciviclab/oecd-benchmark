# DataCivicLab — OECD Benchmark
# Standard interface: make lint test check run clean
# CLI toolkit del Lab. La memoria DuckDB è controllata da safe_connect
# (lab-connectors) via env DUCKDB_MEMORY_LIMIT (default 2GB).

TOOLKIT = toolkit
PYTHON  = python3

YEAR_START ?= 2000
YEAR_END   ?= 2025
YEARS       = $(shell seq $(YEAR_START) $(YEAR_END))
YEARS_COMMA = $(shell echo $(YEARS) | tr ' ' ',')

# --- Dataset discovery ------------------------------------------------------
DATASETS := $(shell find datasets -name dataset.yml 2>/dev/null | sort)

# --- Standard interface (ADR-001, workflows.md) ------------------------------

.PHONY: lint
lint:
	ruff check .

.PHONY: test
test:
	python -m pytest tests/ -v

.PHONY: check
check:
	@for f in $(DATASETS); do \
		echo "→ $$f"; \
		$(TOOLKIT) run preflight --config "$$f" > /dev/null 2>&1 || exit 1; \
	done
	@echo "✅ All configs valid"

.PHONY: run
run:
	@for f in $(DATASETS); do \
		echo "=== $$f ==="; \
		$(TOOLKIT) run --config "$$f" --years $(YEARS_COMMA) || exit 1; \
	done

.PHONY: run-batch
run-batch:
	@if [ -s batch.txt ]; then \
		$(TOOLKIT) run --batch batch.txt --years $(YEARS_COMMA); \
	else \
		echo "Nessun dataset da processare"; \
	fi

.PHONY: run-%
run-%:
	$(TOOLKIT) run --config datasets/$*/dataset.yml --years $(YEARS_COMMA)

.PHONY: pipeline
pipeline: test run
	@echo "✅ Pipeline complete"

# --- Status / diagnostics ----------------------------------------------------

.PHONY: status
status:
	@echo "=== Pipeline Status ==="
	@for ds in datasets/*/; do \
		name=$$(basename "$$ds"); \
		last_run=$$(ls -t out/data/_runs/$$name/*/ 2>/dev/null | head -1); \
		if [ -n "$$last_run" ]; then \
			status=$$(cat "out/data/_runs/$$name/$$last_run"/*.json 2>/dev/null | $(PYTHON) -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null || echo "?"); \
			echo "  $$name: $$status"; \
		else \
			echo "  $$name: no runs"; \
		fi \
	done

# --- Registry ---------------------------------------------------------------

.PHONY: registry registry-write
registry:
	$(TOOLKIT) registry build --prefix oecd-benchmark

registry-write:
	$(TOOLKIT) registry build --prefix oecd-benchmark --write

# --- Cleanup ----------------------------------------------------------------

.PHONY: clean
clean:
	rm -rf out/data/_runs out/data/probe out/data/raw out/data/clean out/data/mart .tmp/

.PHONY: clean-runs
clean-runs:
	rm -rf out/data/_runs/

# --- Dashboard ---------------------------------------------------------------

.PHONY: dashboard
dashboard:
	streamlit run dashboard/app.py

# --- Help -------------------------------------------------------------------

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
