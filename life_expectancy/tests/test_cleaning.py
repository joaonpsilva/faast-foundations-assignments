"""Tests for the cleaning module"""

import pandas as pd

from life_expectancy.cleaning import clean_data, main, parse_args
from life_expectancy.data_io import load_data, save_data
from . import OUTPUT_DIR


def test_main(pt_life_expectancy_expected):
    """Run the `main` function and compare the output to the expected output"""
    main()
    pt_life_expectancy_actual = pd.read_csv(OUTPUT_DIR / "pt_life_expectancy.csv")
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )


def test_main_other_country():
    """Only rows of the requested country are saved"""
    output = OUTPUT_DIR / "fr_life_expectancy.csv"
    try:
        main("FR")
        actual = pd.read_csv(output)
    finally:
        output.unlink(missing_ok=True)
    assert not actual.empty
    assert set(actual["region"]) == {"FR"}


def test_load_data():
    """The raw data is loaded with its combined first column"""
    raw = load_data()
    assert not raw.empty
    assert "," in raw.columns[0]


def test_clean_data(pt_life_expectancy_expected):
    """`clean_data` returns the long-format rows of the requested country"""
    cleaned = clean_data(load_data())
    pd.testing.assert_frame_equal(
        cleaned.reset_index(drop=True), pt_life_expectancy_expected
    )


def test_save_data(tmp_path, pt_life_expectancy_expected):
    """`save_data` writes the data as CSV without the index"""
    output = tmp_path / "output.csv"
    save_data(pt_life_expectancy_expected, output)
    pd.testing.assert_frame_equal(pd.read_csv(output), pt_life_expectancy_expected)


def test_parse_args_default():
    """The country defaults to PT"""
    assert parse_args([]).country == "PT"


def test_parse_args_country():
    """The country can be set from the command line"""
    assert parse_args(["--country", "ES"]).country == "ES"
