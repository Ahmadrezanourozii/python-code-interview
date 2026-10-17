# Part 8 - classic list problems

# %% find_max
def find_max(nums):
    if not nums:
        raise ValueError("empty list")
    best = nums[0]
    for n in nums[1:]:
        if n > best:
            best = n
    return best


def second_largest(nums):
    first = second = None
    for n in nums:
        if first is None or n > first:
            first, second = n, first
        elif n != first and (second is None or n > second):
            second = n
    return second


print(find_max([3, 7, 2]), second_largest([3, 7, 2, 7, 5]))
print(second_largest([4, 4]))                # no distinct second -> None

# %% dedupe annotate
def dedupe(items):
    seen, result = set(), []
    for x in items:
        if x not in seen:                    # set lookup is O(1)
            seen.add(x)
            result.append(x)
    return result


nums = [3, 1, 3, 2, 1]
dedupe(nums)
list(dict.fromkeys(nums))
sorted(set(nums))

# %% two_sum
def two_sum_brute(nums, target):             # O(n^2)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
    return None


def two_sum(nums, target):                   # O(n) with a dict
    seen = {}                                # value -> index
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return seen[need], i
        seen[n] = i
    return None


print(two_sum_brute([2, 7, 11, 15], 9), two_sum([2, 7, 11, 15], 9))
print(two_sum([3, 3], 6), two_sum([1, 2], 10))

# %% missing_number
def missing_number(nums):
    """nums holds 0..n with exactly one number missing."""
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)      # expected sum - real sum


def missing_numbers(nums, start, end):
    return sorted(set(range(start, end + 1)) - set(nums))


print(missing_number([3, 0, 1]))
print(missing_numbers([1, 2, 4, 7], 1, 7))

# %% merge_sorted
def merge_sorted(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])                     # leftovers (one is empty)
    result.extend(b[j:])
    return result


print(merge_sorted([1, 4, 9], [2, 3, 10, 12]))

# %% flatten
def flatten(items):
    result = []
    for x in items:
        if isinstance(x, list):
            result.extend(flatten(x))        # recursion
        else:
            result.append(x)
    return result


print(flatten([1, [2, [3, 4]], [], 5]))
print([x for row in [[1, 2], [3, 4]] for x in row])   # one level only

# %% rotate_chunk
def rotate(nums, k):
    if not nums:
        return []
    k %= len(nums)                           # k may be bigger than len
    return nums[-k:] + nums[:-k]


def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


print(rotate([1, 2, 3, 4, 5], 2), rotate([1, 2, 3], 3))
print(chunk([1, 2, 3, 4, 5, 6, 7], 3))

# %% duplicates
from collections import Counter


def find_duplicates(items):
    return [x for x, c in Counter(items).items() if c > 1]


def common(a, b):
    return sorted(set(a) & set(b))


print(find_duplicates([1, 2, 3, 2, 4, 1]))
print(common([1, 2, 3, 4], [3, 4, 5]))

# %% moving_average
def moving_average(values, window):
    if window <= 0 or window > len(values):
        raise ValueError("invalid window")
    window_sum = sum(values[:window])
    result = [window_sum / window]
    for i in range(window, len(values)):
        window_sum += values[i] - values[i - window]   # slide the window
        result.append(window_sum / window)
    return result


speeds = [50, 52, 55, 60, 58, 61]
print([round(x, 2) for x in moving_average(speeds, 3)])

# %% max_profit
def max_profit(prices):
    """Best profit from one buy followed by one sell."""
    lowest, best = float("inf"), 0
    for p in prices:
        lowest = min(lowest, p)              # cheapest buy so far
        best = max(best, p - lowest)         # sell today?
    return best


print(max_profit([7, 1, 5, 3, 6, 4]), max_profit([7, 6, 4, 3]))

# %% binary_search
import bisect


def binary_search(nums, target):
    """Index of target in the SORTED list nums, or -1."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


data = [2, 5, 8, 12, 16, 23, 38]
print(binary_search(data, 23), binary_search(data, 7))
print(bisect.bisect_left(data, 23))          # built-in helper

# %% bubble_sort
def bubble_sort(nums):
    nums = nums[:]                           # don't modify the input
    n = len(nums)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:                      # already sorted -> stop
            break
    return nums


print(bubble_sort([5, 1, 4, 2, 8]), bubble_sort([]))

# %% matrix annotate
m = [[1, 2, 3],
     [4, 5, 6]]
[list(row) for row in zip(*m)]
[sum(row) for row in m]
[sum(col) for col in zip(*m)]
max(max(row) for row in m)
[[0] * 3 for _ in range(2)]
