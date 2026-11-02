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
    (``Y02E10/10``) covers that subgroup and, because CPC subgroups are
    numbered hierarchically, sub-subgroups sharing its digits (``Y02E10/10x``
    only if ``code_to`` says so). Ranges compare subgroup numbers right-padded.
    """
    s, p = parse_code(scheme_code), parse_code(patent_code)
    if len(s["subclass"]) == 3:  # class-level scheme code, e.g. F22 covers F22B, F22D...
        return p["subclass"].startswith(s["subclass"])
    if s["subclass"] != p["subclass"]:
        return False
    if s["group"] is None:
        return True
    if s["group"] != p["group"]:
        return False
    if s["subgroup"] is None:
        return True
    if code_to:
        t = parse_code(code_to)
        return _sg(s["subgroup"]) <= _sg(p["subgroup"]) <= _sg(t["subgroup"])
    return _sg(s["subgroup"]) == _sg(p["subgroup"])


def is_in_scheme(patent_code: str, scheme_df, category: str | None = None) -> bool:
    """Check a code against a loaded scheme DataFrame (optionally one category)."""
    df = scheme_df if category is None else scheme_df[scheme_df["category"] == category]
    return any(covers(c, patent_code, (t or None))
               for c, t in zip(df["code"], df.get("code_to", [""] * len(df))))
