# Total Coffee - Playwright Automation Framework

A modular, Page-Object-Model, data-driven Playwright + pytest framework
that exercises the real, public storefront at **https://total.coffee/**
(a live WooCommerce site) plus its public WooCommerce Store API.

## Important: this targets a live production store

total.coffee is a real business, not a sandbox. This framework is
designed to never affect it: no test places a real order, submits a real
registration, or creates real spam data. See "Safety model" below.

## Structure

```
config/       environment JSON (dev/qa/stage/prod) + config.py loader
resources/    constants, environment helpers, marker names
pages/        Page Objects (one per page/flow) built on pages/base_page.py
components/   reusable page fragments (header, footer, popups, dialogs)
locators/     centralized CSS/selector constants per page
utilities/    excel/json/csv/yaml readers, logger, screenshots, waits, assertions,
              encryption, random data, misc helpers
fixtures/     pytest fixtures: browser/page, API client, optional DB session
api/          WooCommerce Store API client (wc/store/v1)
database/     optional DB-validation scaffolding (unused by default - see below)
testdata/     excel (primary)/json/csv/yaml data-driven inputs
tests/
  smoke/        fast, high-value checks
  regression/   full functional depth
  api/          Store API tests (no browser)
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
playwright install chromium
```

## Running tests

```bash
pytest                                   # everything
pytest -m smoke                          # smoke suite only
pytest -m "regression and cart"          # regression cart tests only
pytest -m api                            # API tests only (no browser)
pytest --env qa --browser-name chromium  # override environment/browser
pytest --headed-mode                     # watch the browser
```

Because tests run against a real, uncontrolled third-party server,
occasional network/timing flakiness is expected - `pytest.ini` reruns
each failing test up to twice (`--reruns 2 --reruns-delay 2`) before
reporting it as failed.

Reports land in `reports/html/report.html`, `reports/junit/results.xml`,
and `reports/allure-results/` (`allure serve reports/allure-results` to
view). Failure screenshots are saved to `screenshots/failures/`, and logs
to `logs/automation.log` / `logs/error.log`.

## Configuration

`ENV` selects `config/config_<env>.json` (dev/qa/stage/prod). Because
total.coffee is a single public production site, all four files point at
the same `base_url` today - the per-environment structure is kept so the
pattern is ready to point at real internal environments by editing the
relevant JSON file. Override individual values with env vars: `BASE_URL`,
`BROWSER`, `HEADLESS`, `TEST_USERNAME`, `TEST_PASSWORD`.

A handful of tests (my-account dashboard navigation, valid-login smoke
test) need a real customer account and are automatically skipped unless
`TEST_USERNAME`/`TEST_PASSWORD` (or `config.test_account`) are set - the
framework never creates one for you.

## Safety model (read before adding tests)

- **No real orders**: checkout tests fill/inspect the classic WooCommerce
  checkout form but never click `#place_order` with a fully valid
  payload. They only assert client-side validation behavior.
- **No real registrations**: registration tests only fill the email field
  with intentionally invalid formats to check HTML5 validation
  (`checkValidity()`); the register form is never submitted.
- **Cart mutations are safe**: adding/updating/removing cart line items
  only touches the anonymous session's cart (confirmed via the public
  `wc/store/v1/cart` API) - no inventory or order side effects.
- **`database/`** is scaffolded for framework completeness but unused by
  the shipped tests: this project has no real database credentials for a
  third-party hosted store. Point `DB_CONNECTION_STRING` at your own DB
  to use it against an internal environment.

## Data-driven testing

Excel (`testdata/excel/*.xlsx`, via `utilities/excel_reader.py`) is the
primary data source (login/product data). JSON, CSV, and YAML readers are
also wired up and used by other suites (search terms, cart quantities,
category navigation) so the framework demonstrates all four formats.

## CI/CD

`.github/workflows/regression.yml` runs the suite on push/PR/schedule.
`Dockerfile` + `docker-compose.yml` containerize it; `Jenkinsfile` gives
an equivalent Jenkins pipeline.
