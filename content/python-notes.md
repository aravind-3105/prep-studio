# Python basics — interview revision

Based on all 11 topic screenshots in this folder. Examples use Python 3. This is a revision reference, with worked examples and interview traps; question practice comes later.

Read in the order below. Prioritize being able to explain what a line does, what it returns, what it mutates, and how much work it performs.

## 1. Variables

**Names refer to objects. Assignment binds a name; it does not automatically copy an object.**

```python
count = 3                 # int
ratio = 0.5               # float
name = "Ada"              # str
ready = True              # bool
result = None             # explicit absence of a value
x, y = 2, 5               # unpacking; lengths must match
x, y = y, x               # swap; right side evaluated first
first, *rest = [1, 2, 3]   # first=1, rest=[2, 3]
```

- Names are case-sensitive; use `snake_case`, constants conventionally `UPPER_CASE`. Names cannot start with a digit or be keywords. Avoid shadowing `list`, `str`, `sum`, etc.
- Dynamic typing: `x = 1; x = "one"` is legal. Objects have types; names can be rebound to objects of different types.
- Common immutable types: `int`, `float`, `bool`, `str`, `tuple`, `frozenset`. Mutable: `list`, `dict`, `set`.
- Conversion: `int("12") == 12`, `str(12) == "12"`, `int(3.9) == 3` (toward zero).
- `int("3.9")` raises `ValueError`; `"3" + 2` raises `TypeError`.
- `None` differs from `0`, `False`, and `""`. Check it with `is None`.
- `==` compares values; `is` compares object identity. Do not use `is` for numeric/string equality.

```python
a = [1]
b = a
b.append(2)       # a and b both refer to [1, 2]
b = [9]          # rebinding b does not change a
```

**Trap:** `a = b = []` creates one shared list. Use `a, b = [], []` for separate lists.

## 2. Math and Boolean operators

| Expression | Result / meaning |
|---|---|
| `7 / 2` | `3.5` — true division |
| `7 // 2` | `3` — floor division |
| `-7 // 2` | `-4` — floors toward negative infinity |
| `-7 % 2` | `1` — remainder follows divisor's sign |
| `2 ** 3` | `8` — exponentiation |
| `abs(-4)` | `4` |
| `divmod(7, 2)` | `(3, 1)` |

`a == (a // b) * b + a % b` for integers and nonzero `b`.

- Shorthand: `+=`, `-=`, `*=`, `//=`, `%=`. Python has no increment operator `++`.
- Parenthesize when unclear. Arithmetic precedes comparisons; Boolean precedence is `not`, then `and`, then `or`.
- `and` / `or` short-circuit and **return an operand**, not necessarily a Boolean: `0 or 5` → `5`; `"a" and 7` → `7`.
- `not x` always returns a Boolean. `items and items[0]` avoids indexing an empty list.
- `&`, `|`, `^`, `~`, `<<`, `>>` are bitwise operators on integers; they do not replace Boolean `and`/`or`.
- Floats have representation error: `0.1 + 0.2 == 0.3` is false. For approximate comparison, use `math.isclose` with suitable tolerances.
- Python integers grow as needed; extremely large integer arithmetic is not constant-time.

**Trap:** `+=` can mutate a list, but rebinding an integer/string produces a different object.

## 3. Functions

```python
def scaled_total(values: list[int], factor: int = 2) -> int:
    return sum(values) * factor

answer = scaled_total([1, 2], factor=3)   # 9
```

- Parameters are names in the definition; arguments are the supplied values. Arguments can be positional or keyword; required parameters precede ordinary default parameters.
- `return` exits immediately. No return, or bare `return`, produces `None`. Printing is not returning.
- Type hints document intent; Python does not enforce them automatically at runtime.
- `return low, high` returns a tuple, which callers can unpack.
- Arguments bind local names to the supplied objects. Mutating a passed list is visible to the caller; rebinding the parameter is not.

