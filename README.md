# patent-codes-for-research

Patent classification code lists for "green"/"clean" technologies from the research literature, in a machine-readable format (tidy CSV + `schemes.json` metadata + a small Python loader).

| Scheme | File | Status | Source |
|---|---|---|---|
| OECD ENV-TECH | `data/envtech/envtech.csv` | complete (1,244 rows) | Haščič & Migotto (2015) |
| Jee & Srivastav clean / grey / dirty | `data/jee_srivastav/jee_srivastav.csv` | complete (191 rows) | Jee & Srivastav (2023), lists as in Rozendaal (2024) Table E1 |
| CPC Y02 / Y04S | `data/y02/y02_y04s.csv` | **partial**: subclasses + groups named in the papers | EPO CPC scheme |
| WIPO IPC Green Inventory | `data/ipc_green_inventory/ipc_gi.csv` | complete code list (958 unique codes), **no topic hierarchy** | WIPO, expanded by [S. Chen](https://github.com/shuangchenfinance/greenpatent) |

The full Y02/Y04S tree still needs to be generated from the official EPO/CPC release, and the IPC Green Inventory should be cross-checked against WIPO and enriched with its topic hierarchy (those hosts were not reachable when this repo was created). Per-scheme details are in `schemes.json`.

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
- Subclass-level lists (ENV-TECH, IPC Green Inventory, parts of Jee & Srivastav) can label entire subclasses green and produce false positives.
- Y02 tags change between CPC releases; record the release you use.
- Group titles in the partial Y02 file are paraphrased and should be checked against the official scheme.
- Jee & Srivastav lists are taken from Rozendaal's reproduction; verify against the published supplement before relying on them (Rozendaal lists `Y02P20/15` where the original refers to `Y02P20/151`).

## Rebuild / test
```bash
python scripts/build_envtech.py && python scripts/build_jee_srivastav.py && python scripts/build_y02.py
pytest
```

## Citing
See `CITATION.cff` (GitHub's "Cite this repository"). Please also cite the original papers for each scheme you use. Licence: MIT for the code and compilation; the underlying classifications belong to their publishers (OECD, EPO/USPTO, WIPO).
