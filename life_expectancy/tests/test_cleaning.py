"""Tests for the cleaning module"""

import pandas as pd

from life_expectancy.cleaning import clean_data, parse_args
from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    clean_data()
    pt_life_expectancy_actual = pd.read_csv(OUTPUT_DIR / "pt_life_expectancy.csv")
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )


def test_clean_data_other_country():
    """Only rows of the requested country are saved"""
    output = OUTPUT_DIR / "fr_life_expectancy.csv"
    try:
        clean_data("FR")
        actual = pd.read_csv(output)
    finally:
        output.unlink(missing_ok=True)
    assert not actual.empty
    assert set(actual["region"]) == {"FR"}


def test_parse_args_default():
    """The country defaults to PT"""
    assert parse_args([]).country == "PT"


def test_parse_args_country():
    """The country can be set from the command line"""
    assert parse_args(["--country", "ES"]).country == "ES"