```python
def update(items):
    items.append(1)  # changes caller's list
    items = []       # only rebinds the local name
```

**Scope:** Python searches local → enclosing functions → global → built-ins (LEGB). Assignment inside a function normally makes that name local. Reading it before local assignment raises `UnboundLocalError`. `global` allows rebinding a module name; `nonlocal` allows rebinding an enclosing function's name. Prefer explicit parameters and returns in interview solutions.

**Critical trap: default arguments are evaluated once, when the function is defined.**

```python
def collect(value, items=None):  # avoid items=[]: shared across calls
    if items is None:
        items = []
    items.append(value)
    return items
```

Useful extras: `*args` collects positional arguments into a tuple; `**kwargs` collects keyword arguments into a dict. `f(*values)` unpacks positional arguments; `f(**options)` unpacks keyword arguments. A small sorting key can use `lambda pair: pair[1]`.

## 4. Conditional statements

```python
if score >= 80:
    label = "high"
elif score >= 50:
    label = "medium"
else:
    label = "low"

smaller = a if a < b else b
```

- An `if`/`elif` chain takes only its first true branch. Separate `if` statements are evaluated independently.
- Comparisons: `==`, `!=`, `<`, `<=`, `>`, `>=`; chained comparisons such as `0 <= i < n` are valid.
- Falsy values include `None`, `False`, numeric zero, and empty strings/containers. Most other objects are truthy.
- `if value` treats zero/empty as false; `if value is not None` permits them.
- `if` and `for` blocks do **not** introduce a new local scope. A name assigned only in a branch may remain undefined if that branch is skipped.

**Trap:** `if x == 1 or 2:` is always truthy. Write `if x in (1, 2):` or `if x == 1 or x == 2:`.

## 5. Loops

```python
for value in values:                 # direct iteration
    print(value)
for i, value in enumerate(values):    # index and value
    print(i, value)
for left, right in zip(xs, ys):       # stops at shorter iterable
    print(left, right)

for i in range(2, 8, 2):              # 2, 4, 6; stop excluded
    print(i)
for i in range(3, -1, -1):            # 3, 2, 1, 0
    print(i)

while remaining > 0:
    remaining -= 1                   # ensure progress toward termination
```

- `break`: exit the innermost loop. `continue`: skip to its next iteration. `pass`: do nothing.
- `reversed(values)` iterates backward without making a reversed list.
- `range` stores bounds/step rather than building a list. Its step cannot be zero.
- A loop's optional `else` runs when the loop finishes without `break` (including zero iterations).
- Avoid adding/removing elements from the same collection you are iterating over; build a new collection or iterate over a copy.
- One pass over `n` elements is O(n); all pairs are O(n²). Nested loops are not automatically quadratic: count actual iterations.

**Trap:** `continue` before a `while` loop's counter update can cause an infinite loop.

## 6. Strings

Strings are immutable sequences. Indexing returns a one-character string; there is no separate character type.

```python
s = "python"
len(s)             # 6
s[0], s[-1]        # ('p', 'n')
s[1:4]            # 'yth'; start included, stop excluded
s[::2]            # 'pto'
s[::-1]           # 'nohtyp'
s[99:]            # ''; slicing clips out-of-range bounds
# s[99]           # IndexError
# s[0] = 'P'      # TypeError
s = "P" + s[1:]    # creates a new string
f"{s}: {3.14159:.2f}"  # 'Python: 3.14'
```

- Iterate directly: `for ch in s`; use `enumerate(s)` when you need positions.
- `s.split()` splits on whitespace and collapses repeated whitespace. `s.split(",")` uses a specific separator and preserves empty fields.
- `"-".join(["a", "b"])` → `"a-b"`; all joined elements must be strings.
- Useful methods: `strip()`, `lower()`, `upper()`, `replace(old, new)`, `startswith(prefix)`, `endswith(suffix)`, `isalnum()`.
- `s.find("x")` returns `-1` when absent; `s.index("x")` raises `ValueError`.
- Methods return new strings; `s.lower()` alone does not change `s`.
- `ord("a")` → `97`; `chr(97)` → `"a"`. Confirm a problem's character set before assuming only lowercase English letters.

