# Python for coding interviews — revision

Based on the 8 topic screenshots in this folder (40 lessons). Examples use Python 3. This is a revision reference for the Python tools you use while solving interview problems. Question practice comes after you can explain each pattern.

Read in the order below. For every snippet, be able to say what it returns, what it mutates, and the time/space cost.

These notes assume the Python basics revision is already solid: assignment vs mutation, truthiness, `enumerate`/`zip`, shallow vs deep copy.

## 1. Sorting

`list.sort()` mutates in place and returns `None`. `sorted(iterable)` returns a new list and leaves the original alone. Both are Timsort: O(n log n) time, O(n) extra space, and **stable**.

```python
nums = [5, 1, 4, 2]
nums.sort()                 # nums is now [1, 2, 4, 5]; expression value is None
nums.sort(reverse=True)     # [5, 4, 2, 1]
```

**Custom key:** sort by a derived value. The `key` function runs once per element, then those keys are compared.

```python
words = ["pear", "fig", "apple"]
words.sort(key=len)                         # ['fig', 'pear', 'apple']
pairs = [(1, 3), (2, 1), (1, 2)]
pairs.sort(key=lambda p: (p[0], -p[1]))     # [(1, 3), (1, 2), (2, 1)]
```

`lambda` is a one-line anonymous function. Prefer `key=len` or `key=str.lower` over a lambda when a named function already exists.

`sorted` is the copy:

```python
original = [3, 1, 2]
copy = sorted(original)     # [1, 2, 3]
# original is still [3, 1, 2]
```

- `key=` is the usual interview tool. `cmp` comparators are gone in Python 3.
- Tuples compare left to right, so `key=lambda x: (x[0], -x[1])` sorts by first field ascending, second descending.
- Sorting is stable: equal keys keep their original relative order.
- `sort`/`sorted` compare values; mixing incomparable types (`1` and `"a"`) raises `TypeError`.

**Trap:** `nums = nums.sort()` sets `nums` to `None`. Call `nums.sort()` as a statement, or use `nums = sorted(nums)`.

## 2. Pythonic code

**Unpacking** binds names from a sequence. Lengths must match unless you use a starred target.

```python
a, b = 2, 5
a, b = b, a                 # swap; right side is evaluated first
first, *rest = [1, 2, 3, 4] # first=1, rest=[2, 3, 4]
left, *mid, right = [1, 2, 3, 4]  # left=1, mid=[2, 3], right=4
```

**Loop unpacking** works the same way on each element:

```python
for x, y in [(1, 2), (3, 4)]:
    print(x + y)            # 3, then 7
```

**`enumerate`** yields `(index, value)`. Default start is `0`.

```python
for i, ch in enumerate("ab"):
    print(i, ch)            # 0 a, then 1 b
```

**`zip`** pairs corresponding elements and stops at the shortest iterable.

```python
for name, score in zip(["Ada", "Bob"], [90, 85]):
    print(name, score)
```

`enumerate(zip(a, b))` needs nested unpacking: `for i, (x, y) in enumerate(zip(a, b)):`. Both `enumerate` and `zip` are lazy iterators.

**Chained inequality** is valid and reads like math. Each value is evaluated once.

```python
if 0 <= i < n:              # not: if 0 <= i and i < n, though that is equivalent
    pass
```

**Min/max shortcut:** `min` and `max` accept an iterable or several arguments, plus `key=`.

```python
best = min(3, 1, 4)         # 1
best = min(pairs, key=lambda p: p[1])
# empty iterable raises ValueError unless you pass default=
```

Interview habit: update a running extreme with `best = min(best, candidate)` instead of an `if`.

**Trap:** `if x == 1 or 2:` is always truthy. Write `if x in (1, 2):`. `zip` silently drops leftover items unless you use `strict=True` (Python 3.10+).

## 3. Lists

A Python list is a resizable dynamic array. Indexing and assignment are O(1). `append` / `pop()` at the end are O(1) amortized. Insert, remove, or `pop(0)` at the front are O(n).

```python
arr = []
arr.append(3)               # [3]
arr.append(5)               # [3, 5]
last = arr.pop()            # 5; arr is [3]
arr.insert(0, 9)            # [9, 3] — O(n)
```

**Concatenation** creates a new list. `extend` / `+=` mutate.

