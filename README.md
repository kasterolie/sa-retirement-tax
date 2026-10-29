# sa-retirement-tax

Small, dependency-free Python (3.11+) helpers for South African retirement fund calculations:

- **Lump sum tax**: SARS retirement and withdrawal lump sum tables, cumulative method (prior lump sums).
- **Late-payment interest**: annual compounding `amount × ((1+r)^(days/365) − 1)` and simple interest, plus a day counter from the 1st of the month after an exit date.
- **Business days**: SA public holidays (Public Holidays Act 36 of 1994: fixed dates, Good Friday, Family Day, Sunday → Monday), `is_business_day`, `next_business_day`.

```bash
pip install git+https://github.com/kasterolie/sa-retirement-tax
```

```python
from datetime import date
from sa_retirement_tax import (
    withdrawal_lump_sum_tax, retirement_lump_sum_tax,
    late_payment_interest, days_from_first_of_next_month, next_business_day,
)

retirement_lump_sum_tax(1_000_000, on=date(2026, 6, 1))                      # Decimal('101700.00')
withdrawal_lump_sum_tax(50_000, prior_lump_sums=100_000, on=date(2026, 6, 1))  # Decimal('9000.00')

days = days_from_first_of_next_month(date(2026, 3, 15), date(2026, 5, 1))    # 30
late_payment_interest(100_000, 0.10, days)                                   # Decimal('786.45')
next_business_day(date(2026, 4, 3))                                          # date(2026, 4, 7)
```

## Tax tables included

From the SARS page [Retirement Lump Sum Benefits](https://www.sars.gov.za/tax-rates/income-tax/retirement-lump-sum-benefits/), retrieved 2026-10-29, stored in `src/sa_retirement_tax/lump_sum_tables.json` keyed by effective date:

| Effective from | Tax years | Tables |
| --- | --- | --- |
| 2021-03-01 | 2022, 2023 | withdrawal, retirement/severance |
| 2023-03-01 | 2024 – 2027 (SARS: no changes since) | withdrawal, retirement/severance |

Dates before 1 March 2021 raise `ValueError`. Which prior benefits count toward `prior_lump_sums` (withdrawals since March 2009, retirement lump sums since October 2007, severance since March 2011) is described on the SARS page.

Ad-hoc presidential holidays (e.g. election days) aren't included; pass them via `extra=`.

## Disclaimer

Not tax, legal or financial advice. Figures may be out of date or wrong; always verify against [SARS](https://www.sars.gov.za/tax-rates/income-tax/retirement-lump-sum-benefits/) before use.

## License

MIT
