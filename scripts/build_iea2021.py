"""data/iea_epo_2021/iea_epo_2021.csv

Source: EPO & IEA/OECD (April 2021), Methodology for identifying fossil fuel supply related technologies in
patent data (annex to "Patents and the energy transition"), section 3 "Concordance table of CPC ranges and
fossil fuel supply fields" and section 4 (full-text queries). Transcribed by hand from the PDF.

Columns: category/subcategory = the cartography; code (+ code_to for 'X to Y' ranges); low / low_to = the
'/LOW' marker on the first / last code of the entry. Definition in the annex: "/LOW" means that not only the
class itself but also its respective subclasses (sub-levels) must be taken into account; codes WITHOUT the
marker are the class only. filter_including = labels [1]-[13] of the full-text queries (section 4) that must
match (several labels = alternatives, as printed); filter_excluding = exclusion criteria as printed. The
queries themselves are in iea_epo_2021_queries.csv (English only; French and German are in the PDF).
"""
import csv
import re
from pathlib import Path

UNC = "E21B43/26/low OR E21B7/04/low OR E21B7/06/low OR E21B43/16/low OR E21B43/24/low OR E21B43/006 OR E21B41/0099"
BIO = "[10] OR C10L2200/0469/low"
UP, PR, TD = "Upstream", "Processing and downstream", "Transmission and distribution"
CONV, UNCV, COAL = "Conventional oil and gas exploration and extraction", "Unconventional oil and gas exploration and extraction", "Coal and solid fuels exploration and mining"

