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

**Custom key:** sort by a derived value. The `key` function runs once per element, then those keys are compared. `cmp` comparators are gone in Python 3.

```python
original = [3, 1, 2]
copy = sorted(original)     # [1, 2, 3]; original is still [3, 1, 2]
```

- Sorting is stable: equal keys keep their original relative order.
- `sort`/`sorted` compare values; mixing incomparable types (`1` and `"a"`) raises `TypeError`.

**Trap:** `nums = nums.sort()` sets `nums` to `None`. Call `nums.sort()` as a statement, or use `nums = sorted(nums)`.

### Lambda functions

A **lambda** is a short anonymous function: one expression, no `def` name, no `return` keyword. The expression’s value is what it returns.

```python
def square(x):
    return x * x

square = lambda x: x * x     # same idea
square(5)                    # 25
```

Syntax: `lambda arguments: expression`

- Arguments are the inputs (`x`, `p`, `a, b`).
- The expression is computed and returned automatically.
- Lambdas cannot contain statements (`if` blocks, loops, `return`, assignments). Use a ternary if you need a branch: `lambda x: "even" if x % 2 == 0 else "odd"`.
- Defaults work: `lambda x, y=1: x + y`.

A lambda is just a function object. You *can* assign it to a name, but that is usually worse than `def`. The real use is passing a tiny function into something else — especially `sort`, `sorted`, `min`, `max`, and `map`.

```python
nums = [3, 1, 2]
sorted(nums, key=lambda x: -x)      # [3, 2, 1]
max(nums, key=lambda x: x % 3)      # 2
```

Prefer a named function when it already exists: `key=len` not `key=lambda w: len(w)`.

**Trap:** `key=len` passes the function. `key=len()` *calls* it with no argument and fails.

### `key=lambda` in sorting

`key=` tells Python **what to sort by**. Python still sorts those keys in **ascending** order. The original items come along for the ride.

Default tuple order is first field, then second:

```python
pairs = [(2, 1), (1, 2), (1, 3)]
pairs.sort()
# [(1, 2), (1, 3), (2, 1)]
```

Want first field ascending, and when those are equal, second field **descending**: `[(1, 3), (1, 2), (2, 1)]`.

```python
pairs.sort(key=lambda p: (p[0], -p[1]))
```

| Piece | Role |
|---|---|
| `key=` | Sort by this derived value, not by the raw tuple |
| `lambda p:` | Each pair is the input `p` |
| `p[0]` | First field, ascending (smaller first) |
| `-p[1]` | Negate the second field so larger originals sort first |

Python applies the lambda once per tuple, then sorts the keys lexicographically (left to right):

| Original | Key | Why that order |
|---|---|---|
| `(1, 3)` | `(1, -3)` | First field `1`; `-3 < -2` so this beats `(1, 2)` |
| `(1, 2)` | `(1, -2)` | Same first field; `-2` is larger, so later |
| `(2, 1)` | `(2, -1)` | First field `2` comes last |

Negating a **numeric** key reverses that component. It does not work for strings or arbitrary objects — use `reverse=True` for a single-key descending sort, or a wrapper that Python can compare.

### Common lambda sorting patterns

`pairs = [(2, 1), (1, 2), (1, 3)]`

| Requirement | `key=` | Result |
|---|---|---|
| First asc, second asc | `lambda p: (p[0], p[1])` | `[(1, 2), (1, 3), (2, 1)]` |
| First asc, second desc | `lambda p: (p[0], -p[1])` | `[(1, 3), (1, 2), (2, 1)]` |
| First desc, second asc | `lambda p: (-p[0], p[1])` | `[(2, 1), (1, 2), (1, 3)]` |
| Both descending | `lambda p: (-p[0], -p[1])` | `[(2, 1), (1, 3), (1, 2)]` |
| Second field only, asc | `lambda p: p[1]` | `[(2, 1), (1, 2), (1, 3)]` |

```python
words = ["banana", "kiwi", "apple"]
words.sort(key=len)              # ['kiwi', 'apple', 'banana']
words.sort(key=str.lower)        # case-insensitive
words.sort(key=lambda w: (-len(w), w))   # longer first, then A–Z
```

