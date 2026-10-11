### INF601 - Advanced Programming in Python
### Ray Bednara
### Mini Project 4


# Build Hub — Data Processing Toolkit

A small CSV/JSON data-processing toolkit (`buildhub`) built against a fixed
spec, plus a command-line interface for summarizing and ranking records.

## Description

This project implements `buildhub/datakit.py`, a toolkit of five functions
for working with tabular records loaded from either a `.csv` or `.json` file:

* `load_records(path)` — loads a `.csv` (via `csv.DictReader`) or `.json` file
  into a list of dict rows; raises `ValueError` for any other extension.
* `filter_records(records, **criteria)` — returns only the rows matching every
  `field=value` keyword argument given.
* `summarize(records, group_by, value, agg, decimals=2)` — groups rows by a
  field and aggregates a numeric field across each group (`count`, `sum`,
  `mean`, `min`, or `max`).
* `top_n(records, key, n)` — returns the `n` rows with the largest numeric
  `key`, sorted descending.
* `to_report(summary)` — renders a `{key: value}` dict as sorted `key: value`
  text lines.

`buildhub/__main__.py` wraps `summarize` and `top_n` in a small `argparse`
CLI so the toolkit can be run directly from the command line against any
`.csv` or `.json` file.

## Getting Started

### Dependencies

* Windows 10/11
* Python 3.13
* No internet connection required — the toolkit itself uses only the Python
  standard library (`csv`, `json`); `pytest` is used only to run the tests
* Install required libraries with:
```
pip install -r requirements.txt
```

### Installing

* Clone or download this repository
* No file/folder modifications are needed; sample data lives in `fixtures/`

### Executing program

* Run the public test suite from the project root:
```
pytest tests/public
```
* Or run the CLI directly against the sample data:
```
python -m buildhub summarize fixtures/sample.csv --group-by team --value points --agg mean --decimals 2
python -m buildhub top fixtures/sample.csv --key points --n 3
```
* The CLI will:
    * Load the given `.csv` or `.json` file into records
    * `summarize` → group and aggregate a field, then print the report text
    * `top` → print the `n` highest-ranked rows, one per line

## Help

`filter_records` compares with `str(row[field]) == str(value)` on both sides
so a filter like `filter_records(rows, points=10)` (an `int`) still matches a
CSV row where every value was read in as a `str`.

`summarize` converts each value to `float` before aggregating, for the same
reason — CSV rows arrive as strings, but JSON rows may already be numeric, so
coercing to `float` up front lets both sources be aggregated the same way.

## Authors

Ray Bednara
ray.bednara@gmail.com

## AI Usage

I used Claude Code to implement all five functions in `datakit.py` one at a
time, checking and understanding each one (and running the relevant `pytest`
cases) before moving to the next, then to build the `argparse` CLI in
`__main__.py` against `SPEC.md`. I asked it to explain tricky points along
the way — why `top_n` needs to slice after sorting, what `sorted()` is and how
it differs from `list.sort()`, and why values are coerced with `str()`/`float()`
before comparing or aggregating.