# (category, subcategory, code spec ('X to Y' for ranges, ';' separates entries), including, excluding)
T = [
 (UP,CONV,"B03B9/02","",""), (UP,CONV,"B03D2203/006","",""),
 (UP,CONV,"B63B35/4413","[1], [2], [4]",""), (UP,CONV,"B63B2035/442","[1], [2], [4]",""),
 (UP,CONV,"B63B2035/448","[1], [2], [4]",""), (UP,CONV,"B63B75/00","[1], [2], [4]",""),
 (UP,CONV,"C09K8/low","",""), (UP,CONV,"C10L5/04","",""),
 (UP,CONV,"E02B17/00","[1], [8]","[12]"),
 (UP,CONV,"E02B17/0004 to E02B2017/0039/low","[1], [8]","[12]"),
 (UP,CONV,"E02B2017/0056/low to E02B2201/00/low","[1], [8]","[12]"),
 (UP,CONV,"E21B1/00/low to E21B41/00/low","[1], [2], [4], [8]",UNC),
 (UP,CONV,"E21B43/00","[1], [2], [4], [8]",UNC), (UP,CONV,"E21B43/003","[1], [2], [4], [8]",UNC),
 (UP,CONV,"E21B43/006","[1], [2], [4], [8]",UNC), (UP,CONV,"E21B43/01/low","[1], [2], [4], [8]",UNC),
 (UP,CONV,"E21B43/02/low to E21B43/12/low","[1], [2], [4], [8]",UNC),
 (UP,CONV,"E21B43/14","[1], [2], [4], [8]",UNC), (UP,CONV,"E21B43/16/low","[1], [2], [4], [8]",UNC),
 (UP,CONV,"E21B43/25/low","[1], [2], [4], [8]",UNC),
 (UP,CONV,"E21B43/28/low to E21B43/34/low","[1], [2], [4], [8]",UNC),
 (UP,CONV,"E21B44/00/low to E21B49/00/low","[1], [2], [4], [8]",UNC),
 (UP,UNCV,"E21B43/26/low","[1], [2], [4], [8]",""), (UP,UNCV,"E21B7/04/low","[1], [2], [4], [8]",""),
 (UP,UNCV,"E21B43/16/low","[1], [2], [4], [8]",""), (UP,UNCV,"E21B43/006","[1], [2], [4], [8]",""),
 (UP,UNCV,"E21B41/0099","[1], [2], [4], [8]",""),
 (UP,COAL,"B03B9/005","",""), (UP,COAL,"B03B1/00/low","[1], [3]",""), (UP,COAL,"B03D2203/08","",""),
 (UP,COAL,"B61D11/00/low","[1], [3]",""), (UP,COAL,"E21C25/00/low to E21C51/00/low","[1], [3]",""),
 (PR,"Oil refining","C10G2/00/low to C10G99/00/low","",""),
 (PR,"Oil refining","C10G1/00;C10G1/002 to C10G1/042;C10G1/047 to C10G1/10","",""),
 (PR,"Oil refining","C10L1/00/low","[1], [2], [5]",BIO),
 (PR,"Gas conditioning","C10K1/00/low","",""), (PR,"Gas conditioning","C10K3/00/low","",""),
 (PR,"Gas conditioning","C10L3/06/low","[4], [6]",BIO),
 (PR,"Gas conditioning","F25J3/0209/low","",""), (PR,"Gas conditioning","F25J3/061/low","",""),
 (PR,"Solid fuel conditioning","C10F5/00/low to C10F7/00/low","",""),
 (PR,"Solid fuel conditioning","C10L5/06/low","[3], [7]",BIO), (PR,"Solid fuel conditioning","C10L5/24","[3], [7]",BIO),
 (PR,"Solid fuel conditioning","C10L5/26/low","[3], [7]",BIO), (PR,"Solid fuel conditioning","C10L5/34/low","[3], [7]",BIO),
 (PR,"Coal-to-gas","C10B1/00/low to C10B51/00/low","",""), (PR,"Coal-to-gas","C10B53/04 to C10B53/08","",""),
 (PR,"Coal-to-gas","C10B55/00/low to C10B57/00/low","",""), (PR,"Coal-to-gas","C10J1/00/low to C10J3/00/low","",""),
 (PR,"Coal-to-liquids and gas-to-liquids","C01B3/22/low","","C01B2203/062"),
 (PR,"Coal-to-liquids and gas-to-liquids","C01B3/32/low","","C01B2203/062"),
 (PR,"Coal-to-liquids and gas-to-liquids","C10J3/00/low","","C10G2/30/low"),
 (PR,"Hydrogen fuel production","C01B3/22/low","",""), (PR,"Hydrogen fuel production","C01B3/32/low","",""),
 (TD,"Liquid fuel pipelines","B63B27/34","[2], [5]",""), (TD,"Liquid fuel pipelines","B63B27/24/low","[2], [5]",""),
 (TD,"Liquid fuel pipelines","F17D1/00/low to F17D5/00/low","[2], [5]",""),
 (TD,"Gas fuel pipelines","B63B27/24/low","[4], [6]",""), (TD,"Gas fuel pipelines","F17D1/04/low","[4], [6]",""),
 (TD,"Gas fuel pipelines","F17D1/065/low","[4], [6]",""),
 (TD,"Liquid fuel tanker shipping","B63B25/08/low","[2], [5]",""), (TD,"Liquid fuel tanker shipping","B67D9/00/low","[2], [5]",""),
 (TD,"Liquefied gaseous fuel shipping","F25J1/0022/low","",""),
 (TD,"Compressed gaseous fuel shipping","B63B2025/087","[4], [6]",""), (TD,"Compressed gaseous fuel shipping","B63B25/14","[4], [6]",""),
 (TD,"Compressed gaseous fuel shipping","B63B25/16","[4], [6]",""),
 (TD,"Solid fuel shipping","B63B25/04","[3]",""),
 (TD,"Road tanker liquid fuels transport","B60P3/22/low","","@(+tank+ OR reservoir OR citerne) s [5]"),
 (TD,"Road tanker gaseous fuels transport","B60P3/22/low","","@(+tank+ OR reservoir OR citerne) s [6]"),
 (TD,"Rail tanker liquid fuels transport","B61D5/00/low","[2], [5]",""), (TD,"Rail tanker liquid fuels transport","B61D3/00/low","[2], [5]",""),
 (TD,"Rail tanker liquid fuels transport","B61D15/00/low","[2], [5]",""), (TD,"Rail tanker liquid fuels transport","B61D49/00/low","[2], [5]",""),
 (TD,"Rail tanker gaseous fuels transport","B61D3/00/low","[4], [6]",""), (TD,"Rail tanker gaseous fuels transport","B61D15/00/low","[4], [6]",""),
 (TD,"Rail tanker gaseous fuels transport","B61D49/00/low","[4], [6]",""),
 (TD,"Rail solid fuel transport","B61D7/00/low","[3], [7]",""), (TD,"Rail solid fuel transport","B61D9/00/low","[3], [7]",""),
 (TD,"Rail solid fuel transport","B61D3/00/low","[3], [7]",""), (TD,"Rail solid fuel transport","B61D15/00/low","[3], [7]",""),
 (TD,"Rail solid fuel transport","B61D49/00/low","[3], [7]",""),
 (TD,"Underground liquid fuels storage","B65G5/00/low","[1], [2], [5]",""),
 (TD,"Underground gaseous fuels storage","F17C2270/0142/low","[4], [6]",""),
 (TD,"Stationary tank storage for liquids","E02D27/38","[2], [5]",""),
 (TD,"Stationary tank storage for gases","F17B1/26","[4], [6]",""),
 (TD,"Stationary tank storage for gases","F17C1/00/low to F17C13/00/low","[4], [6]",""),
 (TD,"Stationary tank storage for gases","F17C2221/032/low","",""),
 (TD,"Solid fuel storage","B65G3/00/low","[3], [7]",""),
 (TD,"Liquid fuel distribution (gas stations)","G01M3/2892","",""),
 (TD,"Liquid fuel distribution (gas stations)","G01M3/32/low","[5]",""),
 (TD,"Gaseous fuel distribution","F17C2265/06/low","[4], [6]",""),
]

