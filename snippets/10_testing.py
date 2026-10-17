# Part 11 - quick tests, pitfalls

# %% asserts
def normalize_plate(plate: str) -> str:
    """' s-mb 1234 ' -> 'S-MB 1234'"""
    return " ".join(plate.upper().split())


assert normalize_plate("s-mb 1234 ") == "S-MB 1234"
assert normalize_plate("  b  ab 12") == "B AB 12"     # extra spaces
assert normalize_plate("") == ""                      # edge case
print("all tests passed")

# %% pytest_style
# file: test_stats.py      run with:  pytest -q
import pytest


def average(values):
    if not values:
        raise ValueError("empty")
    return sum(values) / len(values)


def test_average_normal():
    assert average([1, 2, 3]) == 2


def test_average_float():
    assert average([0.1, 0.2]) == pytest.approx(0.15)


def test_average_empty():
    with pytest.raises(ValueError):
        average([])

# %% run_tests hidden
test_average_normal()
test_average_float()
test_average_empty()

# %% mutable_default
def add_item_bad(item, items=[]):            # BAD: one list for all calls
    items.append(item)
    return items


def add_item_good(item, items=None):         # GOOD
    if items is None:
        items = []
    items.append(item)
    return items


print(add_item_bad("a"), add_item_bad("b"))      # surprise!
print(add_item_good("a"), add_item_good("b"))

# %% copy_pitfall
a = [1, 2, 3]
b = a                                        # same object, not a copy!
b.append(4)
print(a)
c = a.copy()                                 # or a[:] or list(a)
c.append(5)
print(a, c)

grid = [[0] * 2] * 2                         # BAD: rows share one list
grid[0][0] = 9
print(grid)
grid = [[0] * 2 for _ in range(2)]           # GOOD
grid[0][0] = 9
print(grid)

# %% modify_while_iterating
nums = [1, 2, 2, 3, 4]
for n in nums:                               # BAD: removing while looping
    if n % 2 == 0:
        nums.remove(n)
print(nums)                                  # a 2 survived!

nums = [1, 2, 2, 3, 4]
nums = [n for n in nums if n % 2 != 0]       # GOOD: build a new list
print(nums)

# %% gotchas annotate
a, b = [1, 2], [1, 2]
a == b, a is b
x = None
x is None
0.1 + 0.2 == 0.3
abs((0.1 + 0.2) - 0.3) < 1e-9
7 / 2, 7 // 2, -7 // 2
round(2.5), round(3.5)
"5" + str(5), int("5") + 5

# %% immutable_str
s = "car"
try:
    s[0] = "b"
except TypeError as e:
    print("TypeError:", e)
s = "b" + s[1:]                              # build a new string
print(s)
