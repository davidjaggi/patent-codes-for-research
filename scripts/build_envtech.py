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
# Corrections found by comparing raw/env_tech.xlsx with the original annex of Hascic & Migotto (2015)
# (ENV/EPOC/WPEI(2014)6/FINAL, Annex): the spreadsheet lacked these entries.
CORRECTIONS = [
    ("4.6.4.", "Y02E60/70-7892", "Systems integrating technologies related to power network operation and communication or information technologies mediating in the improvement of the carbon footprint of electrical power generation, transmission or distribution (detail row of 4.6.4 Smart grids in the energy sector)"),
    ("6.1.1.", "Y02T10/10", "Conventional vehicles (based on internal combustion engine); heading range Y02T10/10-56 includes /10"),
]
for prefix, code, desc in CORRECTIONS:
    ref = df[df["Level 3"].astype(str).str.startswith(prefix)].iloc[0]
    c, to = split_range(code) if "-" in code else (code, "")
    rows.append({
        "scheme": "envtech", "scheme_version": "Hascic-Migotto-2015",
        "level_1": ref["Level 1"], "level_2": ref["Level 2"], "level_3": ref["Level 3"],
        "description": desc, "code": c, "code_to": to, "code_type": "range" if to else "code",
        "code_raw": code, "code_system": "IPC/CPC",
    })
out = pd.DataFrame(rows).drop_duplicates()
out.to_csv(root / "data" / "envtech" / "envtech.csv", index=False)
print(len(out), "rows; unparsed ranges:", failed)