Interview rule: multi-criteria sort → return a **tuple** of keys. Python compares left to right. `lambda p: ...` builds that key; `key=` tells `sort` to use it. `min(values, key=fn)` / `max(...)` use the same rule: minimize (or maximize) the key, then return the **original** element. `min(fn(v) for v in values)` would return the transformed key instead.

```python
pairs.sort(key=lambda p: (p[0], -p[1]))     # in place
result = sorted(pairs, key=lambda p: p[1])  # new list
```

### How sorting algorithms work

Python's `sort`/`sorted` already give you a fast stable sort. Interviews still ask you to **explain or implement** the classic algorithms, and to pick one by time, space, and stability.

Two families:

- **Comparison sorts** — decide order by comparing pairs (`<`, `>`). A comparison sort cannot beat O(n log n) in the worst case.
- **Non-comparison sorts** — use the structure of the keys (counts, digits, buckets). They can be O(n) when the value range is small.

Running example: `[5, 1, 4, 2]`.

### O(n²) comparison sorts

**Bubble sort** walks the array and swaps adjacent items that are out of order. Each pass bubbles the next-largest value to the end. After pass 1, `5` is at the back; after pass 2, `4` is next; and so on.

```python
# [5, 1, 4, 2]
# [1, 5, 4, 2]     swap 5 and 1
# [1, 4, 5, 2]     swap 5 and 4
# [1, 4, 2, 5]     swap 5 and 2   — 5 is in place
# [1, 2, 4, 5]     later passes
```

Stable. Adaptive if you stop when a pass makes no swaps. Rarely used in production.

**Selection sort** finds the minimum of the unsorted suffix and swaps it into the next position. First it places `1`, then `2`, then `4`. Always Θ(n²) comparisons; not stable in the usual in-place swap version.

**Insertion sort** keeps a sorted prefix and inserts the next element into it (like sorting a hand of cards). `[5]` then insert `1` → `[1, 5]`, insert `4` → `[1, 4, 5]`, insert `2` → `[1, 2, 4, 5]`.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key, j = arr[i], i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

Stable. Best case O(n) on already-sorted input. Excellent for tiny or nearly sorted arrays — Timsort uses it on short runs.

### O(n log n) comparison sorts

**Merge sort** splits the array in half, sorts each half, then merges two sorted lists. Always O(n log n). Stable. Needs O(n) extra space.

```python
# [5, 1, 4, 2]
# [5, 1]     [4, 2]
# [5] [1]    [4] [2]
# [1, 5]     [2, 4]
# [1, 2, 4, 5]          merge: take the smaller head each time
```

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:          # <= keeps it stable
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]
```

The merge step is O(n). The recursion tree has log n levels, so total time is O(n log n). Linked-list sorting is often merge sort because splitting and merging need no random access.

**Quicksort** picks a **pivot**, partitions into “less than pivot” and “greater than pivot”, then recurses. Average O(n log n). Worst case O(n²) when the pivot is always the smallest or largest (already sorted + bad pivot). Typical in-place versions are **not stable**. O(log n) stack space on average.

```python
# [5, 1, 4, 2]  pivot 2
# < 2: [1]      > 2: [5, 4]
# [1] + [2] + sort([5, 4]) → [1, 2, 4, 5]
```

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    more = [x for x in arr if x > pivot]
    return quicksort(less) + equal + quicksort(more)
```

This version uses extra lists for clarity. In-place Hoare/Lomuto partition is what people mean by “classic quicksort.” Randomized or median-of-three pivots avoid the O(n²) case in expectation.

**Heapsort** builds a max-heap in O(n) (`heapify`), then repeatedly pops the largest into the end of the array. O(n log n) always. In-place. Not stable. You already use this idea with `heapq` for top-k; full heapsort is less common in Python interviews than merge/quick.

### Linear-time sorts (when keys allow it)

**Counting sort** counts how many times each integer in `0..k` appears, then writes values out in order. O(n + k) time and space. Stable if you fill from the counts carefully. Use it when k is not huge (ages, grades, small IDs).

```python
def counting_sort(arr, k):
    counts = [0] * (k + 1)
    for x in arr:
        counts[x] += 1
    out = []
    for value, freq in enumerate(counts):
        out.extend([value] * freq)
    return out
# counting_sort([5, 1, 4, 2], 5) → [1, 2, 4, 5]
```

