"""Build data/y02/y02_y04s.csv (PARTIAL: subclass + group codes named in the sources).

The complete Y02/Y04S tree must be generated from an official CPC release
(cooperativepatentclassification.org / EPO CPC scheme XML). That host was not
reachable when this file was written, so only the nine subclass headings and the
groups explicitly listed by Jee & Srivastav (2023) / Rozendaal (2024) are included.
"""
import csv
from pathlib import Path

SUB = [
 ("Y02A","Technologies for adaptation to climate change"),
 ("Y02B","Climate change mitigation technologies related to buildings, e.g. housing, house appliances or related end-user applications"),
 ("Y02C","Capture, storage, sequestration or disposal of greenhouse gases [GHG]"),
 ("Y02D","Climate change mitigation technologies in information and communication technologies [ICT], i.e. information and communication technologies aiming at the reduction of their own energy use"),
 ("Y02E","Reduction of greenhouse gas [GHG] emissions, related to energy generation, transmission or distribution"),
 ("Y02P","Climate change mitigation technologies in the production or processing of goods"),
 ("Y02T","Climate change mitigation technologies related to transportation"),
 ("Y02W","Climate change mitigation technologies related to wastewater treatment or waste management"),
 ("Y04S","Systems integrating technologies related to power network operation, communication or information technologies for improving the electrical power generation, transmission, distribution, management or usage, i.e. smart grids"),
]
GRP = [  # (code, parent, label as used in the papers)
 ("Y02E10/10","Y02E","Geothermal"),("Y02E10/20","Y02E","Hydro energy"),("Y02E10/30","Y02E","Energy from the sea, e.g. using wave energy or salinity gradient"),
 ("Y02E10/40","Y02E","Solar thermal energy"),("Y02E10/50","Y02E","Photovoltaic [PV] energy"),("Y02E10/60","Y02E","Thermal-PV hybrids"),
 ("Y02E10/70","Y02E","Wind energy"),("Y02E20","Y02E","Combustion technologies with mitigation potential"),("Y02E30","Y02E","Nuclear energy"),
 ("Y02E40","Y02E","Efficient electrical power generation, transmission or distribution"),("Y02E50","Y02E","Technologies for the production of fuel of non-fossil origin"),
 ("Y02E60","Y02E","Enabling technologies; technologies with a potential or indirect contribution to GHG emissions mitigation"),
 ("Y02E70","Y02E","Other energy conversion or management systems reducing GHG emissions"),
 ("Y02P10","Y02P","Technologies relating to metal processing"),("Y02P20","Y02P","Technologies relating to chemical industry"),
 ("Y02P30","Y02P","Technologies relating to oil refining and petrochemical industry"),("Y02P40","Y02P","Technologies relating to the processing of minerals"),
 ("Y02P60","Y02P","Technologies relating to agriculture, livestock or agroalimentary industries"),
 ("Y02P70","Y02P","Climate change mitigation technologies in the production process for final industrial or consumer products"),
 ("Y02P80","Y02P","Climate change mitigation technologies for sector-wide applications"),("Y02P90","Y02P","Enabling technologies with a potential contribution to GHG emissions mitigation"),
 ("Y02T10","Y02T","Road transport of goods or passengers"),("Y02T30","Y02T","Transportation of goods or passengers via railways"),
 ("Y02T50","Y02T","Aeronautics or air transport"),("Y02T70","Y02T","Maritime or waterways transport"),("Y02T90","Y02T","Enabling technologies or technologies with a potential or indirect contribution to GHG emissions mitigation"),
]
EPO_URL = "https://www.epo.org/en/news-events/in-focus/classification/classification/updatesYO2andY04S"
EPO_STATUS = "December 2021"  # status listed by the EPO for every section Y02A-Y02W and Y04S (page text supplied by the user)

root = Path(__file__).resolve().parents[1]
rows = [dict(scheme="y02", scheme_version="partial", code=c, parent="", level="subclass", title=t, epo_status=EPO_STATUS, complete="false") for c, t in SUB]
rows += [dict(scheme="y02", scheme_version="partial", code=c, parent=p, level="group", title=t, epo_status=EPO_STATUS, complete="false") for c, p, t in GRP]
with open(root / "data/y02/y02_y04s.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
