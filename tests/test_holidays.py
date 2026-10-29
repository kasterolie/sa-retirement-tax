from datetime import date

from sa_retirement_tax import is_business_day, next_business_day, public_holidays
from sa_retirement_tax.holidays import easter_sunday


def test_easter():
    assert easter_sunday(2026) == date(2026, 4, 5)
    assert easter_sunday(2025) == date(2025, 4, 20)
    assert easter_sunday(2024) == date(2024, 3, 31)


def test_2026_easter_holidays():
    h = public_holidays(2026)
    assert h[date(2026, 4, 3)] == "Good Friday"
    assert h[date(2026, 4, 6)] == "Family Day"


def test_sunday_moves_to_monday():
    # 16 Jun 2024 was a Sunday
    assert date(2024, 6, 17) in public_holidays(2024)
    # Christmas 2022 Sunday -> 26th already Goodwill -> 27th observed
    assert public_holidays(2022)[date(2022, 12, 27)].endswith("(observed)")


def test_count_2026():
    # 2026: Heritage? no Sunday clashes except 9 Aug (Sun) -> 10 Aug
    h = public_holidays(2026)
    assert date(2026, 8, 10) in h
    assert len(h) == 13


def test_business_days():
    assert not is_business_day(date(2026, 4, 3))
    assert not is_business_day(date(2026, 4, 4))
    assert is_business_day(date(2026, 4, 7))
    assert next_business_day(date(2026, 4, 3)) == date(2026, 4, 7)
    assert next_business_day(date(2026, 4, 7)) == date(2026, 4, 7)
    assert next_business_day(date(2026, 4, 7), include_today=False) == date(2026, 4, 8)
    assert next_business_day(date(2026, 4, 8), extra=[date(2026, 4, 8)]) == date(2026, 4, 9)
