# Part 12 - mock live-coding tasks with full solutions

# %% mock_tracker
from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    owner: str
    hours: float
    due: date
    done: bool = False


class TaskTracker:
    def __init__(self):
        self._tasks = {}                     # title -> Task

    def add(self, title, owner, hours, due):
        if title in self._tasks:
            raise ValueError(f"task {title!r} already exists")
        if hours <= 0:
            raise ValueError("hours must be positive")
        self._tasks[title] = Task(title, owner, hours, due)

    def complete(self, title):
        if title not in self._tasks:
            raise KeyError(f"unknown task {title!r}")
        self._tasks[title].done = True

    def open_tasks(self):
        return [t for t in self._tasks.values() if not t.done]

    def overdue(self, today):
        late = [t for t in self.open_tasks() if t.due < today]
        return sorted(late, key=lambda t: t.due)

    def workload(self):
        load = {}
        for t in self.open_tasks():
            load[t.owner] = load.get(t.owner, 0) + t.hours
        return dict(sorted(load.items(), key=lambda kv: -kv[1]))


tracker = TaskTracker()
tracker.add("Spec", "Ali", 8, date(2026, 10, 10))
tracker.add("Build", "Ali", 40, date(2026, 10, 30))
tracker.add("Test", "Mia", 16, date(2026, 10, 12))
tracker.add("Docs", "Sara", 4, date(2026, 10, 20))
tracker.complete("Spec")

today = date(2026, 10, 17)
print([t.title for t in tracker.overdue(today)])
print(tracker.workload())

# %% mock_sensor
readings = [21.5, 22.0, None, 23.1, 85.0, 24.2, None, 25.0, 26.4, 27.9]


def summarize(values, limit=25.0, max_valid=60.0):
    valid = [v for v in values if v is not None and v <= max_valid]
    if not valid:
        return {}
    return {
        "count": len(valid),
        "dropped": len(values) - len(valid),
        "min": min(valid),
        "max": max(valid),
        "avg": round(sum(valid) / len(valid), 2),
        "above_limit": sum(1 for v in valid if v > limit),
    }


print(summarize(readings))
print(summarize([None, None]))

# %% mock_meetings
def to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def to_hhmm(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def merge_meetings(meetings):
    """[('09:00', '10:00'), ...] -> merged busy blocks."""
    intervals = sorted((to_minutes(s), to_minutes(e)) for s, e in meetings)
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:        # overlaps last block
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(to_hhmm(s), to_hhmm(e)) for s, e in merged]


meetings = [("09:00", "10:00"), ("09:30", "11:00"),
            ("13:00", "13:30"), ("11:00", "11:15")]
print(merge_meetings(meetings))

# %% mock_orders
import csv
import io
from collections import defaultdict

data = """order_id,part,qty,unit_price
1,brake pad,4,25.00
2,oil filter,2,12.50
3,brake pad,2,25.00
4,wiper,x,9.99
5,spark plug,8,7.25
"""

revenue = defaultdict(float)
skipped = 0
for row in csv.DictReader(io.StringIO(data)):    # or open("orders.csv")
    try:
        revenue[row["part"]] += int(row["qty"]) * float(row["unit_price"])
    except ValueError:
        skipped += 1

top = sorted(revenue.items(), key=lambda kv: kv[1], reverse=True)[:2]
print(top, "skipped:", skipped)

# %% mock_charging
from datetime import datetime

FMT = "%Y-%m-%d %H:%M"


def charging_cost(start, end, kwh, price_per_kwh=0.59,
                  fee_per_min=0.10, free_minutes=240):
    """Energy cost + blocking fee after free_minutes."""
    minutes = (datetime.strptime(end, FMT)
               - datetime.strptime(start, FMT)).total_seconds() / 60
    if minutes < 0 or kwh < 0:
        raise ValueError("invalid session")
    blocking = max(0, minutes - free_minutes) * fee_per_min
    return round(kwh * price_per_kwh + blocking, 2)


print(charging_cost("2026-10-17 08:00", "2026-10-17 11:00", 45))
print(charging_cost("2026-10-17 08:00", "2026-10-17 13:30", 60))

# %% worked_example
def top_n_trips(trips, n=3):
    """Return the n longest trips as (driver, km), longest first."""
    if n <= 0:
        return []
    return sorted(trips, key=lambda t: t[1], reverse=True)[:n]


trips = [("Ali", 12.5), ("Sara", 40.0), ("Mia", 7.2), ("Tom", 40.0)]
assert top_n_trips(trips, 2) == [("Sara", 40.0), ("Tom", 40.0)]
assert top_n_trips([], 3) == []
assert top_n_trips(trips, 0) == []
print(top_n_trips(trips))
