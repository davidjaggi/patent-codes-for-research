"""data/aghion_benabou_martin_roulet/abmr2021.csv

Source: Aghion, Bénabou, Martin, Roulet (2020 NBER WP; AER: Insights 2023), NBER WP 26921 / AER: Insights 5(1) 2023, "Environmental
preferences and technological choices: Is market competition clean or dirty?", Appendix Table A1 (CPC codes).
Auto sector only. 'other' = other automotive (B60), neither clean, dirty nor grey.
"""
import csv
from pathlib import Path

R = [
 ("clean","Y02T10/60","Other road transportation technologies with climate change mitigation effect"),
 ("clean","Y02T10/70","Energy storage for electromobility"),
 ("clean","Y02T90/10","Technologies related to electric vehicle charging"),
 ("clean","Y02T90/34","Fuel cell powered electric vehicles"),
 ("clean","Y02T90/42","Hydrogen as fuel for road transportation"),
 ("grey","Y02T10/10","Climate change mitigation technologies related to fuel injection"),
 ("grey","Y02T10/20","Climate change mitigation technologies related to exhaust after treatment"),
 ("grey","Y02T10/40","Climate change mitigation technologies related to engine management systems"),
 ("grey","Y02T10/50","Climate change mitigation technologies related to intelligent control systems"),
 ("dirty","F02","Combustion engines"),
 ("other","B60","Vehicles in general (other automotive)"),
]
SRC = "Aghion, Bénabou, Martin, Roulet (2020 NBER WP; AER: Insights 2023), NBER WP 26921, Appendix Table A1"
root = Path(__file__).resolve().parents[1]
rows = [dict(scheme="aghion_benabou_martin_roulet", scheme_version="NBER-2020", category=c, sector="auto", code=k,
             code_to="", code_system="CPC", description=d, source=SRC) for c, k, d in R]
with open(root / "data/aghion_benabou_martin_roulet/abmr2021.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
