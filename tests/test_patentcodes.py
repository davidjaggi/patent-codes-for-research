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


@pytest.mark.parametrize("scheme", ["envtech", "jee_srivastav", "y02", "ipc_gi", "envtech_expanded", "dechezlepretre_martin_mohnen", "aghion_benabou_martin_roulet", "dechezlepretre_muckley_neelakantan"])
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


def test_expanded_counts():
    assert pc.load("envtech_expanded")["code"].nunique() == 3150
    gi = pc.load("ipc_gi")
    assert len(gi) == 1214 and gi["topic"].nunique() == 170


def test_y02_top_level_covers_everything_below():
    y = pc.load("y02")
    assert sorted(y["code"]) == ["Y02A", "Y02B", "Y02C", "Y02D", "Y02E", "Y02P", "Y02T", "Y02W", "Y04S"]
    for code in ["Y02E10/70", "Y02P20/151", "Y04S10/12", "Y02T10/7258", "Y02A90/10"]:
        assert pc.is_in_scheme(code, y), code
    assert not pc.is_in_scheme("H01L31/00", y)


def test_main_group_and_subgroup_ranges():
    dmm = pc.load("dechezlepretre_martin_mohnen")
    grey = dmm[dmm["category"] == "grey"]
    assert pc.is_in_scheme("F02M45/00", grey)        # inside F02M39-71
    assert not pc.is_in_scheme("F02M75/00", grey)
    assert pc.is_in_scheme("F02M3/04", grey)         # inside F02M3/02-05
    assert pc.is_in_scheme("F02B1/00", dmm, "dirty")
    ab = pc.load("aghion_benabou_martin_roulet")
    assert pc.is_in_scheme("Y02T10/7005", ab, "clean")       # /70 covers its sub-subgroups
    assert not pc.is_in_scheme("Y02T10/7258", ab, "clean")   # /72 is a sibling, not a child
    assert pc.covers("Y02P20/15", "Y02P20/151")              # Rozendaal's /15 vs original /151


def test_envtech_matches_paper_annex():
    e = pc.load("envtech")
    assert pc.is_in_scheme("Y02E60/7400", e)   # Y02E60/70-7892 (added from the paper's annex)
    assert pc.is_in_scheme("Y02T10/10", e)


def test_dmn_dirty_equals_jee_srivastav_manufacturing_dirty():
    dmn = pc.load("dechezlepretre_muckley_neelakantan")
    js = pc.load("jee_srivastav")
    js_m = js[(js["category"] == "dirty") & (js["sector"] == "Manufacturing")]
    assert set(dmn[dmn["category"] == "dirty"]["code"]) == set(js_m["code"])
    assert pc.is_in_scheme("Y02E20/12", dmn, "clean")