```python
left, right = [1, 2], [3]
combined = left + right     # [1, 2, 3]; left unchanged
left.extend(right)          # left is [1, 2, 3]
# left.append(right)        # would add one nested list: [1, 2, [3]]
```

**Initialization:**

```python
zeros = [0] * 4             # [0, 0, 0, 0] — fine for immutable elements
# rows = [[0] * 3] * 2      # both rows share one inner list
rows = [[0] * 3 for _ in range(2)]
```

**Clone:** `arr[:]` and `arr.copy()` are shallow. Assignment shares the same list.

```python
import copy

original = [1, [2, 3]]
alias = original            # same object
shallow = original[:]       # new outer list, same inner list
deep = copy.deepcopy(original)
```

**The scenario.** `original = [1, [2, 3]]`.

Replacing a top-level element only changes that copy. Both shallow and deep copies protect the original here:

```python
shallow[0] = 99
# original -> [1, [2, 3]]     safe
# shallow  -> [99, [2, 3]]
```

Mutating the nested list is where they differ. A shallow copy still shares that inner list:

```python
shallow[1][0] = "X"
# original -> [1, ["X", 3]]   modified
# shallow  -> [99, ["X", 3]]
```

A deep copy duplicates nested structure, so the original stays independent:

```python
original = [1, [2, 3]]
deep = copy.deepcopy(original)
deep[1][0] = "Z"
# original -> [1, [2, 3]]     safe
# deep     -> [1, ["Z", 3]]
```

**List comprehension** builds a new list in one expression.

```python
squares = [x * x for x in range(5) if x % 2 == 0]   # [0, 4, 16]
```

Prefer a comprehension when the result is a list you will keep. Prefer a loop when you are only iterating, or when the body is several statements.

| Operation | Time |
|---|---|
| Index / assign / `len` / `append` / `pop()` | O(1) (`append` amortized) |
| `pop(0)`, `insert(0, x)`, `remove`, `in` | O(n) |
| `arr + other`, `arr[:]`, comprehension of n items | O(n) |

**Trap:** `a = b = []` creates one shared list. Use `a, b = [], []`.

## 4. Stacks and queues

**Stack:** last in, first out. A list is the usual stack: `append` to push, `pop()` to pop. Both O(1).

```python
stack = []
stack.append(1)
stack.append(2)
top = stack.pop()           # 2
# stack[-1] is peek; IndexError if empty
```

**Queue:** first in, first out. Do **not** use `list.pop(0)` — that is O(n). Use `collections.deque`.

```python
from collections import deque

queue = deque()
queue.append("a")           # enqueue at the right
queue.append("b")
front = queue.popleft()     # 'a' — O(1)
```

**Deque** is a double-ended queue. Push/pop at either end is O(1). Indexing in the middle is O(n).

```python
d = deque([1, 2, 3])
d.appendleft(0)             # deque([0, 1, 2, 3])
d.pop()                     # 3 from the right
d.popleft()                 # 0 from the left
```

Typical interview uses: BFS (`queue`), monotonic stack, sliding-window maximum (`deque` of indices), undo (`stack`).

**Trap:** `if stack:` is the emptiness check. `stack[-1]` on an empty list raises `IndexError`. `deque` is not hashable and cannot be sliced the way a list can.

## 5. 2-D lists

A 2-D list is a list of rows. `grid[r][c]` is row first, then column.

```python
grid = [
    [1, 2, 3],
    [4, 5, 6],
]
rows, cols = len(grid), len(grid[0])
grid[1][0]                  # 4
```

**Independent rows** must be created in a loop or a comprehension. `[row] * n` repeats the same row object.

```python
# shared rows — changing one cell changes every row
broken = [[0] * 3] * 2
broken[0][0] = 1
# broken -> [[1, 0, 0], [1, 0, 0]]

grid = [[0] * 3 for _ in range(2)]
grid[0][0] = 1
# grid -> [[1, 0, 0], [0, 0, 0]]
```

**2-D grid traversal** usually walks four (or eight) directions and bounds-checks.

```python
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
for r in range(rows):
    for c in range(cols):
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor = grid[nr][nc]
```

**Nested list comprehension:**

```python
pairs = [[i, j] for i in range(2) for j in range(3)]
# [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]

matrix = [[i * 3 + j for j in range(3)] for i in range(2)]
# [[0, 1, 2], [3, 4, 5]]
```

