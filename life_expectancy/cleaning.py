"""Cleaning script for the EU life expectancy data"""

import argparse
from pathlib import Path

import pandas as pd

from .loading import DATA_DIR, load_data, save_data


def clean_data(raw: pd.DataFrame, country: str = "PT") -> pd.DataFrame:
    """Return the rows of `country` from the raw EU data in long format"""
    first_col = raw.columns[0]
    raw = raw.copy()
    raw[["unit", "sex", "age", "region"]] = raw[first_col].str.split(",", expand=True)

    long = raw.drop(columns=first_col).melt(
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )

    long["year"] = long["year"].str.strip().astype(int)
    # Values may carry flags (e.g. "79.4 p"); keep only the numeric part
    long["value"] = long["value"].astype(str).str.extract(r"(\d+\.?\d*)", expand=False)
    long["value"] = long["value"].astype(float)
    long = long.dropna(subset=["value"])

    return long[long["region"] == country].reset_index(drop=True)


def main(
    country: str = "PT",
    input_path: Path = DATA_DIR / "eu_life_expectancy_raw.tsv",
    output_dir: Path = DATA_DIR,
) -> pd.DataFrame:
    """Load, clean and save the data, returning the cleaned DataFrame"""
    cleaned = clean_data(load_data(input_path), country)
    save_data(cleaned, output_dir / f"{country.lower()}_life_expectancy.csv")
    return cleaned


def parse_args(argv: list = None) -> argparse.Namespace:
    """Parse the command-line options"""
    parser = argparse.ArgumentParser(description="Clean the EU life expectancy data")
    parser.add_argument(
        "-c", "--country", default="PT", help="region code to keep (default: PT)"
    )
    return parser.parse_args(argv)


if __name__ == "__main__":  # pragma: no cover
    main(parse_args().country)
