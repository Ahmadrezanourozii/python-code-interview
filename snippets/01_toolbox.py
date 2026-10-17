# Part 2 - Python toolbox (cheat sheet). Run: python3 snippets/01_toolbox.py

# %% str_methods annotate
s = "  Mercedes-Benz EQS  "
s.strip()
s.strip().lower()
s.strip().replace("-", " ")
s.split()
"a,b,,c".split(",")
"-".join(["2026", "10", "18"])
"EQS 580".startswith("EQ")
"EQS 580".find("580")
"EQS 580".find("x")
"banana".count("a")
"hello world".title()
"abc123".isalnum(), "123".isdigit(), "abc".isalpha()

# %% fstrings annotate
model, price, km = "EQS", 109990.5, 12345
f"{model} costs {price:,.2f} EUR"
f"{km:>8}|"
f"{km:<8}|"
f"{0.4567:.1%}"
f"{7:03d}"
f"{model=}"

# %% slicing annotate
s = "Python"
s[0], s[-1]
s[1:4]
s[:2], s[2:]
s[::-1]
s[::2]
nums = [10, 20, 30, 40, 50]
nums[-2:]
nums[1:-1]

# %% list_methods annotate
cars = ["C", "E", "S"]
cars.append("G")
cars.insert(0, "A")
cars
cars.extend(["EQA", "EQB"])
cars.pop()
cars.pop(0)
cars.remove("E")
cars
"S" in cars
cars.index("S")
len(cars), cars.count("C")

# %% sorting annotate
nums = [5, 2, 9, 1]
sorted(nums)
sorted(nums, reverse=True)
nums
nums.sort()
nums
words = ["banana", "apple", "Fig"]
sorted(words)
sorted(words, key=str.lower)
sorted(words, key=len)
cars = [("EQS", 2022), ("C", 2014), ("GLE", 2019)]
sorted(cars, key=lambda c: c[1])
max(cars, key=lambda c: c[1])

# %% comprehensions annotate
nums = [1, 2, 3, 4, 5, 6]
[n * n for n in nums]
[n for n in nums if n % 2 == 0]
["even" if n % 2 == 0 else "odd" for n in nums[:3]]
{n: n * n for n in nums[:3]}
{len(w) for w in ["a", "bb", "cc"]}
[(i, j) for i in range(2) for j in range(2)]
sum(n for n in nums if n > 3)

# %% dict_basic annotate
car = {"model": "EQS", "year": 2022}
car["model"]
car.get("color")
car.get("color", "black")
car["color"] = "silver"
"year" in car
list(car.keys())
list(car.values())
car.pop("color")
car.update({"km": 12000})
car
car.setdefault("options", []).append("AMG Line")
car

# %% dict_loop
prices = {"C": 48_000, "E": 62_000, "S": 115_000}
for model, price in prices.items():
    print(f"{model}: {price}")

cheapest = min(prices, key=prices.get)       # key with the smallest value
print("cheapest:", cheapest)
by_price = sorted(prices.items(), key=lambda kv: kv[1], reverse=True)
print(by_price)

# %% counting
words = "red blue red green blue red".split()
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1      # the classic counting pattern
print(counts)

# %% sets annotate
a = {1, 2, 3, 4}
b = {3, 4, 5}
a | b
a & b
a - b
a ^ b
set([1, 1, 2, 2, 3])
3 in a

# %% unpacking annotate
x, y = (3, 4)
x, y
a, b = 1, 2
a, b = b, a
a, b
first, *rest = [1, 2, 3, 4]
first, rest
q, r = divmod(17, 5)
q, r

# %% builtins
models = ["C", "E", "S"]
years = [2014, 2016, 2020]
for i, m in enumerate(models, start=1):
    print(i, m)
for m, y in zip(models, years):
    print(m, y)
print(dict(zip(models, years)))
print(any(y > 2019 for y in years), all(y > 2019 for y in years))
print(list(range(0, 10, 3)), sum(years) / len(years))
print(round(3.14159, 2), abs(-7), 7 // 2, 7 % 2, 2 ** 10)

# %% counter annotate
from collections import Counter
c = Counter("mississippi")
c
c.most_common(2)
c["s"], c["z"]
Counter(["EQS", "C", "EQS"]) + Counter(["C"])

# %% defaultdict
from collections import defaultdict

cars = [("EQS", "electric"), ("C200", "petrol"), ("EQE", "electric")]
groups = defaultdict(list)          # missing key -> starts as []
for model, fuel in cars:
    groups[fuel].append(model)
print(dict(groups))

totals = defaultdict(int)           # missing key -> starts as 0
for model, fuel in cars:
    totals[fuel] += 1
print(dict(totals))

# %% stack_queue annotate
stack = [1, 2, 3]                   # list = stack (LIFO)
stack.append(4)
stack.pop()
from collections import deque
q = deque([1, 2, 3])                # deque = queue (FIFO)
q.append(4)
q.popleft()
q

# %% conversions annotate
int("42") + 1
float("3.5")
str(2026) + "!"
list("abc")
int("ff", 16), bin(5)
type(3.0).__name__
isinstance(3, (int, float))
bool(""), bool([]), bool(0), bool("0")
