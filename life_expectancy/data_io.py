"""Functions to read and write the EU life expectancy data"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
RAW_DATA_FILE = DATA_DIR / "eu_life_expectancy_raw.tsv"
RAW_DATA_SEPARATOR = "\t"


def load_data(file_path: Path = RAW_DATA_FILE) -> pd.DataFrame:
    """Load the raw EU life expectancy data from a TSV file"""
    return pd.read_csv(file_path, sep=RAW_DATA_SEPARATOR)


def save_data(data: pd.DataFrame, file_path: Path) -> None:
    """Save the data as CSV, without the index"""
    data.to_csv(file_path, index=False)
