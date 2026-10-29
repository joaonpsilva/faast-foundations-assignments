"""Cleaning script for the EU life expectancy data"""

import argparse

import pandas as pd

from life_expectancy.data_io import DATA_DIR, load_data, save_data

DEFAULT_COUNTRY = "PT"
ID_COLUMNS = ["unit", "sex", "age", "region"]
COMBINED_COLUMNS_SEPARATOR = ","
# A number optionally followed by flags (e.g. "79.4 p")
NUMERIC_PATTERN = r"(\d+\.?\d*)"


def _split_combined_column(raw: pd.DataFrame) -> pd.DataFrame:
    """Split the first column, which holds comma-separated ids, into `ID_COLUMNS`"""
    combined_column = raw.columns[0]
    split = raw.copy()
    split[ID_COLUMNS] = split[combined_column].str.split(
        COMBINED_COLUMNS_SEPARATOR, expand=True
    )
    return split.drop(columns=combined_column)


def _to_long_format(wide: pd.DataFrame) -> pd.DataFrame:
    """Turn the year columns into `year` and `value` rows"""
    return wide.melt(id_vars=ID_COLUMNS, var_name="year", value_name="value")


def _clean_types_and_values(long: pd.DataFrame) -> pd.DataFrame:
    """Convert years and values to numbers and drop rows without a value"""
    cleaned = long.copy()
    cleaned["year"] = cleaned["year"].str.strip().astype(int)
    # Values may carry flags (e.g. "79.4 p"); keep only the numeric part
    cleaned["value"] = (
        cleaned["value"]
        .astype(str)
        .str.extract(NUMERIC_PATTERN, expand=False)
        .astype(float)
    )
    return cleaned.dropna(subset=["value"])


def clean_data(raw: pd.DataFrame, country: str = DEFAULT_COUNTRY) -> pd.DataFrame:
    """Convert the raw EU data to long format, keeping only the rows of `country`"""
    long = _to_long_format(_split_combined_column(raw))
    cleaned = _clean_types_and_values(long)
    return cleaned[cleaned["region"] == country]


def parse_args(argv: list | None = None) -> argparse.Namespace:
    """Parse the command-line options"""
    parser = argparse.ArgumentParser(description="Clean the EU life expectancy data")
    parser.add_argument(
        "-c",
        "--country",
        default=DEFAULT_COUNTRY,
        help=f"region code to keep (default: {DEFAULT_COUNTRY})",
    )
    return parser.parse_args(argv)


def main(country: str = DEFAULT_COUNTRY) -> None:
    """Load the raw data, clean it for `country` and save the result as CSV"""
    raw = load_data()
    cleaned = clean_data(raw, country)
    save_data(cleaned, DATA_DIR / f"{country.lower()}_life_expectancy.csv")


if __name__ == "__main__":  # pragma: no cover
    main(parse_args().country)
