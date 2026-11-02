"""Load the shipped code lists as pandas DataFrames."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parent
_DATA = _ROOT / "data"
if not _DATA.exists():  # source checkout
    _DATA = _ROOT.parents[1] / "data"

SCHEMES = {
    "envtech": "envtech/envtech.csv",
    "envtech_expanded": "envtech/envtech_expanded.csv",
    "dechezlepretre_martin_mohnen": "dechezlepretre_martin_mohnen/dmm2013.csv",
    "aghion_benabou_martin_roulet": "aghion_benabou_martin_roulet/abmr2021.csv",
    "dechezlepretre_muckley_neelakantan": "dechezlepretre_muckley_neelakantan/dmn2021.csv",
    "aghion_2016": "aghion_2016/aghion2016.csv",
    "popp_2019": "popp_2019/popp2019.csv",
    "iea_epo_2021": "iea_epo_2021/iea_epo_2021.csv",
    "jee_srivastav": "jee_srivastav/jee_srivastav.csv",
    "y02": "y02/y02_y04s.csv",
    "ipc_gi": "ipc_green_inventory/ipc_gi.csv",
}


def load(scheme: str) -> pd.DataFrame:
    if scheme not in SCHEMES:
        raise KeyError(f"unknown scheme {scheme!r}; choose from {sorted(SCHEMES)}")
    return pd.read_csv(_DATA / SCHEMES[scheme], dtype=str, keep_default_na=False)


def load_iea_queries() -> pd.DataFrame:
    """Full-text queries [1]-[13] used with the IEA/EPO CPC ranges (English)."""
    return pd.read_csv(_DATA / "iea_epo_2021" / "iea_epo_2021_queries.csv", dtype=str)


def metadata() -> dict:
    return json.loads((_DATA.parent / "schemes.json").read_text())
