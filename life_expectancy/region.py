"""Regions available in the EU life expectancy data"""

from enum import Enum


class Region(Enum):
    """Region codes present in the EU life expectancy data"""

    AL = "AL"
    AM = "AM"
    AT = "AT"
    AZ = "AZ"
    BE = "BE"
    BG = "BG"
    BY = "BY"
    CH = "CH"
    CY = "CY"
    CZ = "CZ"
    DE = "DE"
    DE_TOT = "DE_TOT"
    DK = "DK"
    EA18 = "EA18"
    EA19 = "EA19"
    EE = "EE"
    EEA30_2007 = "EEA30_2007"
    EEA31 = "EEA31"
    EFTA = "EFTA"
    EL = "EL"
    ES = "ES"
    EU27_2007 = "EU27_2007"
    EU27_2020 = "EU27_2020"
    EU28 = "EU28"
    FI = "FI"
    FR = "FR"
    FX = "FX"
    GE = "GE"
    HR = "HR"
    HU = "HU"
    IE = "IE"
    IS = "IS"
    IT = "IT"
    LI = "LI"
    LT = "LT"
    LU = "LU"
    LV = "LV"
    MD = "MD"
    ME = "ME"
    MK = "MK"
    MT = "MT"
    NL = "NL"
    NO = "NO"
    PL = "PL"
    PT = "PT"
    RO = "RO"
    RS = "RS"
    RU = "RU"
    SE = "SE"
    SI = "SI"
    SK = "SK"
    SM = "SM"
    TR = "TR"
    UA = "UA"
    UK = "UK"
    XK = "XK"

    @classmethod
    def countries(cls) -> list["Region"]:
        """Return only the regions that are actual countries (no aggregates)"""
        return [region for region in cls if region not in _AGGREGATES]


# Groups of countries (e.g. EU28, EFTA) and Germany's DE_TOT (Germany incl. former GDR)
_AGGREGATES = frozenset(
    {
        Region.DE_TOT,
        Region.EA18,
        Region.EA19,
        Region.EEA30_2007,
        Region.EEA31,
        Region.EFTA,
        Region.EU27_2007,
        Region.EU27_2020,
        Region.EU28,
    }
)
