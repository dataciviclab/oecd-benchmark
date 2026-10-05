## Description

<!-- Descrizione breve delle modifiche -->

## Type of change

- [ ] Bug fix
- [ ] Nuovo dataset
- [ ] Espansione dataset (aggiunta paesi/anni/indicatori)
- [ ] Aggiornamento dashboard
- [ ] Pipeline / CI
- [ ] Documentazione
- [ ] Altro

## Checklist

### Dataset
- [ ] `dataset.yml` valido (schema_version, raw, clean, mart, validation)
- [ ] SQL file esistenti (clean.sql, mart_italia.sql, mart_benchmark.sql)
- [ ] required_columns e required_tables dichiarati
- [ ] min_rows > 0 in validazione
- [ ] `make check` passa

### Codice
- [ ] Test passano localmente (`make test`)
- [ ] Linter passa (`make lint`)
- [ ] Nessun file dati committato (out/ è gitignorato)

### Dashboard
- [ ] Pagine funzionanti (`make dashboard`)
- [ ] Dati caricati correttamente

### Documentazione
- [ ] README aggiornato (se nuovo dataset)
- [ ] CONTRIBUTING seguito
