"""Parsing, normalising and expanding patent classification codes (IPC/CPC)."""
from __future__ import annotations

import re

_ORIGIN = re.compile(r"^(?P<base>[A-HY]\d{2}[A-Z])(?P<a>\d+)-(?P<b>\d+)$")
_CODE = re.compile(r"^(?P<sub>[A-HY]\d{2}(?:[A-Z])?)(?:(?P<group>\d+)(?:/(?P<sub2>\d+))?)?$")


def normalise(code: str) -> str:
    """Strip whitespace; keep 'B01D53/34' style (no space before group)."""
    return re.sub(r"\s+", "", str(code)).upper()


def expand_code(code: str) -> list[str]:
    """Expand a short range into explicit codes.

    ``F02M39-71``    -> main-group range  F02M39, F02M40, ..., F02M71
    ``B01D53/34-72`` -> subgroup range    B01D53/34 ... B01D53/72
    Long subgroup ranges such as ``Y02T10/72-7291`` (CPC sub-subgroups, i.e. /72
    up to /7291) must NOT be expanded numerically; use :func:`split_range`.
    """
    c = normalise(code)
    if "/" in c and "-" in c:
        base, rest = c.split("/", 1)
        pre, end = rest.split("-", 1)
        if len(pre) <= 2 and len(end) <= 2 and pre.isdigit() and end.isdigit():
            a, b = int(pre), int(end)
            if a > b:
                raise ValueError(f"descending range: {code}")
            return [f"{base}/{str(i).zfill(2)}" for i in range(a, b + 1)]
        return [c]
    m = _ORIGIN.match(c)
    if m:
        a, b = int(m.group("a")), int(m.group("b"))
        if a > b:
            raise ValueError(f"descending range: {code}")
        return [f"{m.group('base')}{i}" for i in range(a, b + 1)]
    return [c]


def split_range(code: str) -> tuple[str, str | None]:
    """'Y02T10/72-7291' -> ('Y02T10/72', 'Y02T10/7291'); plain codes -> (code, None)."""
    c = normalise(code)
    if "/" in c and "-" in c:
        base, rest = c.split("/", 1)
        pre, end = rest.split("-", 1)
        return f"{base}/{pre}", f"{base}/{end}"
    return c, None


def split_codes(raw: str) -> list[str]:
    """Split a free-text cell such as 'Y02E 10/10; Y02E 30' into raw codes."""
    if raw is None or (isinstance(raw, float)):
        return []
    return [p.strip() for p in re.split(r"[;,\n]", str(raw)) if p.strip()]


def parse_code(code: str) -> dict:
    """Return {'subclass', 'group', 'subgroup'}; class-level codes (F22) keep the class in 'subclass'."""
    m = _CODE.match(normalise(code))
    if not m:
        raise ValueError(f"unparseable code: {code!r}")
    return {"subclass": m.group("sub"), "group": m.group("group"), "subgroup": m.group("sub2")}
