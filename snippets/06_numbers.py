# Part 7 - classic number problems

# %% fizzbuzz
def fizzbuzz(n: int) -> list[str]:
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:                      # check 15 FIRST
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


print(", ".join(fizzbuzz(15)))

# %% primes
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:                        # only up to sqrt(n)
        if n % i == 0:
            return False
        i += 1
    return True


def primes_up_to(n: int) -> list[int]:
    """Sieve of Eratosthenes."""
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i, p in enumerate(is_p) if p]


print([n for n in range(20) if is_prime(n)])
print(primes_up_to(30))

# %% fibonacci
from functools import lru_cache


def fib_list(n: int) -> list[int]:
    """First n Fibonacci numbers (iterative, O(n))."""
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


@lru_cache(maxsize=None)                     # memoization
def fib(n: int) -> int:
    """n-th Fibonacci number (recursive)."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib_list(10))
print(fib(50))

# %% factorial
import math


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_rec(n: int) -> int:
    return 1 if n <= 1 else n * factorial_rec(n - 1)


assert factorial(5) == factorial_rec(5) == math.factorial(5) == 120
assert factorial(0) == 1
print(factorial(10))

# %% digits
def sum_digits(n: int) -> int:
    n = abs(n)
    total = 0
    while n > 0:
        total += n % 10                      # last digit
        n //= 10                             # drop last digit
    return total


def reverse_int(n: int) -> int:
    sign = -1 if n < 0 else 1
    return sign * int(str(abs(n))[::-1])


print(sum_digits(2026), sum(int(d) for d in str(2026)))
print(reverse_int(-1230))
print(math.gcd(12, 18))                      # greatest common divisor
