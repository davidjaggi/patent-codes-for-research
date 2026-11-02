"""Build data/jee_srivastav/jee_srivastav.csv.

Source: Jee & Srivastav (2023/24), "Pivoting from Dirty to Clean", Supplementary
Table 1 (clean/dirty/grey search strategy). The full code lists are taken from
Table E1 in Rozendaal (2024), "Market Power, Innovation, and the Green
Transition", which reproduces the Jee & Srivastav lists with all codes spelled
out (their own Supp. Table 1 refers to Haščič & Migotto 2015, Aghion et al. 2016,
IEA 2021 and Dechezleprêtre et al. 2021 for the dirty lists).
Rule from the papers: grey is removed from clean; patents both clean and dirty
are excluded from the main analysis.
"""
import csv
from pathlib import Path

# (category, sector, subsector, system, codes)
T = [
 # ---- clean (CPC) ----
 ("clean","Energy","Efficient electrical power generation, transmission or distribution","CPC","Y02E40"),
 ("clean","Energy","Enabling technologies","CPC","Y02E60"),
 ("clean","Energy","Geothermal","CPC","Y02E10/10"),
 ("clean","Energy","Hydro","CPC","Y02E10/20"),
 ("clean","Energy","Nuclear","CPC","Y02E30"),
 ("clean","Energy","Other energy conversion or management systems","CPC","Y02E70"),
 ("clean","Energy","Photovoltaic","CPC","Y02E10/50"),
 ("clean","Energy","Production of fuel of non-fossil origin","CPC","Y02E50"),
 ("clean","Energy","Sea","CPC","Y02E10/30"),
 ("clean","Energy","Solar thermal","CPC","Y02E10/40"),
 ("clean","Energy","Thermal-PV hybrid","CPC","Y02E10/60"),
 ("clean","Energy","Wind","CPC","Y02E10/70"),
 ("clean","Manufacturing","Agriculture","CPC","Y02P60"),
 ("clean","Manufacturing","Chemical","CPC","Y02P20;Y02P30;Y02P40"),
 ("clean","Manufacturing","Consumer products","CPC","Y02P70;Y02P80"),
 ("clean","Manufacturing","Enabling technologies","CPC","Y02P90"),
 ("clean","Manufacturing","Metal","CPC","Y02P10"),
 ("clean","Transport","Air","CPC","Y02T50"),
 ("clean","Transport","Electric and hybrid vehicles","CPC","Y02T10"),
 ("clean","Transport","Enabling technologies","CPC","Y02T90"),
 ("clean","Transport","Maritime","CPC","Y02T70"),
 ("clean","Transport","Railways","CPC","Y02T30"),
 ("clean","Other","Building","CPC","Y02B"),
 ("clean","Other","Carbon capture, storage and sequestration","CPC","Y02C"),
 ("clean","Other","ICT","CPC","Y02D"),
 ("clean","Other","Smart grid","CPC","Y04S"),
 ("clean","Other","Waste management","CPC","Y02W"),
 # ---- clean (IPC, transport; Aghion et al. 2016) ----
 ("clean","Transport","Electric","IPC","B60L11;B60L50;B60L53;B60L55;B60L58;B60L3;B60L15;B60K1;B60W10/08;B60W10/24;B60W10/26"),
 ("clean","Transport","Hybrid","IPC","B60K6;B60W20;B60L7/1;B60L7/20"),
 ("clean","Transport","Hydrogen fuel cell","IPC","B60W10/28;H01M8"),
 # ---- grey ----
 ("grey","Energy","Combustion technologies with mitigation potential","CPC","Y02E20"),
 ("grey","Manufacturing","Metal processing","CPC","Y02P10/20;Y02P10/25"),
 ("grey","Manufacturing","Chemical industry","CPC","Y02P20/129;Y02P20/143;Y02P20/15;Y02P20/20;Y02P20/30;Y02P20/40;Y02P20/50"),
 ("grey","Manufacturing","Oil refining and petrochemical industry","CPC","Y02P30/40"),
 ("grey","Manufacturing","Processing of minerals","CPC","Y02P40/121;Y02P40/50;Y02P40/57;Y02P40/60"),
 ("grey","Manufacturing","Production process for final industrial or consumer products","CPC","Y02P70/50;Y02P70/62"),
 ("grey","Manufacturing","Reducing waste and minimizing material use","CPC","Y02P80/30;Y02P80/40"),
 ("grey","Transport","Fuel efficiency of internal combustion engine-based vehicles","CPC","Y02T10/10;Y02T10/12;Y02T10/30;Y02T10/40"),
 ("grey","Transport","Fuel efficiency of internal combustion engine-based vehicles","IPC",
  "F02M39;F02M41;F02M43;F02M45;F02M47;F02M49;F02M51;F02M53;F02M55;F02M57;F02M59;F02M61;F02M63;F02M65;F02M67;F02M69;F02M71;F02M3/02;F02M3/04;F02M3/05;F02M23;F02M25;F02D41;F02B47/06"),
 # ---- dirty ----
 ("dirty","Energy","Upstream","CPC","B03B9/02;B03D2203/006;B63B35/4413;B63B2035/442;B63B2035/448;B63B75/00;C09K8;C10L5/04;E02B17;E02B2017;E21B;B03B9/005;B03B1;B03D2203/08;B61D11;E21C"),
 ("dirty","Energy","Processing and downstream","CPC","C10G;C10L1;C10K;C10L3/06;C10L3/08;C10L3/10;F25J3/0209;F25J3/0214;F25J3/061;C10F;C10L5/06;C10L5/08;C10L5/1;C10L5/2;C10L5/34;C10L5/36;C10L5/38;C10B;C10J1;C10J3;C01B3/2;C01B3/30;C01B3/32"),
 ("dirty","Energy","Transmission and distribution","CPC","B63B27/34;B63B27/24;B63B27/25;F17D;B63B25/08;B63B2025/08;B63B25/10;B63B25/12;B63B25/14;B63B25/16;B67D9;F25J1/0022;F25J1/0025;B63B2025/087;B63B25/04;B60P3/22;B60P3/24;B61D5;B61D3;B61D15;B61D49;B61D7;B61D9;B65G5;F17C2270/014;F17C2270/015;F17C2270/016;F17C2270/0163;E02D27/38;F17B1/26;F17C1;F17C3;F17C5;F17C7;F17C9;F17C2221/032;F17C2221/033;F17C2221/035;F17C2221/036;B65G3;G01M3/2892;G01M3/32;G01M3/34;F17C2265/06"),
 ("dirty","Manufacturing","Production of producer gas","IPC","C10J"),
 ("dirty","Manufacturing","Steam engine plants","IPC","F01K"),
 ("dirty","Manufacturing","Gas turbine plants","IPC","F02C"),
 ("dirty","Manufacturing","Hot gas plants","IPC","F02G"),
 ("dirty","Manufacturing","Steam generation","IPC","F22"),
 ("dirty","Manufacturing","Combustion apparatus","IPC","F23"),
 ("dirty","Manufacturing","Furnaces, kilns, ovens","IPC","F27"),
 ("dirty","Manufacturing","Internal combustion engine","IPC","F02B"),
 ("dirty","Transport","Internal combustion engine","IPC","F02B;F02D;F02F;F02M;F02N;F02P"),
]

root = Path(__file__).resolve().parents[1]
rows = []
for cat, sector, sub, system, codes in T:
    for c in dict.fromkeys(codes.split(";")):  # dedupe, keep order
        rows.append(dict(scheme="jee_srivastav", scheme_version="2023", category=cat, sector=sector,
                         subsector=sub, code=c, code_to="", code_system=system,
                         source="Jee & Srivastav (2023) Suppl. Table 1; lists as in Rozendaal (2024) Table E1"))
with open(root / "data/jee_srivastav/jee_srivastav.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
