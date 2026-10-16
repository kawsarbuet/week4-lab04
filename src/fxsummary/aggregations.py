from collections import defaultdict
from datetime import date
from typing import TypeAlias

from .models import Record

SummaryValue: TypeAlias = dict[str, object]


class Aggregation:
    def compute(self, records: list[Record]) -> SummaryValue:
        raise NotImplementedError


class MonthlyAverage(Aggregation):
    def compute(self, records: list[Record]) -> SummaryValue:
        grouped: dict[tuple[int, int], list[dict[str, float]]] = defaultdict(list)
        for rec in records:
            grouped[(rec.date.year, rec.date.month)].append(rec.rates)
        result: SummaryValue = {}
        for (year, month), maps in grouped.items():
            currencies = {cur for rate_map in maps for cur in rate_map}
            result[f"{year}-{month:02d}"] = {
                cur: sum(rate_map[cur] for rate_map in maps if cur in rate_map)
                / sum(cur in rate_map for rate_map in maps)
                for cur in sorted(currencies)
            }
        return result


class LargestSingleDayChange(Aggregation):
    def compute(self, records: list[Record]) -> SummaryValue:
        if not records:
            return {}
        ordered = sorted(records, key=lambda record: record.date)
        currencies = sorted({cur for record in records for cur in record.rates})
        result: SummaryValue = {
            cur: {"change": 0.0, "from": None, "to": None} for cur in currencies
        }
        best: dict[str, float] = {cur: 0.0 for cur in currencies}
        for previous, current in zip(ordered, ordered[1:]):
            for cur in currencies:
                if cur in previous.rates and cur in current.rates:
                    change = abs(current.rates[cur] - previous.rates[cur])
                    if change > best[cur]:
                        best[cur] = change
                        result[cur] = {
                            "change": change,
                            "from": previous.date.isoformat(),
                            "to": current.date.isoformat(),
                        }
        return result


class MonthWithMostMovement(Aggregation):
    def compute(self, records: list[Record]) -> SummaryValue:
        if not records:
            return {}
        ordered = sorted(records, key=lambda record: record.date)
        currencies = sorted({cur for record in records for cur in record.rates})
        changes: dict[date, dict[str, float]] = {
            record.date: {cur: 0.0 for cur in currencies} for record in ordered
        }
        for previous, current in zip(ordered, ordered[1:]):
            for cur in currencies:
                if cur in previous.rates and cur in current.rates:
                    changes[current.date][cur] = abs(
                        current.rates[cur] - previous.rates[cur]
                    )
        months = sorted({(record.date.year, record.date.month) for record in ordered})
        result: SummaryValue = {}
        for cur in currencies:
            totals = {
                month: sum(
                    changes[record.date][cur]
                    for record in ordered
                    if (record.date.year, record.date.month) == month
                )
                for month in months
            }
            # Choose earliest month for ties, including all-zero movements.
            best_month = max(months, key=lambda month: totals[month])
            result[cur] = {
                "month": f"{best_month[0]}-{best_month[1]:02d}",
                "movement": totals[best_month],
            }
        return result
