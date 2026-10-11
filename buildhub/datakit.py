"""datakit — a tiny data-processing toolkit.

YOUR JOB: implement every function below so it matches SPEC.md. Drive Claude Code
to help, but you must understand and be able to explain each line. Run the public
tests as you go:  pytest tests/public
"""
from __future__ import annotations

import csv
import json


def load_records(path):
    """Load a .csv or .json file into a list of dict rows.

    - .csv  -> use csv.DictReader (every value is a str)
    - .json -> a list of objects (returned as-is)
    - anything else -> raise ValueError
    """
    if path.endswith(".csv"):
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    elif path.endswith(".json"):
        with open(path) as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported file type: {path}")


def filter_records(records, **criteria):
    """Return only the rows where, for every field=value pair passed as a keyword
    argument, str(row[field]) == str(value)."""
    return [
        row
        for row in records
        if all(str(row[field]) == str(value) for field, value in criteria.items())
    ]


def summarize(records, group_by, value, agg, decimals=2):
    """Group rows by the `group_by` field and aggregate the numeric `value` field.

    agg is one of:
      "count" -> number of rows in the group (int)
      "sum"   -> sum of the values (float)
      "mean"  -> mean of the values, rounded to `decimals` places (float)
      "min"   -> smallest value (float)
      "max"   -> largest value (float)
    Return a dict mapping each group value to its aggregate. Unknown agg -> ValueError.
    """
    groups: dict = {}
    for row in records:
        groups.setdefault(row[group_by], []).append(float(row[value]))

    if agg == "count":
        return {key: len(vals) for key, vals in groups.items()}
    elif agg == "sum":
        return {key: sum(vals) for key, vals in groups.items()}
    elif agg == "mean":
        return {key: round(sum(vals) / len(vals), decimals) for key, vals in groups.items()}
    elif agg == "min":
        return {key: min(vals) for key, vals in groups.items()}
    elif agg == "max":
        return {key: max(vals) for key, vals in groups.items()}
    else:
        raise ValueError(f"Unknown agg: {agg}")


def top_n(records, key, n):
    """Return the `n` rows with the largest numeric `key`, sorted descending."""
    raise NotImplementedError


def to_report(summary):
    """Render a {key: value} dict as lines 'key: value', one per line, sorted
    ascending by key, joined with '\\n' (no trailing newline)."""
    raise NotImplementedError
