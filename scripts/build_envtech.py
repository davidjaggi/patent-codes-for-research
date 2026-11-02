"""raw/env_tech.xlsx -> data/envtech/envtech.csv (long format, one code per row).

Source table: Hascic & Migotto (2015), OECD Environment WP 89, Annex (ENV-TECH).
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import re
from patentcodes.expand import expand_code, split_range, split_codes  # noqa: E402

root = Path(__file__).resolve().parents[1]
df = pd.read_excel(root / "raw" / "env_tech.xlsx")
rows, failed = [], []
for _, r in df.iterrows():
    if pd.isna(r["IPC and CPC Classes"]):
        continue
    cell = str(r["IPC and CPC Classes"])
    parts = [cell] if "[" in cell else split_codes(cell)
    for raw in parts:
        try:
            codes = expand_code(raw)
        except ValueError:
            failed.append(raw)
            codes = [raw.strip()]
        for c in codes:
            to, ctype = "", "code"
            if not re.match(r"^[A-HY]\d{2}[A-Z]\d*(/\d+(-\d+)?)?$", c):
                ctype = "complex"          # conditional/free-text combination
                c = " ".join(raw.split())
            elif "-" in c:
                c, to = split_range(c)
                ctype = "range"
            rows.append({
                "scheme": "envtech", "scheme_version": "Hascic-Migotto-2015",
                "level_1": r["Level 1"], "level_2": r["Level 2"], "level_3": r["Level 3"],
                "description": " ".join(str(r["Description"]).split()),
                "code": c, "code_to": to, "code_type": ctype, "code_raw": raw.strip(), "code_system": "IPC/CPC",
            })
out = pd.DataFrame(rows).drop_duplicates()
out.to_csv(root / "data" / "envtech" / "envtech.csv", index=False)
print(len(out), "rows; unparsed ranges:", failed)
