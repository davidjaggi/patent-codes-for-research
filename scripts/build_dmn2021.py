"""data/dechezlepretre_muckley_neelakantan/dmn2021.csv

Source: Dechezleprêtre, A., Muckley, C. B., Neelakantan, P. (2021). Does the Market Value Clean Innovation?
Evidence from US Listed Firms. In: Applied Operations Research and Financial Modelling in Energy, Springer,
pp. 225-?, https://doi.org/10.1007/978-3-030-84981-8_11. Internet Appendix 1, Table 8 (clean) and Table 9
(dirty). Everything else is 'other'. Table 10 (emerging technologies: B82, H04W, G06, C12N...) is a non-green
control group and is not included. Note that this paper counts Y02E20 (combustion technologies with
mitigation potential) as clean, whereas Jee & Srivastav treat it as grey.
"""
import csv
from pathlib import Path

CLEAN = [
 ("Y02E10","Energy generation through renewable energy sources"),
 ("Y02E20","Combustion technologies with mitigation potential"),
 ("Y02E30","Energy generation of nuclear origin"),
 ("Y02E40","Technologies for an efficient electrical power generation, transmission or distribution"),
 ("Y02E50","Technologies for the production of fuel of non-fossil origin"),
 ("Y02E60","Enabling technologies or technologies with a potential or indirect contribution to GHG emissions mitigation"),
 ("Y02E70","Other energy conversion or management systems reducing GHG emissions"),
 ("Y02C10","CO2 capture or storage"),
 ("Y02C20","Capture or disposal of greenhouse gases [GHG] other than CO2"),
 ("Y02T10","Road transport of goods or passengers"),
 ("Y02T30","Transportation of goods or passengers via railways"),
 ("Y02T50","Aeronautics or air transport"),
 ("Y02T70","Maritime or waterways transport"),
 ("Y02T90","Enabling technologies or technologies with a potential or indirect contribution to GHG emissions mitigation"),
 ("Y02B10","Integration of renewable energy sources in buildings"),
 ("Y02B20","Energy efficient lighting technologies"),
 ("Y02B30","Energy efficient heating, ventilation or air conditioning [HVAC]"),
 ("Y02B40","Technologies aiming at improving the efficiency of home appliances"),
 ("Y02B50","Energy efficient technologies in elevators, escalators and moving walkways"),
 ("Y02B70","Technologies for an efficient end-user side electric power management and consumption"),
 ("Y02B80","Architectural or constructional elements improving the thermal performance of buildings"),
 ("Y02B90","Enabling technologies or technologies with a potential or indirect contribution to GHG emissions mitigation"),
]
DIRTY = [
 ("C10J","Production of producer gas, water-gas, synthesis gas from solid carbonaceous material, or mixtures containing these gases; carburetting air or other gases"),
 ("F01K","Steam engine plants; steam accumulators; engine plants not otherwise provided for; engines using special working fluids or cycles"),
 ("F02C","Gas-turbine plants; air intakes for jet-propulsion plants; controlling fuel supply in air-breathing jet-propulsion plants"),
 ("F02G","Hot gas or combustion-product positive-displacement engine plants; use of waste heat of combustion engines; not otherwise provided for"),
 ("F22","Steam generation"),
 ("F23","Combustion apparatus; combustion processes"),
 ("F27","Furnaces; kilns; ovens; retorts"),
 ("F02B","Internal-combustion piston engines; combustion engines in general"),
]
SRC = "Dechezleprêtre, Muckley & Neelakantan (2021), Internet Appendix 1, Tables 8-9"
root = Path(__file__).resolve().parents[1]
rows = [dict(scheme="dechezlepretre_muckley_neelakantan", scheme_version="2021", category=cat, code=k, code_to="",
             code_system="CPC" if k.startswith("Y02") else "IPC/CPC", description=d, source=SRC)
        for cat, L in (("clean", CLEAN), ("dirty", DIRTY)) for k, d in L]
with open(root / "data/dechezlepretre_muckley_neelakantan/dmn2021.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
