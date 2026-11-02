# patent-codes-for-research

Patent classification code lists for "green"/"clean" technologies from the research literature, in a machine-readable format (tidy CSV + `schemes.json` metadata + a small Python loader).

| Scheme | File | Status | Source |
|---|---|---|---|
| OECD ENV-TECH | `data/envtech/envtech.csv` | complete (1,246 rows), checked against the paper's annex | Haščič & Migotto (2015) |
| Jee & Srivastav clean / grey / dirty | `data/jee_srivastav/jee_srivastav.csv` | complete (191 rows) | Jee & Srivastav (2023), lists as in Rozendaal (2024) Table E1 |
| CPC Y02 / Y04S | `data/y02/y02_y04s.csv` | complete at top level (9 subclasses, each covers everything below; EPO status Dec 2021) | EPO CPC scheme |
| Dechezleprêtre, Martin & Mohnen (2013) | `data/dechezlepretre_martin_mohnen/dmm2013.csv` | complete, hand-transcribed (59 rows; car, fuel, energy, lighting; clean/grey/dirty) | CCCEP WP 151 |
| Dechezleprêtre, Muckley & Neelakantan (2021) | `data/dechezlepretre_muckley_neelakantan/dmn2021.csv` | complete (30 rows; clean/dirty) | Springer 2021, the paper Jee & Srivastav cite |
| Popp, Pless, Haščič & Johnstone | `data/popp_2019/popp2019.csv` | complete (25 rows; clean energy, enabling, hydrofracturing; CPC) | NBER chapter draft Dec 2019 (published 2022) |
| Aghion et al. (2016, JPE) | `data/aghion_2016/aghion2016.csv` | complete (26 rows; auto IPC, clean/dirty/grey), original source of the Jee & Srivastav transport lists | J. Political Economy 124(1) |
| Aghion, Bénabou, Martin & Roulet (2020/2023) | `data/aghion_benabou_martin_roulet/abmr2021.csv` | complete (11 rows; auto sector, CPC) | NBER WP 26921 / AER: Insights 2023 |
| OECD ENV-TECH, expanded | `data/envtech/envtech_expanded.csv` | complete (3,150 unique codes) | Haščič & Migotto (2015), expanded by Favot et al. (2023) |
| WIPO IPC Green Inventory | `data/ipc_green_inventory/ipc_gi.csv` | complete (1,214 codes, 170 topics with hierarchy) | WIPO 2022 list, expanded by Favot et al. (2023) |

Y02/Y04S is stored as the nine top-level subclasses; `covers("Y02B", code)` matches every group beneath, so no deeper tree is needed to flag tagged patents. The IPC Green Inventory and expanded ENV-TECH come from the replication package of Favot et al. (2023), whose methodology compares exactly these three schemes (ENV-TECH, IPC Green Inventory, Y02/Y04S). Per-scheme details are in `schemes.json`.

## Columns
Common: `scheme, scheme_version, code, code_to, code_system, source`. ENV-TECH adds `level_1..3, description, code_raw, code_type` (`code` | `range` | `complex`); Jee & Srivastav adds `category` (clean/grey/dirty), `sector`, `subsector`; Y02 adds `parent, level, title`.

- Codes are written without spaces (`Y02E10/10`, `B60L3`). A code covers everything below it: `Y02B` = whole subclass, `B60L3` = group 3 only (not `B60L30`).
- `code_to` is set for CPC subgroup ranges such as `Y02T10/72`–`Y02T10/7291`; these are **not** expanded numerically.

## Usage
```bash
pip install -e .
```
```python
import patentcodes as pc
js = pc.load("jee_srivastav")
pc.is_in_scheme("Y02E10/70", js, "clean")   # True
pc.expand_code("F02M39-41")                 # ['F02M39', 'F02M40', 'F02M41']
```

## Caveats
- Matching is structural: a subgroup code also covers its sub-subgroups (`Y02E10/70` covers `Y02E10/7005`, not the sibling `/72`); this is a digit-prefix heuristic because the full CPC tree is not shipped.
- Jee & Srivastav's dirty manufacturing list is confirmed by Dechezleprêtre, Muckley & Neelakantan (2021) (same eight codes). The Aghion, Bénabou, Martin & Roulet paper (2020 NBER / 2023 AER: Insights) is a different paper from Aghion et al. (2016, *JPE*), which is also included.
- Subclass-level lists (ENV-TECH, IPC Green Inventory, parts of Jee & Srivastav) can label entire subclasses green and produce false positives.
- Y02 tags change between CPC releases; record the release you use.
- Jee & Srivastav lists are taken from Rozendaal's reproduction; verify against the published supplement before relying on them (Rozendaal lists `Y02P20/15` where the original refers to `Y02P20/151`).

## Rebuild / test
```bash
python scripts/build_envtech.py && python scripts/build_jee_srivastav.py && python scripts/build_y02.py
pytest
```

## Citing
See `CITATION.cff` (GitHub's "Cite this repository") for citing this repository. Please also cite the original paper of each scheme you use; the full source references are in `schemes.json`. Licence: MIT for the code and compilation; the underlying classifications belong to their publishers (OECD, EPO/USPTO, WIPO).

## Attribution
`raw/favot2023/` and the files derived from it are from Favot et al. (2023), CC-BY-4.0 - cite the paper when using `ipc_gi.csv` or `envtech_expanded.csv`. S. Chen's [greenpatent](https://github.com/shuangchenfinance/greenpatent) was used as a cross-check of the IPC list (see `schemes.json`).
