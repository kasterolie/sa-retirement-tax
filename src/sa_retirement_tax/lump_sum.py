"""SARS retirement fund lump sum tax tables (cumulative method).

Source: https://www.sars.gov.za/tax-rates/income-tax/retirement-lump-sum-benefits/
"""

from __future__ import annotations

import json
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from functools import cache
from importlib import resources


@cache
def _tables() -> dict:
    return json.loads(resources.files(__package__).joinpath("lump_sum_tables.json").read_text())


def _table_for(kind: str, on: date) -> list:
    tables = _tables()[kind]
    keys = sorted(k for k in tables if date.fromisoformat(k) <= on)
    if not keys:
        raise ValueError(f"No {kind} table available for {on.isoformat()}")
    return tables[keys[-1]]


def _apply(table: list, amount: Decimal) -> Decimal:
    if amount <= 0:
        return Decimal(0)
    tax = Decimal(0)
    for threshold, base, rate in table:
        if amount > threshold:
            tax = Decimal(base) + (amount - Decimal(threshold)) * Decimal(str(rate))
    return tax.quantize(Decimal("0.01"), ROUND_HALF_UP)


def _cumulative(kind: str, amount, prior, on: date) -> Decimal:
    amount, prior = Decimal(str(amount)), Decimal(str(prior))
    if amount < 0 or prior < 0:
        raise ValueError("Amounts must be non-negative")
    table = _table_for(kind, on)
    return _apply(table, prior + amount) - _apply(table, prior)


def withdrawal_lump_sum_tax(amount, prior_lump_sums=0, on: date | None = None) -> Decimal:
    """Tax on a withdrawal (pre-retirement) lump sum.

    ``prior_lump_sums`` is the aggregate of earlier lump sums that SARS requires
    to be taken into account (see the SARS page for which benefits qualify).
    """
    return _cumulative("withdrawal", amount, prior_lump_sums, on or date.today())


def retirement_lump_sum_tax(amount, prior_lump_sums=0, on: date | None = None) -> Decimal:
    """Tax on a retirement fund lump sum benefit or severance benefit."""
    return _cumulative("retirement", amount, prior_lump_sums, on or date.today())
