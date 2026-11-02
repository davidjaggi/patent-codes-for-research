import re

import pytest

import patentcodes as pc

CODE = re.compile(r"^[A-HY]\d{2}[A-Z]?\d*(/\d+)?$")


def test_expand_short_ranges():
    assert pc.expand_code("F02M39-41") == ["F02M39", "F02M40", "F02M41"]
    assert pc.expand_code("B01D53/34-36") == ["B01D53/34", "B01D53/35", "B01D53/36"]
    assert pc.expand_code("Y02T10/72-7291") == ["Y02T10/72-7291"]  # never expand long ranges
    with pytest.raises(ValueError):
        pc.expand_code("F02M71-39")


def test_covers():
    assert pc.covers("Y02B", "Y02B90/10")
    assert pc.covers("Y02E30", "Y02E30/10")
    assert not pc.covers("B60L3", "B60L30/00")  # group 3 is not group 30
    assert pc.covers("Y02E10/70", "Y02E10/70")
    assert not pc.covers("Y02E10/70", "Y02E10/721")  # exact subgroup unless a range is given
    assert pc.covers("F22", "F22B1/00")
    assert pc.covers("Y02T10/72", "Y02T10/7258", code_to="Y02T10/7291")
    assert not pc.covers("Y02T10/72", "Y02T10/7300", code_to="Y02T10/7291")


@pytest.mark.parametrize("scheme", ["envtech", "jee_srivastav", "y02"])
def test_schemes_load_and_codes_valid(scheme):
    df = pc.load(scheme)
    assert len(df) > 0
    if "code_type" in df:
        df = df[df["code_type"] != "complex"]
    bad = [c for c in df["code"] if not CODE.match(c)]
    assert not bad, bad[:5]


def test_jee_srivastav_categories():
    df = pc.load("jee_srivastav")
    assert set(df["category"]) == {"clean", "grey", "dirty"}
    assert pc.is_in_scheme("Y04S10/12", df, "clean")
    assert pc.is_in_scheme("F02B1/00", df, "dirty")
    assert not pc.is_in_scheme("H01L31/00", df)


def test_metadata_matches_files():
    meta = pc.metadata()
    assert set(meta) == set(pc.SCHEMES)
