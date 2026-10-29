"""South African public holidays (Public Holidays Act 36 of 1994).

Ad-hoc holidays declared by the President (e.g. election days) are not
included; pass them via ``extra`` where needed.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta

FIXED = {
    (1, 1): "New Year's Day",
    (3, 21): "Human Rights Day",
    (4, 27): "Freedom Day",
    (5, 1): "Workers' Day",
    (6, 16): "Youth Day",
    (8, 9): "National Women's Day",
    (9, 24): "Heritage Day",
    (12, 16): "Day of Reconciliation",
    (12, 25): "Christmas Day",
    (12, 26): "Day of Goodwill",
}


def easter_sunday(year: int) -> date:
    """Western Easter Sunday (anonymous Gregorian algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7  # noqa: E741
    m = (a + 11 * h + 19 * l) // 433
    month = (h + l - 7 * m + 90) // 25
    day = (h + l - 7 * m + 33 * month + 19) % 32
    return date(year, month, day)


def public_holidays(year: int) -> dict[date, str]:
    """All public holidays for ``year``, including Sunday-to-Monday substitutes."""
    hol = {date(year, m, d): n for (m, d), n in FIXED.items()}
    easter = easter_sunday(year)
    hol[easter - timedelta(days=2)] = "Good Friday"
    hol[easter + timedelta(days=1)] = "Family Day"
    for d, name in sorted(hol.items()):
        if d.weekday() == 6:
            sub = d + timedelta(days=1)
            while sub in hol:
                sub += timedelta(days=1)
            hol[sub] = f"{name} (observed)"
    return dict(sorted(hol.items()))


def is_business_day(d: date, extra: Iterable[date] = ()) -> bool:
    return d.weekday() < 5 and d not in public_holidays(d.year) and d not in set(extra)


def next_business_day(d: date, extra: Iterable[date] = (), include_today: bool = True) -> date:
    """The first business day on or after ``d`` (strictly after if include_today=False)."""
    extra = set(extra)
    if not include_today:
        d += timedelta(days=1)
    while not is_business_day(d, extra):
        d += timedelta(days=1)
    return d
