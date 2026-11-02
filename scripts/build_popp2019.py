"""data/popp_2019/popp2019.csv

Source: Popp, D., Pless, J., Haščič, I., Johnstone, N. "Innovation and Entrepreneurship in the Energy Sector",
NBER chapter draft of 6 December 2019 (c14375.rev0); published 2022 in The Role of Innovation and
Entrepreneurship in Economic Growth, Univ. of Chicago Press, pp. 175-248. Appendix Table A (CPC codes).
group: clean_energy | enabling | hydrofracturing. category: clean for the first two, 'fossil' for
hydrofracturing (the paper does not label it 'dirty'). requires_keywords=true for the robustness codes that
the paper only uses together with a keyword search (hydraulic fracturing, horizontal drilling, well completion).
Range notation: 'Y02B 20/00-70/00' = whole groups Y02B20..Y02B70.
"""
import csv
from pathlib import Path

# (group, technology, code, code_to, requires_keywords, description)
R = [
 ("clean_energy","Building energy efficiency","Y02B20","Y02B70","false","Aspects of energy efficiency related to lighting, appliances, etc. (Y02B 20/00-70/00)"),
 ("clean_energy","Building energy efficiency","Y02B80","","false","Aspects of energy efficiency related to building envelope"),
 ("clean_energy","Carbon capture and storage","Y02C","","false","Capture, storage, sequestration or disposal of greenhouse gases"),
 ("clean_energy","Solar photovoltaic (PV)","Y02E10/50","","false","Photovoltaic (PV) energy"),
 ("clean_energy","Solar thermal energy","Y02E10/40","","false","Solar thermal energy"),
 ("clean_energy","Wind energy","Y02E10/70","","false","Wind energy"),
 ("clean_energy","Hybrid and electric vehicles","Y02T10/62","","false","Hybrid vehicles"),
 ("clean_energy","Hybrid and electric vehicles","Y02T10/64","","false","Electric vehicles"),
 ("enabling","Energy storage","Y02E60/10","","false","Energy storage"),
 ("enabling","Smart grids","Y04S","","false","Systems integrating technologies related to power network operation, communication or information technologies (smart grids)"),
 ("enabling","Systems integration: building","Y02B70/30","Y02B70/346","false","Smart grids as CCMT/enabling technology in buildings sector (Y02B 70/30-346)"),
 ("enabling","Systems integration: building","Y02B90/20","Y02B90/2692","false","Smart grids as enabling technology in buildings sector (Y02B 90/20-2692)"),
 ("enabling","Systems integration: energy","Y02E40/70","Y02E40/76","false","Smart grids as CCMT/enabling technology in the energy generation sector (Y02E 40/70-76)"),
 ("enabling","Systems integration: energy","Y02E60/70","Y02E60/7892","false","Smart grids as enabling technology in the energy generation sector (Y02E 60/70-7892)"),
 ("enabling","Systems integration: transportation","Y02T90/167","Y02T90/169","false","Smart grids as interface for battery charging of EV/HEV (Y02T 90/167-169)"),
 ("hydrofracturing","Hydrofracturing (main search, Figure 10)","C10G1","","false","Production of liquid hydrocarbon mixtures from oil-shale, oil-sand, or non-melting solid carbonaceous materials"),
 ("hydrofracturing","Hydrofracturing (main search, Figure 10)","E21B43","","false","Methods or apparatus for obtaining oil, gas, water, soluble or meltable materials or a slurry of minerals from wells"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","E21B36","","true","Heating, cooling, insulating arrangements for boreholes or wells"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","C10G2300","","true","Aspects relating to hydrocarbon processing covered by groups C10G 1/00-C10G 99/00"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","Y10T29","","true","Metal working"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","C09K8","","true","Compositions for drilling of boreholes or wells; compositions for treating boreholes or wells"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","E21B47","","true","Survey of boreholes or wells"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","B32B15","","true","Layered products comprising a layer of metal"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","E21B7","","true","Special methods or apparatus for drilling"),
 ("hydrofracturing","Hydrofracturing (robustness, with keywords)","B32B1","","true","Layered products having a general shape other than plane"),
]
SRC = "Popp, Pless, Hascic, Johnstone, NBER chapter draft 6 Dec 2019, Appendix Table A"
root = Path(__file__).resolve().parents[1]
rows = [dict(scheme="popp_2019", scheme_version="NBER-chapter-2019-12-06",
             category="fossil" if g == "hydrofracturing" else "clean", group=g, technology=t, code=c, code_to=to,
             code_system="CPC", requires_keywords=kw, description=d, source=SRC) for g, t, c, to, kw, d in R]
with open(root / "data/popp_2019/popp2019.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