**Radix sort** counting-sorts by digit (least significant digit first, if that pass is stable). O(d · (n + b)) for d digits and base b. Useful for fixed-length integers or strings.

**Bucket sort** scatters values into buckets, sorts each bucket (often insertion), then concatenates. Average O(n) when values are spread evenly.

### What Python actually uses

**Timsort** (CPython `list.sort` / `sorted`): find already-sorted **runs**, insertion-sort short runs, then merge them. Worst and average O(n log n), best O(n) on sorted or reverse-sorted data, O(n) extra space, **stable**. That is why you almost always call `sort`/`sorted` in a Python interview unless the question is “implement merge sort.”

| Algorithm | Best | Average | Worst | Extra space | Stable | Notes |
|---|---|---|---|---|---|---|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes | Adjacent swaps |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No | Fewest swaps |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes | Tiny / nearly sorted |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Predictable; linked lists |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Fast average; watch pivot |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | No | In-place n log n |
| Counting | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | Small integer range |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) | Yes | Python's `sort`/`sorted` |

Interview rule: use `sort`/`sorted` unless asked to implement a sort. If you must write one, merge sort is the usual “explainable and always O(n log n)” answer; mention quicksort’s average speed and worst-case pivot risk; mention counting/radix when keys are small integers.

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

Interview habit: update a running extreme with `best = min(best, candidate)` instead of an `if`. `key=lambda v: (abs(v - x), v)` means “smallest distance, then smallest value on a tie” — and `min` still returns the original `v`, not the tuple. See closest-key in Sorted dicts.

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

These names sound alike. Keep the **structure**, the **operations**, and the **Python type** separate.

| Term | Meaning |
|---|---|
| Queue | FIFO structure: first in, first out |
| Enqueue | Add an element to a queue |
| Dequeue | Remove an element from a queue |
| Deque | Double-ended queue: insert or remove at **either** end |

`deque` is pronounced **deck**. It is the data structure. *Dequeue* is the remove operation.

A **queue** is a rule about processing order (FIFO). A **deque** is a flexible structure you can use to implement that rule — or a stack, or both-ends access.

### Queue — FIFO

People in a coffee line: Alex, then Bob, then Charlie. Alex is served first.

New items enter at the **right**. Existing items leave from the **left**.

```python
from collections import deque

queue = deque()
queue.append("Alex")        # enqueue
queue.append("Bob")
queue.append("Charlie")
# deque(['Alex', 'Bob', 'Charlie'])
queue.popleft()             # dequeue → 'Alex'
```

### Deque — both ends

A deque lets you add or remove at the front **or** the back. All four end operations are O(1). Peeking at either end is O(1). The middle is O(n) — not a random-access array.

```python
d = deque([10, 20, 30])
# left/front 10 … 30 right/back
d.append(40)                # [10, 20, 30, 40]
d.appendleft(5)             # [5, 10, 20, 30, 40]
d.pop()                     # 40 from the right
d.popleft()                 # 5 from the left
# deque([10, 20, 30])
```

| Method | Action | Time |
|---|---|---|
| `append(x)` | Add at right | O(1) |
| `appendleft(x)` | Add at left | O(1) |
| `pop()` | Remove from right | O(1) |
| `popleft()` | Remove from left | O(1) |
| `d[0]` / `d[-1]` | Peek front / back | O(1) |

### Why not a list as a queue?

`list.append` is O(1) amortized, but `list.pop(0)` is O(n): every remaining element shifts left. At thousands of operations that cost shows up. `deque.popleft()` does not shift the whole collection.

```python
queue = [10, 20, 30]
queue.append(40)            # O(1) amortized
queue.pop(0)                # O(n) — avoid this

queue = deque([10, 20, 30])
queue.append(40)            # O(1)
queue.popleft()             # O(1)
```

### Stack vs queue on the same structure

The same `deque` can be a stack or a queue. What changes is **which end** you use. A plain list is also a fine stack.

```python
stack = []                  # or deque(); LIFO
stack.append(1)
stack.append(2)
stack.pop()                 # 2 — last in, first out
# stack[-1] is peek; IndexError if empty

queue = deque()             # FIFO
queue.append(1)             # enqueue
queue.append(2)
queue.popleft()             # 1 — first in, first out
```

| Role | Insert | Remove |
|---|---|---|
| Stack (LIFO) | `append` | `pop` |
| Queue (FIFO) | `append` | `popleft` |

