"""raw/ipc_green_inventory_chen.xlsx -> data/ipc_green_inventory/ipc_gi.csv

Source: WIPO IPC Green Inventory (https://www.wipo.int/classifications/ipc/green-inventory/home),
as expanded to one IPC code per row by Shuang Chen
(https://github.com/shuangchenfinance/greenpatent, MIT licence). Ranges such as
'C10L 5/00, 5/40-5/48' are already expanded. The topic hierarchy of the WIPO
inventory is NOT contained in that file, so topic_1/topic_2 are empty.
"""
import re
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[1]
df = pd.read_excel(root / "raw" / "ipc_green_inventory_chen.xlsx")
codes = [re.sub(r"\s+", "", str(c)).upper() for c in df["IPC_Codes"].dropna()]
codes = list(dict.fromkeys(codes))
bad = [c for c in codes if not re.match(r"^[A-H]\d{2}[A-Z]\d*(/\d+)?$", c)]
assert not bad, bad
out = pd.DataFrame({
    "scheme": "ipc_gi", "scheme_version": "WIPO-via-Chen-2024", "topic_1": "", "topic_2": "",
    "code": codes, "code_to": "", "code_system": "IPC", "description": "",
})
out.to_csv(root / "data/ipc_green_inventory/ipc_gi.csv", index=False)
print(len(out), "codes;", sum(len(c) == 4 for c in codes), "subclass-level")
