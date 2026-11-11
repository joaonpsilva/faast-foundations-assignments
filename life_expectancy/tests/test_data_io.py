"""Tests for the data_io module"""

from pathlib import Path
from unittest.mock import patch

import pandas as pd

from life_expectancy.data_io import load_data, save_data
from . import FIXTURES_DIR


def test_load_data(eu_life_expectancy_raw):
    """The raw sample is loaded as a DataFrame"""
    actual = load_data(FIXTURES_DIR / "eu_life_expectancy_raw.tsv")
    pd.testing.assert_frame_equal(actual, eu_life_expectancy_raw)


def test_save_data(pt_life_expectancy_expected):
    """`save_data` writes the CSV without the index"""
    with patch("pandas.DataFrame.to_csv") as to_csv_mock:
        save_data(pt_life_expectancy_expected, Path("out.csv"))
    to_csv_mock.assert_called_once_with(Path("out.csv"), index=False)
