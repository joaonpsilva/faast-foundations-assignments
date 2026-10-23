"""Cleaning script for the EU life expectancy data"""

import argparse
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def clean_data(country: str = "PT") -> None:
    """Load the raw EU data, keep the rows of `country` in long format and save them as CSV"""
    raw = pd.read_csv(DATA_DIR / "eu_life_expectancy_raw.tsv", sep="\t")

    first_col = raw.columns[0]
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

    country_data = long[long["region"] == country]
    country_data.to_csv(
        DATA_DIR / f"{country.lower()}_life_expectancy.csv", index=False
    )


def parse_args(argv: list = None) -> argparse.Namespace:
    """Parse the command-line options"""
    parser = argparse.ArgumentParser(description="Clean the EU life expectancy data")
    parser.add_argument(
        "-c", "--country", default="PT", help="region code to keep (default: PT)"
    )
    return parser.parse_args(argv)


if __name__ == "__main__":  # pragma: no cover
    clean_data(parse_args().country)