The rightmost `for` is the inner loop. Read `[expr for row in grid for x in row]` as flatten.

**Trap:** `len(grid[0])` assumes a non-empty rectangular grid. Check `if not grid or not grid[0]:` first. Jagged rows are legal in Python and break `cols = len(grid[0])`.

## 6. Hash maps and hash sets

A dict maps unique hashable keys to values. A set stores unique hashable elements. Average lookup/insert/delete is O(1); worst case is O(n).

```python
counts = {}
counts["a"] = 1
counts["a"] += 1            # 2
counts.get("z", 0)          # 0; does not insert
# counts["z"]               # KeyError
```

**`defaultdict`** inserts a default when a missing key is read.

```python
from collections import defaultdict

groups = defaultdict(list)
groups["a"].append(1)       # groups["a"] is [1]
freq = defaultdict(int)
freq["a"] += 1              # 1
```

**`Counter`** counts hashable items. Missing keys read as `0` and are not inserted by that read.

```python
from collections import Counter

freq = Counter("banana")    # {'b': 1, 'a': 3, 'n': 2}
freq.most_common(1)         # [('a', 3)]
freq["z"]                   # 0
```

**Dict comprehension and items:**

```python
squares = {x: x * x for x in range(4)}          # {0: 0, 1: 1, 2: 4, 3: 9}
for key, value in squares.items():
    pass
```

`keys()`, `values()`, and `items()` are dynamic views. Do not change dict size while iterating over it.

**Hash set:** unique elements, average O(1) membership. Order is not guaranteed. `{}` is a dict; use `set()`.

```python
seen = set()
seen.add(3)
3 in seen                   # True
seen.discard(9)             # no error
# seen.remove(9)            # KeyError
evens = {x for x in range(6) if x % 2 == 0}     # {0, 2, 4}

A, B = {1, 2, 3, 4}, {3, 4, 5, 6}
A | B                       # {1, 2, 3, 4, 5, 6}
A & B                       # {3, 4}
A - B                       # {1, 2}
A ^ B                       # {1, 2, 5, 6}
```

`set(values)` drops duplicates but does not keep order. To deduplicate and keep first-seen order: `list(dict.fromkeys(values))`.

A `frozenset` is immutable and hashable, so it can be a dict key or a set element (a normal set cannot). `frozenset(["A", "B"])` equals `frozenset(["B", "A"])` — useful for undirected edges.

```python
len(nums) != len(set(nums))     # has a duplicate
set(a) & set(b)                 # common elements
```

Use a set for repeated membership checks. Scanning a list is O(n) each time.

**Tuple keys** work when every element is hashable. Lists cannot be keys.

```python
visited = set()
visited.add((1, 2))         # grid cell (r, c)
# visited.add([1, 2])       # TypeError: unhashable type: 'list'
pos = {(r, c): val for r, row in enumerate(grid) for c, val in enumerate(row)}
```

`True` and `1` collide as dict/set keys (they compare equal and hash equal).

**Trap:** `d.get(key)` returning `None` cannot distinguish a missing key from a stored `None`. Use `key in d` when that matters.

## 7. Heaps and priority queues

`heapq` is a **min-heap** on a list. Index `0` is always the smallest item. Push and pop are O(log n). `heapify` is O(n).

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
smallest = heapq.heappop(heap)   # 1; heap is now [3, 5]
peek = heap[0]                   # smallest without removing
```

**Heapify** rearranges an existing list in place. It does not sort the whole list.

```python
nums = [5, 1, 4, 2]
heapq.heapify(nums)         # nums[0] == 1; the rest is heap-ordered, not fully sorted
```

**Max-heap:** negate numbers, then negate again on the way out.

```python
max_heap = []
for x in [5, 1, 4]:
    heapq.heappush(max_heap, -x)
