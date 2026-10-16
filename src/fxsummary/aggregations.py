from collections import defaultdict


class Aggregation:
    def compute(self, records):
        raise NotImplementedError

class MonthlyAverage(Aggregation):
    def compute(self, records):
        grouped = defaultdict(list)

        for rec in records:
            key = (rec.date.year, rec.date.month)
            grouped[key].append(rec.rates)

        monthly_avgs = {}

        for key, maps in grouped.items():
            currencies = {cur for m in maps for cur in m.keys()}

            avg_map = {}
            for cur in currencies:
                values = [m[cur] for m in maps if cur in m]
                if values:
                    avg_map[cur] = sum(values) / len(values)

            month_key = f"{key[0]}-{key[1]:02d}"
            monthly_avgs[month_key] = avg_map

        return monthly_avgs

class LargestSingleDayChange(Aggregation):
    def compute(self, records):
        if not records:
            return {}

        records_sorted = sorted(records, key=lambda r: r.date)
        currencies = {cur for r in records for cur in r.rates.keys()}

        result = {cur: {"change": 0.0, "from": None, "to": None} for cur in currencies}

        for i in range(1, len(records_sorted)):
            prev = records_sorted[i - 1]
            curr = records_sorted[i]

            for cur in currencies:
                if cur in prev.rates and cur in curr.rates:
                    change = abs(curr.rates[cur] - prev.rates[cur])
                    if change > result[cur]["change"]:
                        result[cur] = {
                            "change": change,
                            "from": prev.date.isoformat(),
                            "to": curr.date.isoformat(),
                        }

        return result

class MonthWithMostMovement(Aggregation):
    def compute(self, records):
        if not records:
            return {}

        records_sorted = sorted(records, key=lambda r: r.date)
        currencies = {cur for r in records for cur in r.rates.keys()}

        daily_changes = {r.date: {cur: 0.0 for cur in currencies} for r in records_sorted}

        for i in range(1, len(records_sorted)):
            prev = records_sorted[i - 1]
            curr = records_sorted[i]

            for cur in currencies:
                if cur in prev.rates and cur in curr.rates:
                    daily_changes[curr.date][cur] = abs(curr.rates[cur] - prev.rates[cur])

        grouped = defaultdict(list)
        for r in records_sorted:
            key = (r.date.year, r.date.month)
            grouped[key].append(r.date)

        result = {}

        for cur in currencies:
            best_month = None
            best_total = 0.0

            for key, dlist in grouped.items():
                total = sum(daily_changes[d][cur] for d in dlist)
                if total > best_total:
                    best_total = total
                    best_month = key

            month_str = f"{best_month[0]}-{best_month[1]:02d}"
            result[cur] = {"month": month_str, "movement": best_total}

        return result