def tok(t):
    t = t.strip(); low = t.endswith("/low")
    return re.sub(r"/low$", "", t), low

SRC = "EPO & IEA/OECD (2021), Methodology for identifying fossil fuel supply related technologies in patent data, section 3"
root = Path(__file__).resolve().parents[1]
rows = []
for cat, sub, spec, inc, exc in T:
    for ent in spec.split(";"):
        parts = [p for p in ent.split(" to ")]
        c, low = tok(parts[0]); to, low_to = tok(parts[1]) if len(parts) > 1 else ("", False)
        note = ""
        if exc.startswith("@"):
            note, exc = exc[1:], ""        # layout of the PDF is ambiguous (see notes in schemes.json)
        rows.append(dict(scheme="iea_epo_2021", scheme_version="April-2021", category="dirty", fossil_category=cat,
                         fossil_subcategory=sub, code=c, code_to=to, low=str(low).lower(),
                         low_to=str(low_to).lower() if to else "", code_system="CPC", filter_including=inc,
                         filter_excluding=exc, filter_note=note, source=SRC))
with open(root / "data/iea_epo_2021/iea_epo_2021.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

Q = [
 ("1","fossil OR (non w renewable) OR hydrocarbon? OR petrol+"),
 ("2","petroleum OR (crude w oil) OR oil"),
 ("3","coal OR mineral? OR coke OR peat OR BKB OR briquette OR asphaltite OR ortholignite OR metaanthracite OR lignite OR hardcoal OR browncoal OR (brown w coal) OR (oil 2w deposit) OR (oil w bear+) OR bitumen OR bituminous OR (tar w sand) OR (oil w sand)"),
 ("4","methane OR (natural w gas) OR hydrate? OR (petroleum w gas+) OR hydrogen OR (boil 2w gas+) OR BOG OR LNG OR LPG OR (liqui+ 2w (fuel? OR petroleum)) OR (liqui+ 2w gas+) OR (gaseous w fuel?)"),
 ("5","LNG OR LPG OR (liquid w fuel?) OR diesel OR gasoline OR (jet w fuel?) OR (fuel w oil) OR (bunker w fuel?) OR kerosene OR (oil w product?) OR octane OR cetane OR propane OR butane"),
 ("6","methane OR (natural w gas+) OR CNG OR LNG OR PLNG OR propane OR butane OR LPG OR Hydrate? OR (petroleum w gas+) OR hydrogen OR liquefied OR (compressed w gas+)"),
 ("7","coal OR BKB OR briquette OR asphaltite, ortholignite OR metaanthracite OR lignite OR hardcoal OR browncoal"),
 ("8","drilling OR offshore OR onshore OR oil OR hydrocarbon? OR gas+ OR subsea OR seabed OR reservoir OR petroleum OR methane OR formation OR riser? OR (well w head) OR bop OR (blowout w prevent+) OR fracturing OR frack+ OR ((bottom OR down) w hole)"),
 ("9","(oil 3w (spill?, containment?)) OR hydrocarbon? OR petrol+ OR (crude w oil) OR (light w oil) OR (hazardous w material?) OR chemical? OR (raw w oil) OR tanker? OR (liquid w pollutant?) OR ((subsea OR underwater) w emission?)"),
 ("10","biomass OR biofuel OR bioethanol OR biodiesel"),
 ("11","plastic OR (floating w debris) OR (floating w waste) OR leaves OR (solid w waste) OR (waste w matter) OR (floating w matter) OR pollutant?"),
 ("12","(wind w turbine) OR tower OR mast OR ((power OR electric) 3w generat+)"),
 ("13","(tar w sand?) OR (oil w sand?) OR (bituminous w sand?) OR frack+ OR (produced w water) OR drilling"),
]
with open(root / "data/iea_epo_2021/iea_epo_2021_queries.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["label", "language", "query"])
    for k, q in Q: w.writerow([k, "en", q])
print(len(rows), "rows;", len(Q), "queries")
