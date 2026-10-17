# Part 9 - data processing with plain Python (list of dicts, logs, dates)

# %% cars_data
cars = [
    {"model": "C200", "type": "petrol",   "price": 48_000,  "year": 2021},
    {"model": "EQE",  "type": "electric", "price": 79_000,  "year": 2023},
    {"model": "E300", "type": "hybrid",   "price": 65_000,  "year": 2022},
    {"model": "EQS",  "type": "electric", "price": 110_000, "year": 2022},
    {"model": "A180", "type": "petrol",   "price": 34_000,  "year": 2020},
]

# %% filter_sort
electric = [c["model"] for c in cars if c["type"] == "electric"]
print(electric)

by_price = sorted(cars, key=lambda c: c["price"], reverse=True)
print([c["model"] for c in by_price[:3]])        # top 3 most expensive

newest = max(cars, key=lambda c: c["year"])
print(newest["model"])

# sort by type (A-Z), then by price (high -> low)
ordered = sorted(cars, key=lambda c: (c["type"], -c["price"]))
print([c["model"] for c in ordered])

# %% group_by
from collections import defaultdict

prices_by_type = defaultdict(list)
for c in cars:
    prices_by_type[c["type"]].append(c["price"])

avg_by_type = {t: sum(p) / len(p) for t, p in prices_by_type.items()}
print(avg_by_type)

count_by_type = {}
for c in cars:
    count_by_type[c["type"]] = count_by_type.get(c["type"], 0) + 1
print(count_by_type)

# %% parse_log
log = """\
2026-10-01 08:00:01,V001,speed=52
2026-10-01 08:00:02,V002,speed=n/a
2026-10-01 08:00:03,V001,speed=61
bad line
2026-10-01 08:00:04,V002,speed=47
"""


def parse_line(line):
    parts = line.split(",")
    if len(parts) != 3:
        return None
    timestamp, vehicle, field = parts
    try:
        return timestamp, vehicle, float(field.split("=")[1])
    except (IndexError, ValueError):
        return None


records = [r for r in map(parse_line, log.splitlines()) if r]
max_speed = {}
for _, vehicle, speed in records:
    max_speed[vehicle] = max(speed, max_speed.get(vehicle, speed))
print(len(records), "valid records")
print(max_speed)

# %% dates
from datetime import date, datetime, timedelta

start = datetime.strptime("2026-10-18 09:30", "%Y-%m-%d %H:%M")  # str->dt
end = start + timedelta(hours=2, minutes=15)
print(end.strftime("%d.%m.%Y %H:%M"))                             # dt->str
print((end - start).total_seconds() / 60, "minutes")

deadline = date(2026, 10, 18)
today = date(2026, 10, 17)
print((deadline - today).days, "day(s) left")
print(deadline.isoformat(), deadline.strftime("%A"), deadline.weekday())

# %% longest_streak
def longest_streak(values, threshold):
    """Longest run of consecutive values above threshold."""
    best = current = 0
    for v in values:
        current = current + 1 if v > threshold else 0
        best = max(best, current)
    return best


temps = [88, 92, 95, 91, 85, 97, 99, 101, 102, 80]
print(longest_streak(temps, 90))

# %% clean_data
raw = [" 12.5", "", None, "abc", "7", "-3", "1e2"]


def clean(values, low=0, high=100):
    cleaned = []
    for v in values:
        if v is None or not str(v).strip():
            continue                         # skip missing
        try:
            x = float(v)
        except ValueError:
            continue                         # skip not-a-number
        if low <= x <= high:                 # skip out-of-range
            cleaned.append(x)
    return cleaned


print(clean(raw))

# %% nested
order = {
    "id": 17,
    "customer": {"name": "Sara", "city": "Stuttgart"},
    "items": [{"part": "brake pad", "qty": 4, "price": 25.0},
              {"part": "oil filter", "qty": 1, "price": 12.5}],
}
total = sum(item["qty"] * item["price"] for item in order["items"])
print(order["customer"]["city"], total)
print(order.get("discount", {}).get("code", "none"))   # safe nested get