Typical interview uses: BFS (queue), DFS/undo (stack), monotonic stack, sliding-window maximum (`deque` of indices).

**Trap:** `if stack:` is the emptiness check. `stack[-1]` on an empty list raises `IndexError`. `deque` is not hashable and cannot be sliced the way a list can.

### BFS uses a queue

Breadth-first search processes nodes in the order they are discovered. That is FIFO, so use `append` / `popleft`. A stack would give a depth-first order instead.

```python
graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
queue, visited = deque(["A"]), {"A"}
while queue:
    node = queue.popleft()
    print(node)             # A, then B, C, then D
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
```

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

**`Counter`** counts an iterable automatically. Missing keys read as `0` and are not inserted.

```python
from collections import Counter

freq = Counter("banana")    # Counter({'a': 3, 'n': 2, 'b': 1})
freq["z"]                   # 0 — not a KeyError, and not inserted
freq.most_common(1)         # [('a', 3)]
freq.update("aaa")
freq["a"]                   # 6
Counter([1, 2, 2, 3, 3, 3]) # Counter({3: 3, 2: 2, 1: 1})

def is_anagram(s, t):
    return Counter(s) == Counter(t)
```

**`defaultdict`** creates and stores a default on missing-key access with `[]`. `d["a"].append(0)` on a normal dict is `KeyError`.

```python
from collections import defaultdict

positions = defaultdict(list)
for i, ch in enumerate("banana"):
    positions[ch].append(i)
# {'b': [0], 'a': [1, 3, 5], 'n': [2, 4]}

freq = defaultdict(int)
for ch in "banana":
    freq[ch] += 1           # missing key starts at 0

graph = defaultdict(set)
for u, v in [("A", "B"), ("A", "C"), ("A", "B")]:
    graph[u].add(v)
# {'A': {'B', 'C'}}
```

`[]` inserts the default; `.get()` does not: `defaultdict(list).get("x")` is `None`.

| Need | Use |
|---|---|
| Frequency of an iterable | `Counter` |
| Count while looping | `defaultdict(int)` or `Counter` |
| Group into lists | `defaultdict(list)` |
| Unique neighbors / edges | `defaultdict(set)` |

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

A **heap** is a complete binary tree with a parent-child rule. Python stores it as a list via `heapq`. It is **not** a sorted list — only the heap property is guaranteed. `[2, 4, 6, 5]` is a valid min-heap because `2 ≤ 4`, `2 ≤ 6`, and `4 ≤ 5`.

| | Min-heap | Max-heap |
|---|---|---|
| Root | Smallest | Largest |
| Rule | Parent ≤ children | Parent ≥ children |
| Retrieve | Minimum | Maximum |
| In Python | `heap[0]` is smallest | Negate values, or 3.14+ max helpers |

`heapq` is a min-heap. Push and pop are O(log n). Peek is O(1). `heapify` is O(n).

### Sift-up vs sift-down

| Operation | Technique | Time |
|---|---|---|
| Insert (`heappush`) | Sift-up | O(log n) |
| Remove root (`heappop`) | Sift-down | O(log n) |
| Build (`heapify`) | Bottom-up sift-down | O(n) |
| Peek (`heap[0]`) | No movement | O(1) |
| Heap sort | Repeated root removal | O(n log n) |

**Insert → sift-up.** Put the new value at the end. Swap with its parent while the heap rule is broken.

```python
# [3, 5, 4] insert 2
# [3, 5, 4, 2]
# [3, 2, 4, 5]     swap with parent
# [2, 3, 4, 5]     swap again; 2 is the new root
```

**Remove root → sift-down.** Take `heap[0]`. Move the last item to the root. Swap with the smaller child (min-heap) until the rule holds.

```python
# [2, 4, 6, 5] pop 2
# [5, 4, 6]        last item moves to the root
# [4, 5, 6]        5 swaps with smaller child 4
```

Memory trick: insert → up; remove root → down; build → bottom-up down; heap sort → repeated down.

### `heapify` — build in O(n)

Turns an unsorted list into a heap **in place**. Starts at the last parent (`n // 2 - 1`) and sifts down while walking toward the root. That is cheaper than n separate pushes (which would be O(n log n)). The result is heap-ordered, not fully sorted.

