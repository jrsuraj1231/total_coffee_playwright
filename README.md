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
pages/        Page Objects (one per page/flow), locators live as class
              constants on each page, built on pages/base_page.py
components/   reusable page fragments used across pages (header, popup)
utilities/    excel/json/csv/yaml readers, logger, screenshots, misc helpers
fixtures/     pytest fixtures: browser/page, API client
api/          WooCommerce Store API client (wc/store/v1)
testdata/     excel (primary)/json/csv/yaml data-driven inputs
tests/
  smoke/        fast, high-value checks
  regression/   full functional depth
  api/          Store API tests (no browser)
```

`reports/`, `screenshots/`, and `logs/` are created automatically the
first time you run the suite and are git-ignored.

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

## Data-driven testing

Excel (`testdata/excel/*.xlsx`, via `utilities/excel_reader.py`) is the
primary data source (login/product data). JSON, CSV, and YAML readers are
also wired up and used by other suites (search terms, cart quantities,
category navigation) so the framework demonstrates all four formats.

## CI/CD

`.github/workflows/regression.yml` runs the suite on push/PR/schedule.