largest = -heapq.heappop(max_heap)   # 5
```

**Custom heap:** store tuples. Comparison is left to right, so put the priority first.

```python
# smallest deadline first; break ties by name
tasks = []
heapq.heappush(tasks, (2, "write"))
heapq.heappush(tasks, (1, "read"))
heapq.heappop(tasks)        # (1, 'read')
```

If two tuples can have equal priorities and incomparable later fields, add a unique tie-breaker (`count`) so the heap never compares the payload.

**N smallest / n largest** are convenience helpers. They do not require you to manage the heap yourself.

```python
heapq.nsmallest(2, [5, 1, 4, 2])    # [1, 2]
heapq.nlargest(2, [5, 1, 4, 2])     # [5, 4]
```

Cost is O(n log k) for k results. For one pass over a stream, keep a heap of size k yourself.

**The scenario.** Find the 2 largest values in `[5, 1, 4, 2]`.

A min-heap of size k keeps the current winners. The heap top is the **smallest of the large values**, so a new candidate replaces it only when it is bigger:

```python
nums, k = [5, 1, 4, 2], 2
heap = []
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)     # drop the current smallest
# heap holds [4, 5] (order inside the heap is not sorted)
```

Using a max-heap for “k largest” is the opposite idea and uses more memory (the whole array). Prefer a size-k min-heap.

**Trap:** `heapq` has no `heappushpop` requirement, but `heappushpop` and `heapreplace` exist and are faster than separate push+pop. There is no max-heap type. Do not sort after every insert — that is the point of a heap.

## 8. Sorted dicts and sorted sets

Ordinary `dict` and `set` are not sorted by key. If you need ordered keys plus fast lookup, interviews usually do one of these:

1. Keep a list sorted yourself and use `bisect` (stdlib, always available).
2. Use `sortedcontainers` (`SortedDict`, `SortedSet`, `SortedList`) if the environment allows a third-party package.

```python
import bisect

vals = [1, 3, 5]
bisect.insort(vals, 4)      # [1, 3, 4, 5] — O(n) to insert, O(log n) to find the index
i = bisect.bisect_left(vals, 4)     # 2
```

`bisect_left` is the insertion point before existing equals; `bisect_right` is after them. `insort` is insert-into-sorted-list, not a balanced tree.

If `sortedcontainers` is allowed:

```python
from sortedcontainers import SortedDict, SortedSet

sd = SortedDict({"c": 3, "a": 1})
sd["b"] = 2
list(sd.keys())             # ['a', 'b', 'c']
sd.bisect_left("b")         # 1 — index of the first key >= "b"

ss = SortedSet([3, 1, 2])
ss.add(2)                   # still SortedSet([1, 2, 3])
ss.bisect_left(2)           # 1
```

- `SortedDict` iterates keys in sorted order. `dict` iterates in insertion order.
- `SortedSet` is an ordered unique collection. `set` has no positional index.
- Typical uses: sliding-window medians, closest-key queries, “next greater key”.
- In a standard coding interview, say you would use a balanced tree / `SortedList`, then implement with `bisect` on a list if the library is unavailable. Insert into a Python list is O(n).

**Trap:** sorting a dict’s keys on every query is O(n log n) and usually the wrong substitute for a sorted map.

## Costs to remember

Assume n elements and ordinary fixed-size values. Hash-table costs are average; individual operations can be O(n) in the worst case.

| Structure / operation | Time |
|---|---|
| List index, `append`, `pop()` | O(1) |
| List insert/pop at front, scan, `in` | O(n) |
| `sort` / `sorted` | O(n log n) |
| Dict / set lookup, insert, delete | O(1) average |
| `deque` append/pop at either end | O(1) |
| `heappush` / `heappop` | O(log n) |
| `heapify` | O(n) |
| `nsmallest` / `nlargest` of k | O(n log k) |
| `bisect` search | O(log n) |
| `bisect.insort` | O(n) |

## Ready to move on

You should be able to explain these without looking them up:

- `sort` vs `sorted`, `key=`, stability, and why `arr = arr.sort()` is wrong.
- Unpacking, `enumerate`, `zip`, and chained comparisons.
- Why `pop(0)` is the wrong queue, and when to use `deque`.
- Independent 2-D rows vs `[row] * n`, and 4-direction bounds checks.
- Shallow vs deep copy on `original = [1, [2, 3]]`.
- `defaultdict`, `Counter`, tuple keys, `set` vs `frozenset`, and `list(dict.fromkeys(...))`.
- Min-heap vs negated max-heap, `heapify`, and a size-k heap for top-k.
- `bisect` as the stdlib stand-in for a sorted map/set.

Next: pick problems that force these tools — arrays/hashing, two pointers, sliding windows, stack, BFS with `deque`, and top-k with `heapq`.
