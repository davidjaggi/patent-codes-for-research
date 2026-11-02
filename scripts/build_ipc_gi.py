"""raw/favot2023 -> data/ipc_green_inventory/ipc_gi.csv

WIPO IPC Green Inventory (2022 list) as expanded and validated against PATSTAT IPC symbols by
Favot et al. (2023), https://doi.org/10.1016/j.rcradv.2023.200132 (CC-BY-4.0).
Topic hierarchy (topic_1 = upper-case heading, topic_2 = sub-heading) is read from the WIPO xlsx.
"""
import re
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[1]
raw = root / "raw" / "favot2023"

wipo = pd.read_excel(raw / "2IPCGreenInventoryList_2022WIPO.xlsx", dtype=str)
t1 = t2 = ""
hier: dict[str, set] = {}
for _, r in wipo.iterrows():
    topic = str(r["TOPIC"]).strip()
    if pd.isna(r["IPC"]):                      # heading row
        if topic.isupper():
            t1, t2 = topic, ""
        else:
            t2 = topic
    else:
        hier.setdefault(topic, set()).add((t1, t2))

res = pd.read_csv(raw / "IPC_green_codes.csv", header=None, names=["code", "topic"], dtype=str,
                  encoding="utf-8-sig")
res["code"] = res["code"].str.replace(r"\s+", "", regex=True).str.upper()
bad = [c for c in res["code"] if not re.match(r"^[A-H]\d{2}[A-Z]?\d*(/\d+)?$", c)]
assert not bad, bad[:5]

def lookup(topic, i):
    h = sorted(hier.get(topic, {("", "")}))
    return " | ".join(dict.fromkeys(x[i] for x in h))     # ambiguous topics: joined, kept visible

out = pd.DataFrame({
    "scheme": "ipc_gi", "scheme_version": "WIPO-2022-list (Favot et al. 2023)",
    "topic_1": res["topic"].map(lambda t: lookup(t, 0)), "topic_2": res["topic"].map(lambda t: lookup(t, 1)),
    "topic": res["topic"], "code": res["code"], "code_to": "", "code_system": "IPC",
})
out.to_csv(root / "data/ipc_green_inventory/ipc_gi.csv", index=False)
print(len(out), "codes,", out["topic"].nunique(), "topics; ambiguous topic names:",
      sum(len(v) > 1 for v in hier.values()))
