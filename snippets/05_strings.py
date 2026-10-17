# Part 6 - classic string problems

# %% reverse_string
def reverse_string(s: str) -> str:
    return s[::-1]


def reverse_string_loop(s: str) -> str:
    chars = []
    for i in range(len(s) - 1, -1, -1):      # walk from the end
        chars.append(s[i])
    return "".join(chars)


assert reverse_string("abc") == reverse_string_loop("abc") == "cba"
assert reverse_string("") == ""
print(reverse_string("Mercedes"), "".join(reversed("Benz")))

# %% palindrome
def is_palindrome(s: str) -> bool:
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]


def is_palindrome_two_pointers(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True


for text in ["racecar", "A man, a plan, a canal: Panama", "hello", ""]:
    print(repr(text), is_palindrome(text), is_palindrome_two_pointers(text))

# %% count_vowels
def count_vowels(s: str) -> int:
    return sum(1 for ch in s.lower() if ch in "aeiou")


assert count_vowels("Mercedes-Benz") == 4
assert count_vowels("") == 0
print(count_vowels("Hello World"))

# %% char_frequency
from collections import Counter


def char_frequency(s: str) -> dict:
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


print(char_frequency("banana"))
print(Counter("banana"))
print(Counter("banana").most_common(1))      # most frequent character

# %% first_unique
from collections import Counter


def first_unique_char(s: str):
    counts = Counter(s)                      # pass 1: count
    for i, ch in enumerate(s):               # pass 2: first with count 1
        if counts[ch] == 1:
            return i, ch
    return None


print(first_unique_char("swiss"))
print(first_unique_char("aabb"))

# %% anagram
from collections import Counter, defaultdict


def is_anagram(a: str, b: str) -> bool:
    a = a.replace(" ", "").lower()
    b = b.replace(" ", "").lower()
    return Counter(a) == Counter(b)          # or: sorted(a) == sorted(b)


def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w) # same letters -> same key
    return list(groups.values())


print(is_anagram("Listen", "Silent"), is_anagram("abc", "abd"))
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

# %% word_count
import re
from collections import Counter


def top_words(text: str, k: int = 3):
    words = re.findall(r"[a-z']+", text.lower())
    return Counter(words).most_common(k)


def top_words_plain(text: str, k: int = 3):
    counts = {}
    for w in text.lower().split():
        w = w.strip(".,!?;:\"'()")
        if w:
            counts[w] = counts.get(w, 0) + 1
    # sort by count (high first), then alphabetically for ties
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


text = "The car is fast. The car is red! Is the car electric?"
print(top_words(text))
print(top_words_plain(text))

# %% sentence_ops annotate
sentence = "  python is   fun  "
" ".join(sentence.split()[::-1])
" ".join(w.capitalize() for w in sentence.split())
" ".join(w[::-1] for w in sentence.split())
max(sentence.split(), key=len)

# %% compress
from itertools import groupby


def compress(s: str) -> str:
    if not s:
        return ""
    result = []
    current, count = s[0], 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            result.append(f"{current}{count}")
            current, count = ch, 1
    result.append(f"{current}{count}")       # don't forget the last group
    return "".join(result)


def compress_groupby(s: str) -> str:
    return "".join(f"{ch}{len(list(g))}" for ch, g in groupby(s))


assert compress("aaabbc") == compress_groupby("aaabbc") == "a3b2c1"
assert compress("") == ""
print(compress("aaabccdddd"))

# %% brackets
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack                         # leftovers -> not balanced


for t in ["(a[b]{c})", "(]", "((", ""]:
    print(repr(t), is_balanced(t))

# %% decompress
import re


def decompress(s: str) -> str:
    """'a3b2' -> 'aaabb'"""
    return "".join(ch * int(n) for ch, n in re.findall(r"(\D)(\d+)", s))


assert decompress(compress("aaabccdddd")) == "aaabccdddd"
print(decompress("a3b1c2"))
