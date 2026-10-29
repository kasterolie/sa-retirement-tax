from datetime import date
from decimal import Decimal

from sa_retirement_tax import days_from_first_of_next_month, late_payment_interest, simple_interest


def test_compound_30_days():
    # 100000 * (1.10 ** (30/365) - 1) = 786.45
    assert late_payment_interest(100000, 0.10, 30) == Decimal("786.45")


def test_compound_full_year():
    assert late_payment_interest(100000, 0.10, 365) == Decimal("10000.00")


def test_simple_30_days():
    assert simple_interest(100000, 0.10, 30) == Decimal("821.92")


def test_zero_days():
    assert late_payment_interest(1000, 0.1, 0) == Decimal("0.00")
    assert simple_interest(1000, 0.1, -5) == Decimal("0.00")


def test_days_helper():
    assert days_from_first_of_next_month(date(2026, 3, 15), date(2026, 5, 1)) == 30
    assert days_from_first_of_next_month(date(2026, 12, 31), date(2027, 1, 31)) == 30
    assert days_from_first_of_next_month(date(2026, 3, 15), date(2026, 3, 20)) == 0