```python
import heapq

nums = [5, 3, 8, 1, 2]
heapq.heapify(nums)
# Original:  [5, 3, 8, 1, 2]
# After 3:   [5, 1, 8, 3, 2]
# After 5:   [1, 2, 8, 3, 5]
# nums[0] == 1; the rest is not sorted
```

### Min-heap with `heapq`

```python
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
heap                       # [1, 5, 3] — heap-ordered
heap[0]                    # 1 — peek
heapq.heappop(heap)        # 1 — remove minimum
```

Use `heapq` operations. Mutating the list by hand can break the heap property.

### Max-heap

Interview-safe approach: negate numbers, then negate on the way out. The largest positive becomes the smallest negative, so the min-heap surfaces it first.

```python
max_heap = []
for x in [5, 1, 4]:
    heapq.heappush(max_heap, -x)
largest = -heapq.heappop(max_heap)   # 5
```

Python 3.14+ also has `heapq.heappush_max` / `heappop_max`. In interviews, still prefer negation unless the prompt allows 3.14.

**Custom order:** store tuples. Comparison is left to right, so put the priority first.

```python
tasks = []
heapq.heappush(tasks, (2, "write"))
heapq.heappush(tasks, (1, "read"))
heapq.heappop(tasks)        # (1, 'read')
```

If two tuples can have equal priorities and incomparable later fields, add a unique tie-breaker (`count`) so the heap never compares the payload.

### K largest / k smallest

Keep a heap of size **k**. For the k **largest**, use a **min-heap**: the root is the smallest of the current winners, so you can drop it when a bigger candidate arrives. Time O(n log k), space O(k).

```python
nums, k = [5, 1, 4, 2], 2
heap = []
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)     # drop the current smallest
# heap holds [4, 5] (not sorted)
```

K **smallest** is the mirror: a size-k **max-heap** (negated values). A max-heap of the whole array also works for k largest but uses O(n) memory.

Helpers if you already have the full list: `heapq.nsmallest(2, nums)` → `[1, 2]`; `heapq.nlargest(2, nums)` → `[5, 4]`. Same O(n log k). For a stream, maintain the size-k heap yourself.

| Need | Approach |
|---|---|
| Smallest repeatedly | Min-heap |
| Largest repeatedly | Max-heap (negate) |
| Insert | Sift-up (`heappush`) |
| Remove root | Sift-down (`heappop`) |
| Unsorted list → heap | `heapq.heapify` — O(n) |
| K largest | Size-k min-heap |
| K smallest | Size-k max-heap |
| Sort with a heap | Repeated `heappop` — O(n log n) |

**Trap:** `heappushpop` and `heapreplace` are faster than separate push+pop when you need both. Do not sort after every insert — partial order is the point of a heap.

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
- In a standard coding interview, say you would use a balanced tree / `SortedList`, then implement with `bisect` on a list if the library is unavailable. Insert into a Python list is O(n).

### Typical uses

A dict answers “is this exact key present?” in O(1). A heap answers “what is the current min or max?” A sorted list/map answers questions about **order among keys**: successor, nearest neighbor, and the middle of a changing window.

**Next greater key** (ceiling). `bisect_left(vals, x)` is the index of the first value `>= x`. That is “what comes at or after this key?” `bisect_right` is strictly after (`>`).

```python
vals = [1, 3, 5, 8]
i = bisect.bisect_left(vals, 4)     # 2 → vals[2] is 5
i = bisect.bisect_left(vals, 5)     # 2 → 5 itself
i = bisect.bisect_left(vals, 9)     # 4 → past the end; no greater key
```

Interview shape: timestamps, prices, or compressed coordinates. “First slot at or after time t,” “smallest number ≥ target.” A dict cannot do this without scanning every key.

**Closest-key query.** Find the insertion point, then compare the neighbor on each side. The nearer of `vals[i - 1]` and `vals[i]` (when they exist) is the answer.

```python
def closest(vals, x):
    i = bisect.bisect_left(vals, x)
    candidates = []
    if i < len(vals):
        candidates.append(vals[i])       # next >= x
    if i > 0:
        candidates.append(vals[i - 1])   # previous < x
    return min(candidates, key=lambda v: (abs(v - x), v))

closest([1, 3, 5, 8], 4)    # 3  (ties: 3 and 5 are both distance 1; pick smaller)
closest([1, 3, 5, 8], 7)    # 8
```