**Cost:** indexing and `len` are O(1) in typical Python interview analysis; a slice of length k takes O(k) time/space. Repeatedly copying a growing string can take O(n²); accumulate pieces in a list and `"".join(parts)` for linear total construction.

## 7. Lists and tuples

Lists are mutable, ordered sequences; duplicates are allowed.

```python
nums = [3, 1, 2]
nums.append(4)         # [3, 1, 2, 4]; adds one object
nums.extend([5, 6])    # adds each element
last = nums.pop()     # removes and returns 6
nums.insert(0, 9)     # inserts before index 0
nums.remove(1)        # removes first matching value; ValueError if absent
nums.index(2)         # first matching index; ValueError if absent
copy = nums[:]        # shallow copy, like nums.copy()
squares = [x * x for x in nums if x > 2]
```

- Indexing/slicing follow the string rules, but list elements can be reassigned. `del nums[i]` removes by index.
- `len`, `sum`, `min`, `max` are useful. `min([])` and `max([])` raise `ValueError` unless supplied a `default`.
- `nums.sort()` sorts in place and returns `None`; `sorted(nums)` returns a new list. Both accept `key=` and `reverse=`; sorting is stable.
- `nums.reverse()` mutates and returns `None`; `nums[::-1]` creates a reversed copy.
- `append([1, 2])` adds one nested list; `extend([1, 2])` adds two elements.

**Critical traps:**

```python
rows = [[0] * 3] * 2  # both entries reference the same row!
rows = [[0] * 3 for _ in range(2)]  # independent rows

original = [[1], [2]]
copy = original.copy()
copy[0].append(9)     # original also becomes [[1, 9], [2]]
```

A shallow copy separates the outer container, but shares nested objects. `copy.deepcopy` recursively copies nested structure when needed.

**Tuples:** `point = (2, 3)`; a single-element tuple is `(2,)`. Tuple slots cannot be reassigned, but a contained mutable object can still change. A tuple can be a dict key/set element only if all its elements are hashable.

## 8. Sets

Sets store distinct hashable elements. They have no positional indexing or guaranteed iteration order.

```python
seen = set()             # {} creates a dict!
seen.add(3)
seen.update([3, 4])       # {3, 4}
exists = 3 in seen
seen.discard(9)          # no error if absent
seen.remove(3)           # KeyError if absent

{1, 2} | {2, 3}          # union: {1, 2, 3}
{1, 2} & {2, 3}          # intersection: {2}
{1, 2} - {2, 3}          # difference: {1}
{1, 2} ^ {2, 3}          # symmetric difference: {1, 3}
{1} <= {1, 2}            # subset: True
```

- Typical uses: membership, duplicate detection, visited nodes.
- Lists, dicts, and sets are unhashable. Strings, integers, and tuples of hashable values are suitable elements.
- `set(values)` removes duplicates but does not preserve sequence order. `frozenset` is immutable and hashable.

## 9. Dictionaries

Dictionaries map unique hashable keys to arbitrary values. Iteration follows insertion order, not sorted order. Assigning an existing key replaces its value.

```python
counts = {"a": 2}
counts["b"] = 1
counts["a"] += 1
counts.get("missing", 0)   # 0; does not insert the key
counts["c"] = counts.get("c", 0) + 1

for key, value in counts.items():
    print(key, value)

removed = counts.pop("b")
counts.pop("missing", None)  # default avoids KeyError
# del counts['a']            # KeyError if absent
```

