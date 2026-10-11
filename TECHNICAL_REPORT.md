# Technical Report — Build Hub (`buildhub`)

**Author:** Ray Bednara
**Course:** INF601 — Advanced Programming in Python
**Project:** Mini Project 4, Track B

## 1. Overview

`buildhub` is a small data-processing toolkit implemented against a fixed
specification (`SPEC.md`). It loads tabular data from `.csv` or `.json`
files and provides filtering, grouped aggregation, top-N ranking, and
report rendering, plus a command-line interface over the aggregation and
ranking functions.

## 2. Design Decisions

**`load_records(path)`** dispatches purely on the file's suffix
(`path.endswith(".csv")` / `.endswith(".json")`), rather than inspecting
file contents or using a library like `pathlib` for the extension check.
CSV rows come back as `str`-only dicts via `csv.DictReader`, matching how
that reader works; JSON is parsed and returned as-is, keeping its native
types (numbers stay numbers). Anything else raises `ValueError`.

**`filter_records(records, **criteria)`** compares with
`str(row[field]) == str(value)` on *both* sides rather than a direct `==`.
This was a deliberate choice to make filtering type-tolerant: a CSV-sourced
row always holds strings, but a caller might reasonably pass an `int`
(`filter_records(rows, points=10)`). Coercing both sides to `str` makes the
function work the same way regardless of where the data came from. With no
keyword arguments, `all()` over an empty generator is vacuously `True`, so
every row passes through — matching the spec's "with no criteria, return
all rows."

**`summarize(records, group_by, value, agg, decimals=2)`** converts every
grouped value to `float` immediately when building the groups, before any
aggregation runs. This was the same reasoning as above: CSV values arrive
as strings, JSON values may already be numeric, and converting once up
front means the five aggregation branches (`count`/`sum`/`mean`/`min`/`max`)
don't each need their own type handling. `count` is the one branch that
returns `len(vals)` (an `int`) rather than a float, since the spec requires
an `int` there specifically. Unknown `agg` values fall through to an
explicit `else: raise ValueError(...)`.

**`top_n(records, key, n)`** uses `sorted(records, key=lambda row:
float(row[key]), reverse=True)[:n]`. Sorting alone only produces the full
list in descending order; `[:n]` is the step that actually satisfies "the
`n` rows" — without it the function would silently ignore `n` and return
everything. `sorted()` (rather than `list.sort()`) was used specifically
because it returns a new list, leaving the caller's original `records`
list untouched.

**`to_report(summary)`** relies on `sorted(summary.items())`, which sorts a
list of `(key, value)` tuples by the first element by default — i.e. by
key, ascending, exactly as the spec requires — then formats each pair with
an f-string and joins with `"\n"`. Using `"\n".join(...)` rather than
building the string with a trailing newline per line was intentional, since
it naturally avoids a trailing newline after the last entry.

**CLI (`buildhub/__main__.py`)** uses `argparse` with two subparsers
(`summarize`, `top`), matching the spec exactly — there is no `filter`
subcommand, since `SPEC.md` only defines CLI access to `summarize` and
`top`; `filter_records` remains a library-only function. The `summarize`
subcommand's `--decimals` flag was added after cross-checking the CLI usage
example in `SPEC.md` (`--agg mean --decimals 2`), which the first draft of
the CLI didn't include. `from .datakit import ...` is a relative import,
which only resolves correctly when the module is run as part of the
`buildhub` package (i.e. via `python -m buildhub`, not by running
`__main__.py` as a standalone script).

## 3. What the Agent Did vs. What I Did

I drove the work function-by-function: for each of the five functions in
`datakit.py`, I asked Claude Code to implement just that one function, then
reviewed the diff and the explanation of what each line did before
approving and moving to the next. Claude Code wrote the implementations,
ran the relevant `pytest` cases after each change to confirm it passed, and
explained the reasoning (e.g. why `str()`/`float()` coercion is needed, why
`top_n` needs a slice after sorting, the difference between `sorted()` and
`list.sort()`). I supplied the actual `SPEC.md` partway through the session
(after the CLI had already been built from the in-file docstrings alone),
which surfaced the missing `--decimals` flag — that gap, and the fix, came
from comparing the existing implementation against the real spec rather
than from me independently noticing it.

## 4. Testing

* All 7 tests in `tests/public/test_smoke.py` pass (`pytest tests/public`):
  CSV/JSON loading, filtering, `sum`/`count` summaries, `top_n`, and
  `to_report`.
* The CLI was manually verified against `SPEC.md`'s own inline examples,
  including `summarize(..., "mean", decimals=1)` → `{"red": 31.7, "blue":
  32.5}` and the `--decimals 2` CLI example, both of which matched exactly.
* `python -m buildhub top fixtures/sample.csv --key points --n 3` was
  checked against the expected descending order of the sample data.

## 5. Limitations

* The public test suite only covers `sum` and `count` for `summarize`;
  `mean`/`min`/`max` were checked manually against `SPEC.md`'s examples
  rather than by an automated test in this repo.
* Neither `filter_records` nor `summarize`/`top_n` validate that the
  requested field actually exists on every row — a missing key raises a
  plain `KeyError` rather than a more descriptive error, since the spec
  doesn't call for special handling there.
* The hidden autograder varies parameters (e.g. `decimals`, `n`) using a
  per-student `BUILD_SEED` (mine is `130`); since the seed-to-parameter
  mapping isn't public, the implementation was built to be general
  (reading all parameters rather than hard-coding values from the public
  tests) instead of being verified against the grader's exact inputs.
