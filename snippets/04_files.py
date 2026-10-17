# Part 5 - files: text, CSV, JSON (the build runs this in a temp folder)

# %% text_file
with open("notes.txt", "w", encoding="utf-8") as f:     # "w" overwrites
    f.write("first line\nsecond line\n")

with open("notes.txt", "a", encoding="utf-8") as f:     # "a" appends
    f.write("third line\n")

with open("notes.txt", encoding="utf-8") as f:          # "r" is default
    for number, line in enumerate(f, start=1):
        print(number, line.strip())                     # strip the "\n"

# %% csv_file
import csv

rows = [{"model": "C200", "price": "48000"},
        {"model": "EQS", "price": "109990"}]
with open("cars.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["model", "price"])
    writer.writeheader()
    writer.writerows(rows)

with open("cars.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):            # each row is a dict
        print(row["model"], float(row["price"]))    # values are str!

# %% json_file
import json

data = {"model": "EQS", "options": ["AMG Line", "Pano roof"], "km": 1200}
with open("car.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)             # dict -> file

with open("car.json", encoding="utf-8") as f:
    loaded = json.load(f)                    # file -> dict
print(loaded["options"][0])

print(json.dumps({"a": 1, "ok": True}))      # dict -> str
print(json.loads('{"speed": 120}')["speed"]) # str -> dict

# %% pathlib
from pathlib import Path

p = Path("notes.txt")
print(p.exists(), p.suffix, p.stem)
print(p.read_text(encoding="utf-8").splitlines())
print(sorted(f.name for f in Path(".").glob("*.csv")))