`min(..., key=...)` still returns an **original candidate**, not the key. `key=` is only how Python decides which one is smallest.

For `candidates = [3, 5]` and `x = 4`:

| Candidate `v` | Distance `abs(v - 4)` | Key |
|---|---|---|
| `3` | `1` | `(1, 3)` |
| `5` | `1` | `(1, 5)` |

Tuples compare left to right: `1 == 1`, then `3 < 5`, so `3` wins. Result is `3`, not `(1, 3)`.

If distances differ, the second field never matters:

```python
# candidates [5, 8], x = 7
# 5 → (2, 5); 8 → (1, 8);  (1, 8) < (2, 5)  → 8
```

Why include `v` in the key at all? `min(candidates, key=lambda v: abs(v - x))` treats equal distances as a tie and keeps whichever candidate came **first**. `[5, 3]` would then return `5`. `(abs(v - x), v)` makes the tie-break “smaller value,” independent of order.

Same rule as `sort`/`sorted`/`max`: the key function is for comparison only.

```python
min(candidates, key=lambda v: (abs(v - x), v))   # original value 3
min((abs(v - x), v) for v in candidates)         # transformed tuple (1, 3)
```

Conceptually:

```python
best = candidates[0]
for v in candidates[1:]:
    if (abs(v - x), v) < (abs(best - x), best):
        best = v            # still an original candidate
```

Heaps do not help: the closest key is not the min or the max.

**Sliding-window median.** For a window of odd length k, the median is the middle value of the **sorted** window. As the window moves, one value leaves and one enters. Re-sorting from scratch each time is O(k log k) per step. Maintaining an ordered window lets you delete the leaving value and insert the new one, then read the middle.

```python
# nums = [1, 3, -1, -3, 5], k = 3
# window [1, 3, -1]  sorted [-1, 1, 3]   median 1
# window [3, -1, -3] sorted [-3, -1, 3]  median -1
# window [-1, -3, 5] sorted [-3, -1, 5]  median -1
```

```python
window = []
for x in [1, 3, -1]:
    bisect.insort(window, x)            # [-1, 1, 3]
median = window[len(window) // 2]       # 1

# slide: drop 1, add -3
i = bisect.bisect_left(window, 1)
del window[i]
bisect.insort(window, -3)               # [-3, -1, 3]
```

Why not a heap? A min-heap’s root is the smallest, not the middle. Two heaps (lo max-heap + hi min-heap) also work for medians; a `SortedList` is the same idea with less bookkeeping if the library is allowed. With only the stdlib, `bisect` on a list is the usual stand-in — find is O(log k), insert/delete are O(k).

| Question | Wrong tool | Right idea |
|---|---|---|
| Exact key present? | Sorted scan | `dict` / `set` |
| Current min / max? | Sorted map | Heap |
| First key `>= x`? | Dict or heap | `bisect_left` / sorted map |
| Nearest key to x? | Heap | Insertion point, then both neighbors |
| Median of a moving window? | Re-sort each step | Ordered window, or two heaps |

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

- `sort` vs `sorted`, `lambda` keys, tuple criteria with negation, and why `arr = arr.sort()` is wrong.
- Merge vs quick vs heap vs insertion, stability/space, and when counting/radix beat n log n.
- Unpacking, `enumerate`, `zip`, and chained comparisons.
- Queue vs deque vs dequeue, `append`/`popleft` for FIFO, and why `pop(0)` is O(n).
- Independent 2-D rows vs `[row] * n`, and 4-direction bounds checks.
- Shallow vs deep copy on `original = [1, [2, 3]]`.
- `Counter` vs `defaultdict` vs `dict` (`[]` inserts on defaultdict, returns 0 on Counter), tuple keys, `set` vs `frozenset`, and `list(dict.fromkeys(...))`.
- Min-heap vs max-heap, sift-up vs sift-down, O(n) `heapify`, and a size-k heap for top-k.
- `bisect` as the stdlib stand-in for a sorted map/set: next-greater key, closest key, sliding-window median.

Next: pick problems that force these tools — arrays/hashing, two pointers, sliding windows, stack, BFS with `deque`, and top-k with `heapq`.
