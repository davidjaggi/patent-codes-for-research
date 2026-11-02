"""Match patent classification codes against a scheme."""
from __future__ import annotations

from .expand import parse_code


def _sg(x: str | None) -> int:
    """Subgroup as comparable number: /72 < /7208 < /73 (right-pad to 6 digits)."""
    return int((x or "0").ljust(6, "0"))


def covers(scheme_code: str, patent_code: str, code_to: str | None = None) -> bool:
    """True if ``scheme_code`` (optionally a range to ``code_to``) covers ``patent_code``.

    Structural matching: subclass-level (``Y02B``) covers the whole subclass;
    main-group level (``Y02E30``) covers all its subgroups; a subgroup code
    (``Y02E10/70``) covers that subgroup and its sub-subgroups, which extend its
    digits (``Y02E10/7005``) - a heuristic, since the full CPC tree is not shipped. Ranges
    (``code_to``) compare subgroup numbers right-padded.
    """
    s, p = parse_code(scheme_code), parse_code(patent_code)
    if len(s["subclass"]) == 3:  # class-level scheme code, e.g. F22 covers F22B, F22D...
        return p["subclass"].startswith(s["subclass"])
    if s["subclass"] != p["subclass"]:
        return False
    if s["group"] is None:
        return True
    if code_to and s["subgroup"] is None:         # main-group range, e.g. F02M39-71
        t = parse_code(code_to)
        if t["subgroup"] is None and t["group"] and p["group"]:
            return int(s["group"]) <= int(p["group"]) <= int(t["group"])
    if s["group"] != p["group"]:
        return False
    if s["subgroup"] is None:
        return True
    if code_to:
        t = parse_code(code_to)
        return _sg(s["subgroup"]) <= _sg(p["subgroup"]) <= _sg(t["subgroup"])
    ss, ps = s["subgroup"], p["subgroup"] or ""
    # CPC sub-subgroups extend their parent's digits (/70 -> /7005, /7094; /15 -> /151), so a
    # subgroup code covers patent subgroups that start with it. Siblings (/72 vs /70) do not match.
    return ps.startswith(ss) if len(ss) >= 2 else ps == ss


def is_in_scheme(patent_code: str, scheme_df, category: str | None = None) -> bool:
    """Check a code against a loaded scheme DataFrame (optionally one category).

    Rows that are not plain codes/ranges (ENV-TECH ``code_type == 'complex'``, i.e. conditional
    combinations such as '[F17D5/02 and E03]') cannot be evaluated from one code and are skipped.
    """
    df = scheme_df if category is None else scheme_df[scheme_df["category"] == category]
    tos = df["code_to"] if "code_to" in df else [""] * len(df)
    for c, t in zip(df["code"], tos):
        try:
            if covers(c, patent_code, (t or None)):
                return True
        except ValueError:
            continue
    return False
