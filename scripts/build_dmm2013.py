"""data/dechezlepretre_martin_mohnen/dmm2013.csv

Source: Dechezleprêtre, A., Martin, R., Mohnen, M. (2013). Knowledge spillovers from clean and dirty
technologies: a patent citation analysis. CCCEP WP 151 / Grantham Research Institute WP 135 (LSE), Figure 2
"Patent classification codes by sector and type of technology". Transcribed by hand from the PDF (the
printed table is a three-column figure). Printed typo 'B06K 6' is corrected to B60K6. 'Less dirty' in the
paper = 'grey' (efficiency-improving dirty technologies). 'E02B' appears in the printed energy-dirty column
under the label 'Hydraulic Engineering' and is kept as printed. The paper notes Y02E20/10 as '(not used)'.
Ranges: F02M39-71, F02M3/02-05, F03B13/10-26 are kept as code/code_to.
"""
import csv
from pathlib import Path

# (category, sector, code, code_to, description)
R = [
 ("clean","car","B60K1","","Arrangement or mounting of electrical propulsion units"),
 ("clean","car","B60K6","","Arrangement or mounting of hybrid propulsion systems comprising electric motors and internal combustion engines"),
 ("clean","car","B60L3","","Electric devices on electrically-propelled vehicles for safety purposes; monitoring operating variables"),
 ("clean","car","B60L7","","Dynamic electric regenerative braking"),
 ("clean","car","B60L11","","Electric propulsion with power supplied within the vehicle"),
 ("clean","car","B60L15","","Methods, circuits or devices for controlling the traction-motor speed of electrically-propelled vehicles"),
 ("clean","car","B60R16","","Electric or fluid circuits specially adapted for vehicles and not otherwise provided for"),
 ("clean","car","B60S5","","Supplying batteries to, or removing batteries from, vehicles"),
 ("clean","car","B60W10","","Conjoint control of vehicle sub-units of different type or different function"),
 ("clean","car","B60W20","","Control systems specially adapted for hybrid vehicles"),
 ("clean","car","H01M","","Fuel cells"),
 ("grey","car","F02M39","F02M71","Fuel injection apparatus"),
 ("grey","car","F02M3/02","F02M3/05","Idling devices for carburettors preventing flow of idling fuel"),
 ("grey","car","F02M23","","Apparatus for adding secondary air to fuel-air mixture"),
 ("grey","car","F02M25","","Engine-pertinent apparatus for adding non-fuel substances or small quantities of secondary fuel"),
 ("grey","car","F02D41","","Electrical control of supply of combustible mixture or its constituents"),
 ("grey","car","F02B47/06","","Methods of operating engines involving adding non-fuel substances or anti-knock agents"),
 ("dirty","car","F02B","","Internal-combustion piston engines; combustion engines in general"),
 ("dirty","car","F02D","","Controlling combustion engines"),
 ("dirty","car","F02F","","Cylinders, pistons or casings for combustion engines; arrangement of sealings"),
 ("dirty","car","F02M","","Supplying combustion engines with combustible mixtures or constituents thereof"),
 ("dirty","car","F02N","","Starting of combustion engines"),
 ("dirty","car","F02P","","Ignition (other than compression ignition) for internal-combustion engines"),
 ("clean","fuel","Y02E50","","Technologies for the production of fuel of non-fossil origin"),
 ("dirty","fuel","C10G1","","Production of liquid hydrocarbon mixtures from oil-shale, oil-sand or non-melting solid carbonaceous materials"),
 ("dirty","fuel","C10L1","","Fuel"),
 ("clean","energy","Y02E10","","Energy generation through renewable energy sources"),
 ("clean","energy","Y02E30","","Energy generation of nuclear origin"),
 ("clean","energy","E02B9/08","","Tide or wave power plants"),
 ("clean","energy","F03B13/10","F03B13/26","Submerged units incorporating electric generators or motors characterised by using wave or tide energy"),
 ("clean","energy","F03D","","Wind motors"),
 ("clean","energy","F03G4","","Devices for producing mechanical power from geothermal energy"),
 ("clean","energy","F03G6","","Devices for producing mechanical power from solar energy"),
 ("clean","energy","F03G7/05","","Ocean thermal energy conversion"),
 ("clean","energy","F24J2","","Use of solar heat, e.g. solar heat collectors"),
 ("clean","energy","F24J3/08","","Production or use of heat, not derived from combustion, using geothermal heat"),
 ("clean","energy","F26B3/28","","Drying solid materials or objects by application of heat by radiation, e.g. from the sun"),
 ("grey","energy","Y02E20/10","","Combined combustion (not used)"),
 ("grey","energy","Y02E20/12","","Heat utilisation in combustion or incineration of waste"),
 ("grey","energy","Y02E20/14","","Combined heat and power generation"),
 ("grey","energy","Y02E20/16","","Combined cycle power plant, or combined cycle gas turbine"),
 ("grey","energy","Y02E20/18","","Integrated gasification combined cycle"),
 ("grey","energy","Y02E20/30","","Technologies for a more efficient combustion or heat usage"),
 ("grey","energy","Y02E20/32","","Direct CO2 mitigation"),
 ("grey","energy","Y02E20/34","","Indirect CO2 mitigation, by acting on non-CO2 directly related matters of the process, more efficient use of fuels"),
 ("grey","energy","Y02E20/36","","Heat recovery other than air pre-heating"),
 ("dirty","energy","C10J","","Production of fuel gases by carburetting air or other gases without pyrolysis"),
 ("dirty","energy","E02B","","Hydraulic engineering (as printed)"),
 ("dirty","energy","F01K","","Steam engine plants; steam accumulators; engine plants not otherwise provided for; engines using special working fluids or cycles"),
 ("dirty","energy","F02C","","Gas-turbine plants; air intakes for jet-propulsion plants; controlling fuel supply in air-breathing jet-propulsion plants"),
 ("dirty","energy","F22","","Steam generation"),
 ("dirty","energy","F23","","Combustion apparatus; combustion processes"),
 ("dirty","energy","F24J","","Production or use of heat not otherwise provided for"),
 ("dirty","energy","F27","","Furnaces; kilns; ovens; retorts"),
 ("dirty","energy","F28","","Heat exchange in general"),
 ("clean","lighting","H01J61","","Gas- or vapour-discharge lamps (compact fluorescent lamp)"),
 ("clean","lighting","H05B33","","Electroluminescent light sources (LED)"),
 ("clean","lighting","F21K9","","Electric lamps using semiconductor devices as light generating elements, e.g. LED"),
 ("dirty","lighting","F21H","","Incandescent lamp"),
]
SRC = "Dechezleprêtre, Martin & Mohnen (2013), Grantham RI WP 135, Figure 2"
root = Path(__file__).resolve().parents[1]
rows = [dict(scheme="dechezlepretre_martin_mohnen", scheme_version="WP-2013", category=c, sector=s, code=k, code_to=t,
             code_system="CPC" if k.startswith("Y02") else "IPC/CPC", description=d, source=SRC) for c, s, k, t, d in R]
with open(root / "data/dechezlepretre_martin_mohnen/dmm2013.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
