# Part 3 - functions, input and error handling

# %% fake_input hidden
import builtins


def _fake_input(prompt=""):
    print(prompt + "42")
    return "42"


builtins.input = _fake_input

# %% func_basic
def average(values: list[float]) -> float:
    """Return the arithmetic mean of values."""
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)


def min_max(values):
    return min(values), max(values)          # returns a tuple


print(average([2, 4, 6]))
lo, hi = min_max([3, 9, 1])
print(lo, hi)

# %% func_args
def greet(name, greeting="Hello"):           # default argument
    return f"{greeting}, {name}!"


def total(*args):                            # any number of positional args
    return sum(args)


def describe(**kwargs):                      # any number of keyword args
    return ", ".join(f"{k}={v}" for k, v in kwargs.items())


print(greet("Nico"))
print(greet("Nico", greeting="Hi"))
print(total(1, 2, 3))
print(describe(model="EQS", year=2022))

# %% lambda_map annotate
square = lambda x: x * x
square(5)
list(map(str.upper, ["a", "b"]))
list(filter(lambda n: n > 2, [1, 2, 3, 4]))
[n for n in [1, 2, 3, 4] if n > 2]

# %% user_input
raw = input("Enter mileage: ")               # input() ALWAYS returns a str
try:
    km = int(raw)
    print(f"You entered {km} km")
except ValueError:
    print("Please enter a whole number")

# %% try_except
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("cannot divide by zero")
        return None
    except TypeError as e:
        print("bad input:", e)
        return None
    else:                                    # runs only if no exception
        return result
    finally:                                 # always runs
        print("done")


print(safe_divide(10, 2))
print(safe_divide(1, 0))

# %% parse_numbers
def parse_numbers(items):
    """Convert strings to floats and collect the invalid ones."""
    numbers, errors = [], []
    for item in items:
        try:
            numbers.append(float(item))
        except (ValueError, TypeError):
            errors.append(item)
    return numbers, errors


print(parse_numbers(["1.5", "abc", "3", None, ""]))

# %% custom_exception
class InvalidVinError(Exception):
    """Raised when a vehicle identification number is invalid."""


def validate_vin(vin: str) -> str:
    vin = vin.strip().upper()
    if len(vin) != 17:
        raise InvalidVinError(f"VIN must have 17 chars, got {len(vin)}")
    if any(ch in "IOQ" for ch in vin):
        raise InvalidVinError("VIN must not contain I, O or Q")
    return vin


for v in ["wdd2220011a123456", "ABC"]:
    try:
        print("valid:", validate_vin(v))
    except InvalidVinError as e:
        print("error:", e)
