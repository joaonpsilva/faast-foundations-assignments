"""Tests for the region module"""

from life_expectancy.region import Region


def test_countries_excludes_aggregates():
    """Aggregated regions such as EU28 or EFTA are not countries"""
    countries = Region.countries()
    for aggregate in (
        "DE_TOT",
        "EA18",
        "EA19",
        "EEA30_2007",
        "EEA31",
        "EFTA",
        "EU27_2007",
        "EU27_2020",
        "EU28",
    ):
        assert Region(aggregate) not in countries


def test_countries_keeps_actual_countries():
    """Every non-aggregated region is returned, in definition order"""
    countries = Region.countries()
    assert len(countries) == len(Region) - 9
    assert Region.PT in countries
    assert all(isinstance(country, Region) for country in countries)
