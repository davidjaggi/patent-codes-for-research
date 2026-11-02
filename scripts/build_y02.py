"""Build data/y02/y02_y04s.csv: the nine top-level Y02/Y04S CPC subclasses.

A subclass code covers every group/subgroup below it (patentcodes.covers("Y02B", "Y02B90/10") is
True), so these nine rows identify all Y02/Y04S-tagged patents. Section names and status are taken from
the EPO page https://www.epo.org/en/news-events/in-focus/classification/classification/updatesYO2andY04S
(status of every section: December 2021; page text supplied by the user, page not fetched directly).
"""
import csv
from pathlib import Path

EPO_STATUS = "December 2021"
SECTIONS = [
    ("Y02A", "Adaptation to climate change"),
    ("Y02B", "Buildings"),
    ("Y02C", "Capture and storage of greenhouse gases"),
    ("Y02D", "ICT aiming at the reduction of own energy use"),
    ("Y02E", "Production, distribution and transport of energy"),
    ("Y02P", "Industry and agriculture"),
    ("Y02T", "Transportation"),
    ("Y02W", "Waste and wastewater"),
    ("Y04S", "Smart grids"),
]
root = Path(__file__).resolve().parents[1]
rows = [dict(scheme="y02", scheme_version=EPO_STATUS, code=c, code_to="", code_system="CPC",
             level="subclass", title=t, epo_status=EPO_STATUS) for c, t in SECTIONS]
with open(root / "data/y02/y02_y04s.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
