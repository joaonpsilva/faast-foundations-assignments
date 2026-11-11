"""Loading and saving of the EU life expectancy data"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def load_data(path: Path = DATA_DIR / "eu_life_expectancy_raw.tsv") -> pd.DataFrame:
    """Load the raw tab-separated EU data"""
    return pd.read_csv(path, sep="\t")


def save_data(data: pd.DataFrame, path: Path) -> None:
    """Save the data as CSV without the index"""
    data.to_csv(path, index=False)
