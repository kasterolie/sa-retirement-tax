from datetime import date
from decimal import Decimal

import pytest

from sa_retirement_tax import retirement_lump_sum_tax, withdrawal_lump_sum_tax

D27 = date(2026, 6, 1)
D23 = date(2022, 6, 1)


@pytest.mark.parametrize("amt,exp", [(27500, "0"), (100000, "13050"), (726000, "125730"),
                                     (1089000, "223740"), (1200000, "263700")])
def test_withdrawal_2027(amt, exp):
    assert withdrawal_lump_sum_tax(amt, on=D27) == Decimal(exp)


@pytest.mark.parametrize("amt,exp", [(550000, "0"), (600000, "9000"), (770000, "39600"),
                                     (1000000, "101700"), (1155000, "143550"), (1255000, "179550")])
def test_retirement_2027(amt, exp):
    assert retirement_lump_sum_tax(amt, on=D27) == Decimal(exp)


def test_older_tables():
    assert withdrawal_lump_sum_tax(100000, on=D23) == Decimal("13500")
    assert retirement_lump_sum_tax(600000, on=D23) == Decimal("18000")


def test_cumulative_prior():
    # 300k prior + 500k = 800k: 39600 + 27% x 30000 = 47700, less tax on 300k (0)
    assert retirement_lump_sum_tax(500000, prior_lump_sums=300000, on=D27) == Decimal("47700")
    assert withdrawal_lump_sum_tax(50000, prior_lump_sums=100000, on=D27) == Decimal("9000")


def test_errors():
    with pytest.raises(ValueError):
        withdrawal_lump_sum_tax(1000, on=date(2010, 1, 1))
    with pytest.raises(ValueError):
        withdrawal_lump_sum_tax(-1, on=D27)