- `key in d` checks **keys**. `value in d.values()` checks values and takes a linear scan.
- `d[key]` raises `KeyError` when absent. `get` is useful when absence is expected.
- `keys()`, `values()`, and `items()` return dynamic views; use `list(...)` for a snapshot.
- `d.update(other)` merges, overwriting duplicate keys. `d.copy()` is shallow.
- Do not change dict size while iterating over it.
- `True` and `1` compare equal and have the same hash, so they represent the same dictionary key.

Useful interview additions:

```python
from collections import Counter, defaultdict

freq = Counter("banana")         # a:3, n:2, b:1; missing count is 0
positions = defaultdict(list)
positions["a"].append(0)          # indexing missing key creates its list
```

**Trap:** `d.get(key)` returning `None` cannot distinguish a missing key from a stored `None`. Use `key in d` when that distinction matters.

## 10. Reading stdin

```python
name = input()                        # str, trailing newline removed
n = int(input())                      # explicit conversion
nums = list(map(int, input().split())) # space-separated integers
a, b = map(int, input().split())       # exactly two values required
```

- `input()` returns a string even when the input looks numeric. End-of-file raises `EOFError`.
- `map` is a lazy iterator; use `list(...)` if you need indexing or repeated traversal.
- For larger input, `sys.stdin.readline()` keeps the newline and returns `""` at EOF. Use `.rstrip("\n")` if spaces must be preserved.
- Many live interview platforms call your function directly: follow the provided signature and return values. Parse stdin only when required.
- `print(*nums)` prints elements separated by spaces; avoid extra debug output in judged submissions.

## 11. Exception handling

```python
def parse_integer(text):
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError("Expected an integer") from exc
    else:
        return value       # runs if try succeeds
    finally:
        pass               # cleanup on normal return or exception
```

- Catch specific expected exceptions; order handlers from specific to general.
- Use `except (ValueError, TypeError):` when handling both identically, or separate handlers for different recovery.
- `raise` inside a handler re-raises the current exception. `raise ValueError("message")` signals invalid input.
- Avoid swallowing errors with bare `except:` or `except Exception: pass`; this hides defects.
- Avoid `return` in `finally`: it can override an earlier return or suppress an exception.

| Exception | Typical trigger |
|---|---|
| `TypeError` | Unsupported operation/type; unhashable key |
| `ValueError` | Correct kind of argument, invalid value; failed conversion |
| `IndexError` | Sequence index outside bounds |
| `KeyError` | Missing dictionary key / set removal |
| `NameError` | Name not defined |
| `UnboundLocalError` | Local name read before assignment |
| `ZeroDivisionError` | Division or modulo by zero |

## 12. Costs to remember before DSA

Assume n elements and ordinary fixed-size values; hash-table costs are expected/average, with O(n) worst cases for individual lookups/updates.

| Operation | Time |
|---|---|
| List index / assignment / `len` | O(1) |
| List append | O(1) amortized |
| List pop from end | O(1) |
| List insert/remove/pop at front | O(n) |
| List membership / index / min / max / sum | O(n) |
| List slice or shallow copy of k elements | O(k), also O(k) extra space |
| List sorting | O(n log n) worst case |
| Dict/set membership, lookup, insertion, deletion | O(1) average; O(n) worst case |
| Iterate list/dict/set | O(n) |

Hashing/comparing long keys adds work; do not assume a newly created long string/tuple key costs O(1) to process.

## Ready to move on

You should be able to explain these without looking them up:

- Assignment versus mutation versus shallow copying.
- Equality versus identity; truthiness versus checking for `None`.
- Floor division with negatives and short-circuit evaluation.
- Return values, local scope, and the mutable-default pitfall.
- Exclusive slice/range bounds and safe reverse iteration.
- `append` versus `extend`; `sort` versus `sorted`.
- Hashability, dictionary membership, and missing-key handling.
- Why list membership and front removal can make an otherwise simple algorithm slow.

Next bridge topics: Big-O, recursion/call stacks, `deque`, `heapq`, `bisect`, and small node classes. These belong to the DSA phase rather than this basics revision.
