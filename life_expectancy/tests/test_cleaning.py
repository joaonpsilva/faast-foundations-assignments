"""Tests for the cleaning module"""

from unittest.mock import patch

import pandas as pd

from life_expectancy.cleaning import clean_data, main, parse_args
from . import FIXTURES_DIR


def test_clean_data(eu_life_expectancy_raw, pt_life_expectancy_expected):
    """Cleaning the raw sample gives the expected PT output"""
    actual = clean_data(eu_life_expectancy_raw).reset_index(drop=True)
    pd.testing.assert_frame_equal(actual, pt_life_expectancy_expected)


def test_clean_data_other_country(eu_life_expectancy_raw, eu_life_expectancy_expected):
    """Only rows of the requested country are kept, flags are stripped"""
    actual = clean_data(eu_life_expectancy_raw, "FR").reset_index(drop=True)
    expected = eu_life_expectancy_expected[
        eu_life_expectancy_expected["region"] == "FR"
    ].reset_index(drop=True)
    pd.testing.assert_frame_equal(actual, expected)


def test_main(pt_life_expectancy_expected):
    """`main` returns the cleaned data and saves it without touching real files"""
    with patch("pandas.DataFrame.to_csv") as to_csv_mock:
        actual = main(
            input_path=FIXTURES_DIR / "eu_life_expectancy_raw.tsv",
            output_dir=FIXTURES_DIR,
        )
    to_csv_mock.assert_called_once()
    pd.testing.assert_frame_equal(
        actual.reset_index(drop=True), pt_life_expectancy_expected
    )


def test_parse_args_default():
    """The country defaults to PT"""
    assert parse_args([]).country == "PT"


def test_parse_args_country():
    """The country can be set from the command line"""
    assert parse_args(["--country", "ES"]).country == "ES"
