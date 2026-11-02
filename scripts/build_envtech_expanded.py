"""raw/favot2023/ENVTECH -> data/envtech/envtech_expanded.csv

ENV-TECH (Haščič & Migotto 2015) with every range expanded to single codes, validated against
PATSTAT, one file per topic, by Favot et al. (2023). Directory name gives level 1 (1..8) and
code system (IPC / CPC); file name gives the topic.
"""
import re
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[1]
rows = []
for d in sorted((root / "raw/favot2023/ENVTECH").iterdir()):
    lvl, system = d.name.split("_")
    for f in sorted(d.glob("*.csv")):
        df = pd.read_csv(f, dtype=str, encoding="utf-8-sig")
        for c in df["Code"].dropna():
            code = re.sub(r"\s+", "", c).upper()
            rows.append(dict(scheme="envtech_expanded", scheme_version="Favot-2023", level_1=lvl,
                             topic=f.stem, code=code, code_to="", code_system=system))
out = pd.DataFrame(rows).drop_duplicates()
bad = [c for c in out["code"] if not re.match(r"^[A-HY]\d{2}[A-Z]?\d*(/\d+)?$", c)]
assert not bad, bad[:5]
out.to_csv(root / "data/envtech/envtech_expanded.csv", index=False)
print(len(out), "rows", out["code"].nunique(), "unique codes")
