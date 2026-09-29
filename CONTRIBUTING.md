# Contribuire a OECD Benchmark

Guida rapida per contribuire a questo repo.

## Aggiungere un nuovo dataset

1. Creare directory in `datasets/<nome-dataset>/`
2. Creare `dataset.yml` seguendo il pattern esistente
3. Creare SQL in `sql/`: `clean.sql`, `mart_italia.sql`, `mart_benchmark.sql`
4. Testare: `make run-<nome-dataset>`
5. Verificare contratti: `make test`

## Modifiche alla dashboard

1. Le pagine sono in `dashboard/pages/`
2. I dati vengono caricati da `dashboard/sources.py`
3. Testare localmente: `make dashboard`

## Regole

- Tutti i test devono passare prima del merge
- Usare `ruff` per il linting
- Scrivere commit message descrittivi

## Domande?

Aprire una GitHub Discussion nel repo principale DataCivicLab.
