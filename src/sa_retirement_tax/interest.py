"""Generic late-payment interest helpers."""

from __future__ import annotations

from datetime import date
from decimal import ROUND_HALF_UP, Decimal


def _q(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), ROUND_HALF_UP)


def late_payment_interest(amount, annual_rate, days: int) -> Decimal:
    """Interest compounded annually: amount * ((1 + r) ** (days / 365) - 1)."""
    if days <= 0:
        return Decimal("0.00")
    factor = (1 + float(annual_rate)) ** (days / 365) - 1
    return _q(Decimal(str(amount)) * Decimal(repr(factor)))


def simple_interest(amount, annual_rate, days: int) -> Decimal:
    """Simple interest: amount * r * days / 365."""
    if days <= 0:
        return Decimal("0.00")
    return _q(Decimal(str(amount)) * Decimal(str(annual_rate)) * days / 365)


def first_of_next_month(d: date) -> date:
    return date(d.year + 1, 1, 1) if d.month == 12 else date(d.year, d.month + 1, 1)


def days_from_first_of_next_month(exit_date: date, payment_date: date) -> int:
    """Days from the 1st of the month after ``exit_date`` to ``payment_date`` (min 0)."""
    return max(0, (payment_date - first_of_next_month(exit_date)).days)
