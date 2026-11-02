"""data/aghion_2016/aghion2016.csv

Source: Aghion, Dechezleprêtre, Hémous, Martin, Van Reenen (2016). Carbon Taxes, Path Dependency, and
Directed Technical Change: Evidence from the Auto Industry. Journal of Political Economy 124(1): 1-51.
Table 1 "Definition of IPC Patent Classes for Clean and Dirty Patents" (panels A clean, B dirty, C grey).
Ranges (F02M39-71, F02M3/02-05) are kept as code/code_to. B60W10/08, 24, 26 are three codes.
Note: the 2019 IPC revision moved B60L11 to B60L50-B60L58 (see Jee & Srivastav note 4).
"""
import csv
from pathlib import Path

# (category, subsector, code, code_to, description)
R = [
 ("clean","Electric vehicles","B60L11","","Electric propulsion with power supplied within the vehicle"),
 ("clean","Electric vehicles","B60L3","","Electric devices on electrically propelled vehicles for safety purposes; monitoring operating variables"),
 ("clean","Electric vehicles","B60L15","","Methods, circuits, or devices for controlling the traction-motor speed of electrically propelled vehicles"),
 ("clean","Electric vehicles","B60K1","","Arrangement or mounting of electrical propulsion units"),
 ("clean","Electric vehicles","B60W10/08","","Conjoint control of vehicle subunits of different type or different function, including control of electric propulsion units"),
 ("clean","Electric vehicles","B60W10/24","","Conjoint control of vehicle subunits ... including control of energy storage means"),
 ("clean","Electric vehicles","B60W10/26","","Conjoint control of vehicle subunits ... for electrical energy, e.g. batteries or capacitors"),
 ("clean","Hybrid vehicles","B60K6","","Arrangement or mounting of plural diverse prime movers for mutual or common propulsion, e.g. hybrid propulsion systems"),
 ("clean","Hybrid vehicles","B60W20","","Control systems specially adapted for hybrid vehicles"),
 ("clean","Regenerative braking","B60L7/1","","Dynamic electric regenerative braking"),
 ("clean","Regenerative braking","B60L7/20","","Braking by supplying regenerated power to the prime mover of vehicles comprising engine-driven generators"),
 ("clean","Hydrogen vehicles/fuel cells","B60W10/28","","Conjoint control of vehicle subunits of different type or different function, including control of fuel cells"),
 ("clean","Hydrogen vehicles/fuel cells","B60L11/18","","Electric propulsion with power supplied from primary cells, secondary cells, or fuel cells"),
 ("clean","Hydrogen vehicles/fuel cells","H01M8","","Fuel cells; manufacture thereof"),
 ("dirty","Internal combustion engine","F02B","","Internal combustion piston engines; combustion engines in general"),
 ("dirty","Internal combustion engine","F02D","","Controlling combustion engines"),
 ("dirty","Internal combustion engine","F02F","","Cylinders, pistons, or casings for combustion engines; arrangement of sealings"),
 ("dirty","Internal combustion engine","F02M","","Supplying combustion engines with combustible mixtures or constituents thereof"),
 ("dirty","Internal combustion engine","F02N","","Starting of combustion engines"),
 ("dirty","Internal combustion engine","F02P","","Ignition (other than compression ignition) for internal combustion engines"),
 ("grey","Fuel efficiency of internal combustion engines","F02M39","F02M71","Fuel injection apparatus"),
 ("grey","Fuel efficiency of internal combustion engines","F02M3/02","F02M3/05","Idling devices for carburetors preventing flow of idling fuel"),
 ("grey","Fuel efficiency of internal combustion engines","F02M23","","Apparatus for adding secondary air to fuel-air mixture"),
 ("grey","Fuel efficiency of internal combustion engines","F02M25","","Engine-pertinent apparatus for adding nonfuel substances or small quantities of secondary fuel"),
 ("grey","Fuel efficiency of internal combustion engines","F02D41","","Electrical control of supply of combustible mixture or its constituents"),
 ("grey","Fuel efficiency of internal combustion engines","F02B47/06","","Methods of operating engines involving adding nonfuel substances or antiknock agents ... including nonairborne oxygen"),
]
SRC = "Aghion et al. (2016), J. Political Economy 124(1), Table 1"
root = Path(__file__).resolve().parents[1]
rows = [dict(scheme="aghion_2016", scheme_version="JPE-2016", category=c, sector="auto", subsector=s, code=k, code_to=t,
             code_system="IPC", description=d, source=SRC) for c, s, k, t, d in R]
with open(root / "data/aghion_2016/aghion2016.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
