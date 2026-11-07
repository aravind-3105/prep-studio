# Cheat sheet

The rules that matter, one card per lesson. Open a lesson for the worked examples.

## Variables {1}

| Need | Remember |
|---|---|
| Assignment | Binds a name; does not copy the object |
| `b = a` then mutate | Both names see the change |
| Rebind `b = [9]` | Leaves `a` unchanged |
| Equality vs identity | `==` values; `is` for `None` |
| `a = b = []` | One shared list; use `a, b = [], []` |

## Math and Boolean operators {2}

| Need | Remember |
|---|---|
| True division | `7 / 2` is `3.5` |
| Floor division | `7 // 2` is `3`; `-7 // 2` is `-4` |
| Remainder identity | `a == (a // b) * b + a % b` |
| `and` / `or` | Return an operand, not always a Boolean |
| Floats | `0.1 + 0.2 == 0.3` is false; use `math.isclose` |

## Functions {3}

| Need | Remember |
|---|---|
| No `return` | Result is `None`; printing is not returning |
| Mutable default | Evaluated once at `def`; use `None` then `[]` |
| `*args` / `**kwargs` | Unnamed → tuple; named → dict |
| Lambda | `lambda p: (p[0], -p[1])` — one expression, no `return` |
| `key=fn` | Compares by the key; returns the original element |

## Conditional statements {4}

| Need | Remember |
|---|---|
| First true branch | `if` / `elif` chain takes only one |
| Falsy | `None`, `False`, `0`, empty string/container |
| Check absence | `if value is not None` when zero/empty is legal |
| Trap | `if x == 1 or 2` is always true; use `x in (1, 2)` |
| Scope | `if` / `for` do not create a local scope |

## Loops {5}

| Need | Remember |
|---|---|
| Index + value | `for i, x in enumerate(arr)` |
| Two lists | `for x, y in zip(a, b)` — stops at shorter |
| Index + two lists | `for i, (x, y) in enumerate(zip(a, b))` |
| Ordered uniques | `list(dict.fromkeys(values))` |
| `range` stop | Excluded; backward including 0 is `range(n-1, -1, -1)` |

## Strings {6}

| Need | Remember |
|---|---|
| Immutable | `s[0] = 'P'` is `TypeError`; build a new string |
| Slice vs index | Slice clips; `s[99]` is `IndexError` |
| Join | Accumulate in a list, then `"".join(parts)` |
| Find vs index | `find` → `-1`; `index` → `ValueError` |
| Cost | Slice of length k is O(k) |

## Lists and tuples {7}

| Need | Remember |
|---|---|
| `append` vs `extend` | One object vs each element |
| `sort` vs `sorted` | In place / `None` vs new list |
| Shared rows | `[[0]*3]*2` is one row twice |
| Shallow copy | New outer list, same nested objects |
| Deep copy | `copy.deepcopy` for nested independence |
| Front of list | `pop(0)` / `insert(0)` are O(n) |

## Sets {8}

| Need | Remember |
|---|---|
| Unique + fast `in` | `set` — order not guaranteed |
| Ordered unique | `list(dict.fromkeys(values))` |
| `remove` vs `discard` | Missing → `KeyError` vs silent |
| `frozenset` | Immutable and hashable (undirected edges) |
| Hashable elements | No lists/dicts/sets inside a set |

## Dictionaries {9}

| Need | Remember |
|---|---|
| Missing `d[k]` | `KeyError` |
| Missing `d.get(k)` | Default, does not insert |
| `Counter` | Counts an iterable; missing reads as `0`, not inserted |
| `defaultdict(list)` | `[]` inserts the default; `.get` does not |
| Frequencies | `Counter`; grouping → `defaultdict(list)` |
| Unique neighbors | `defaultdict(set)` |

## Reading stdin {10}

| Need | Remember |
|---|---|
| `input()` | Always a string |
| Ints on a line | `list(map(int, input().split()))` |
| EOF | `input()` raises `EOFError` |
| Interview platforms | Follow the given signature; parse stdin only if required |

## Exception handling {11}

| Need | Remember |
|---|---|
| `else` | Runs only if `try` had no exception |
| `finally` | Always, including before a pending `return` |
| `raise` vs `return` | Cannot finish vs finished with a value |
| `raise ... from exc` | New message, original kept as cause |
| Trap | No `except Exception: pass`; no `return` in `finally` |

## Costs to remember {12}

| Operation | Time |
|---|---|
| List index / `append` / `pop()` | O(1) |
| List `pop(0)`, `in`, insert front | O(n) |
| `sort` / `sorted` | O(n log n) |
| Dict / set lookup | O(1) average |
| `deque` either end | O(1) |
| `heappush` / `heappop` | O(log n) |
| `heapify` | O(n) |
| `bisect` find / `insort` | O(log n) / O(n) |

## Sorting {i1}

| Need | Remember |
|---|---|
| In place | `arr.sort()` — do not assign it |
| Copy | `sorted(arr)` |
| First asc, second desc | `key=lambda p: (p[0], -p[1])` |
| `key=` | Ascending keys; returns original items |
| Python's sort | Timsort — stable, O(n log n) |
| Always n log n | Merge sort; extra O(n), stable |
| Fast average | Quicksort; worst O(n²), usually not stable |
| Small integers | Counting / radix can beat n log n |

## Pythonic code {i2}

| Need | Remember |
|---|---|
| Swap | `a, b = b, a` |
| Unpack rest | `first, *rest = arr` |
| Chained compare | `0 <= i < n` |
| `min` / `max` with `key` | Original element, not the key tuple |
| Closest on a tie | `min(vals, key=lambda v: (abs(v-x), v))` |

## Lists {i3}

| Need | Remember |
|---|---|
| Dynamic array | End ops O(1); front ops O(n) |
| Clone | `arr[:]` is shallow |
| Nested mutate | Shallow copy shares inner lists |
| Comprehension | New list; loop if you only iterate |

## Stacks and queues {i4}

| Need | Remember |
|---|---|
| Queue | FIFO rule; enqueue add, dequeue remove |
| Deque | Structure (said “deck”); both ends O(1) |
| FIFO in Python | `append` + `popleft` |
| LIFO / stack | `append` + `pop` (list is fine) |
| Trap | `list.pop(0)` is O(n) |
| BFS | Queue so nodes process in discovery order |

## 2-D lists {i5}

| Need | Remember |
|---|---|
| Independent rows | `[[0]*cols for _ in range(rows)]` |
| Shared rows | `[[0]*cols]*rows` — one inner list |
| Index | `grid[r][c]` — row, then column |
| Neighbors | Four dirs + `0 <= nr < rows and 0 <= nc < cols` |

## Hash maps and hash sets {i6}

| Need | Remember |
|---|---|
| Visited cell | Tuple `(r, c)` — not a list |
| Anagram | `Counter(s) == Counter(t)` |
| Group indices | `defaultdict(list)` |
| Adjacency unique | `defaultdict(set)` |
| Duplicate in array | `len(nums) != len(set(nums))` |

## Heaps and priority queues {i7}

| Need | Remember |
|---|---|
| Heap | Partial order, not a sorted list |
| Insert | Sift-up O(log n) |
| Pop root | Sift-down O(log n) |
| Build | `heapify` O(n), bottom-up down |
| Max-heap | Negate; pop then negate |
| K largest | Size-k **min**-heap, O(n log k) |
| K smallest | Size-k max-heap |

## Sorted dicts and sorted sets {i8}

| Need | Remember |
|---|---|
| Exact key | `dict` / `set` |
| Min / max repeatedly | Heap |
| First key `>= x` | `bisect_left` |
| Closest key | Insertion point, then both neighbors |
| Window median | Keep the window ordered (or two heaps) |
| Stdlib stand-in | Sorted list + `bisect`; insert is O(n) |

## RAM {d1}

| Need | Remember |
|---|---|
| Index `i` | Address = `base + i * size` — that is why O(1) |
| Contiguous | Elements sit next to each other |
| Linked get `i` | No formula; walk `i` pointers, O(n) |
| Python list | Array of **pointers**, not inline C ints |
| RAM | Any address in O(1) |

## Static arrays {d2}

| Need | Remember |
|---|---|
| Capacity | Fixed at creation; insert fails if full |
| get / set | O(1) |
| Insert / delete at `i` | Shift the tail, O(n) |
| Insert at end | O(1) if there is room |
| Shift direction | Insert: right to left; delete: left to right |
| Python `list` | Not static |

## Dynamic arrays {d3}

| Need | Remember |
|---|---|
| Grow | Double when full (interview model) |
| `append` | Amortized O(1); a resize is still O(n) that call |
| Why double | Grow-by-1 copies `0+1+…+n` = O(n²) total |
| Insert / pop front | Still O(n) — shifting |
| Python `list` | Dynamic array |

## Stacks {d4}

| Need | Remember |
|---|---|
| Rule | LIFO — last in, first out |
| Python | `append` / `pop` / `stack[-1]` |
| Trap | `pop(0)` is the bottom, O(n) |
| Empty peek | `if stack:` before `stack[-1]` |
| Call stack | Each call pushes a frame; return pops |
| Parentheses | Push openers; pop on matching closer |

## Singly linked lists {d5}

| Need | Remember |
|---|---|
| Node | `val` + `next`; last `next` is `None` |
| get `i` | O(n) — walk from `head` |
| Insert at head | O(1) |
| Delete | Need the **previous** node |
| Dummy | `dummy.next = head` so head-delete is the same code |
| Reverse | `prev, cur, nxt` — save `nxt` before flipping |

## Doubly linked lists {d6}

| Need | Remember |
|---|---|
| Extra | `prev` as well as `next` |
| Delete known node | O(1) — relink neighbors |
| Tail pointer | Append / pop-tail become O(1) |
| Cost | One more reference per node |
| Use | LRU cache, `deque` internals |

## Queues {d7}

| Need | Remember |
|---|---|
| Rule | FIFO — enqueue back, dequeue front |
| Wrong | `list.pop(0)` is O(n) |
| Circular buffer | `(front + size) % cap`; both ends O(1) |
| Linked queue | Head + tail pointers |
| Python | `deque.append` / `popleft` |
| BFS | Queue so discovery order is FIFO |

## Recursion {d8}

| Need | Remember |
|---|---|
| Two pieces | Base case + smaller recursive case |
| Factorial | O(n) time, O(n) stack; a loop is O(1) extra |
| Naive `fib` | Duplicate tree; `fib(8)` is 67 calls for 21 |
| Memoization | Cache answers; not a replacement for recursion |
| `fib(8)` memo | 15 calls; each `n` computed once, O(n) |
| `@cache` | `functools.cache` (or `lru_cache`) |
| When to cache | Only if the same subproblem repeats |
| Mutable default | `memo=None`, not `memo={}` |

## Insertion sort {d9}

| Need | Remember |
|---|---|
| Idea | Sorted prefix; insert the next key into it |
| Shift | Right while `arr[j] > key` (strict `>` is stable) |
| Best | Already sorted → O(n) |
| Worst | Reverse sorted → O(n²) |
| Space | O(1), in-place |
| Use | Tiny n, nearly sorted runs (Timsort) |

## Merge sort {d10}

| Need | Remember |
|---|---|
| Idea | Split in half, merge two sorted lists |
| Merge | Take the smaller head; `<=` keeps it stable |
| Time | Always O(n log n) — log n levels × n work |
| Space | O(n) extra |
| Linked lists | Natural fit: rewire `next`, no index math |

## Quick sort {d11}

| Need | Remember |
|---|---|
| Idea | Partition around a pivot; recurse both sides |
| Lomuto | Pivot at `hi`; swap small values left; swap pivot into `i` |
| Recurse | `p-1` and `p+1` — not `p`, or you loop |
| Average | O(n log n) |
| Worst | O(n²) if pivot is always min or max |
| Fix | Random pivot or median-of-three |
| Stable | No, for the in-place version |

## Bucket sort {d12}

| Need | Remember |
|---|---|
| Comparison lower bound | Cannot beat O(n log n) worst case |
| Counting | Integers `0..k` → O(n + k) |
| Bucket | Scatter, insertion-sort each, concatenate |
| Radix | Stable counting per digit, LSD first |
| Trap | Huge k makes counting worse than n log n |

## Binary search {d13}

| Need | Remember |
|---|---|
| Need | Sorted array |
| Invariant | If present, it is in `arr[lo..hi]` inclusive |
| Loop | `while lo <= hi` |
| Shrink | `lo = mid+1` or `hi = mid-1` (must move) |
| Missing | `lo > hi` → not found |
| Duplicates | Returns *an* index, not first or last |

## Search range {d14}

| Need | Remember |
|---|---|
| `bisect_left` | First index with `arr[i] >= x` |
| `bisect_right` | First index with `arr[i] > x` |
| Window | Half-open: `lo < hi`, `hi = len`, `hi = mid` |
| Count of `x` | `right - left` |
| Last index | `right - 1` if `left < right` |
| First True | Same loop on a monotonic predicate |

## Binary trees {d15}

| Need | Remember |
|---|---|
| Node | `val`, `left`, `right` — no order yet |
| Leaf | Both children `None` |
| Height | Longest down-path; a leaf is 0 if empty is −1 |
| Skewed | One child each time → height n−1, like a list |
| Complete array | Left `2i+1`, right `2i+2` |
| Cost | Walk is O(n); stack O(h) |

## Binary search trees {d16}

| Need | Remember |
|---|---|
| Invariant | Whole left `<` node `<` whole right |
| Search | Compare, go left or right, O(h) |
| Inorder | Sorted keys |
| Min / max | Leftmost / rightmost |
| Validate | Range `(lo, hi)`, not just two children |
| Balanced | h = Θ(log n); skewed h = n |

## BST insert and remove {d17}

| Need | Remember |
|---|---|
| Insert | Walk to `None`, attach, O(h) |
| 0 children | Parent pointer → `None` |
| 1 child | Parent pointer → that child |
| 2 children | Copy inorder successor (min of right), then delete it |
| Successor | Has no left child, so its delete is case 0 or 1 |

## Tree DFS {d18}

| Need | Remember |
|---|---|
| Preorder | Node, left, right |
| Inorder | Left, node, right (sorted on a BST) |
| Postorder | Left, right, node |
| Recursion | Call stack *is* the DFS stack |
| Iterative pre | Stack; push **right then left** |
| Time / space | O(n) / O(h) |

## Tree BFS {d19}

| Need | Remember |
|---|---|
| Order | Level by level |
| Structure | Queue (`deque`), not a stack |
| Per level | `for _ in range(len(q))` |
| Shortest path | BFS level in an unweighted tree/graph |
| Trap | `pop(0)` or `stack.pop()` is not BFS |

## BST sets and maps {d20}

| Need | Remember |
|---|---|
| Hash set / dict | Fast, unordered |
| BST | Ordered; min, successor, range |
| First `>= x` | Walk, remember last `>= x`, go left |
| Python | No stdlib balanced BST; `bisect` on a list inserts in O(n) |
| Map | Same tree, payload on the key |

## Backtracking {d21}

| Need | Remember |
|---|---|
| Template | Choose, explore, unchoose |
| Maze | Mark `(r, c)`, recurse, **unmark** |
| Subsets | `path.append`, recurse, `path.pop` |
| Copy | `out.append(path[:])` not `path` |
| Grid | Bounds, wall, tuple key, then index |

## Heap properties {d22}

| Need | Remember |
|---|---|
| Shape | Complete binary tree in an array — no holes |
| Indexes | Parent `(i-1)//2`; left `2i+1`; right `2i+2` |
| Min-heap | Parent `<=` both children; root is min |
| Not sorted | Only the root is the extreme |
| Height | Always `⌊log n⌋` (complete, cannot skew) |
| vs BST | Heap: fast min. BST: search / order |

## Heap push and pop {d23}

| Need | Remember |
|---|---|
| Push | Append, then **sift-up** |
| Pop | Swap with last, pop, **sift-down** |
| Peek | `heap[0]` — do not pop |
| Time | O(log n) each |
| Max-heap | Negate, or flip the comparisons |
| Trap | Sift the wrong direction; mutate `heap[i]` by hand |

## Heapify {d24}

| Need | Remember |
|---|---|
| What | Unsorted list → heap, in place |
| How | Sift-down from last parent `n//2-1` to 0 |
| Time | O(n), not O(n log n) |
| Why O(n) | Most nodes sit near the leaves (height 0 or 1) |
| After | `a[0]` is min; the rest is not sorted |
| n pushes | That build *is* O(n log n) |

## Hash usage {d25}

| Need | Remember |
|---|---|
| Job | Exact-key membership / map, O(1) average |
| Worst | O(n) if every key collides |
| Key | Must be hashable — tuple `(r, c)`, not a list |
| Two-sum | `value → index` while you walk |
| Not for | Next larger key, min/max repeatedly |
| `in` on a list | O(n) — do not put it in a loop |

## Hash implementation {d26}

| Need | Remember |
|---|---|
| Index | `hash(key) % m` |
| Collision | Two keys, same bucket — normal |
| Chaining | List per bucket; scan the chain |
| Load factor | `n/m`; rehash (double) when it grows |
| Open addressing | Probe the next slot (CPython dict) |
| Rehash | New table, re-insert every pair |

## Intro to graphs {d27}

| Need | Remember |
|---|---|
| Graph | Nodes + edges; a tree is the acyclic connected case |
| Directed | One-way edges; in-degree / out-degree |
| Adj list | Default; space O(n + e) |
| Adj matrix | O(1) edge check; space O(n²) |
| Grid | Implicit graph; 4-dir neighbors |
| Cost | Always name n **and** e |

## Matrix DFS {d28}

| Need | Remember |
|---|---|
| Island / flood | DFS from each unvisited land cell |
| Mark | In place or `seen`; do **not** unmark |
| Bounds | Check before `grid[r][c]` |
| Key | `(r, c)` tuple |
| Count | +1 per new start, not per cell |
| Time | O(rows · cols) |

## Matrix BFS {d29}

| Need | Remember |
|---|---|
| Use | Unweighted shortest path in a grid |
| Queue | `(r, c, dist)` or level-size loop |
| Mark | When you **enqueue**, not when you pop |
| Multi-source | All starts in the queue at dist 0 |
| Trap | DFS is not shortest; weighted needs Dijkstra |

## Adjacency lists {d30}

| Need | Remember |
|---|---|
| Build | Undirected: add `u→v` **and** `v→u` |
| `seen` | Required — graphs have extra edges / cycles |
| Cycle (undirected) | Neighbor already seen and not the parent |
| Components | How many times you start a DFS/BFS |
| Topo (DAG) | Kahn: indegree 0 queue; `len < n` means a cycle |
| Time | O(n + e) |

## 1-D DP {d31}

| Need | Remember |
|---|---|
| When | Overlapping subproblems **and** optimal substructure |
| Top-down | Memoized recursion (`@cache` / dict) |
| Bottom-up | Fill a `dp` table / rolling variables |
| Four sentences | State, base, transition, fill order |
| Stairs / Fibonacci | `dp[i] = dp[i-1] + dp[i-2]` |
| House robber | `max(skip, take + dp[i-2])` |
| Coin change | `dp[a] = min coins`; greedy can fail |
| Time | States × work per state |

## 2-D DP {d32}

| Need | Remember |
|---|---|
| Unique paths | `dp[r][c] = top + left`; first row/col = 1 |
| LCS | Match → diagonal + 1; else max of top/left |
| 0/1 knapsack | Each item once; inner `w` **down** |
| Unbounded | Inner `w` **up** so the item can repeat |
| Rows | `[[0]*cols for _ in range(rows)]` |
| Draw | Fill a 3×3 table by hand first |

## Bit operations {d33}

| Need | Remember |
|---|---|
| AND / OR / XOR | Both 1 / either 1 / differ |
| Python `~n` | `-n-1`, not a 32-bit NOT |
| Last bit / drop it | `n & 1`, `n >> 1` |
| Drop lowest 1 | `n & (n-1)` |
| Power of two | `n > 0` and `n & (n-1) == 0` |
| Unique in pairs | XOR everything |

## DSA costs so far {d34}

| Structure / operation | Time |
|---|---|
| Array get / set | O(1) |
| Array insert / delete at `i` | O(n) |
| Dynamic `append` / `pop()` | Amortized O(1) |
| Stack push / pop | O(1) |
| Singly get `i` / reverse | O(n) |
| Singly insert head | O(1) |
| Doubly delete known node | O(1) |
| Queue (`deque` / ring / two-end list) | O(1) |
| Naive `fib(n)` | Θ(φ^n) |
| Insertion sort | O(n²) / O(n) best |
| Merge sort | O(n log n) always |
| Quicksort | O(n log n) avg, O(n²) worst |
| Counting sort | O(n + k) |
| Binary search / `bisect` | O(log n) |
| Tree DFS / BFS | O(n) |
| BST search / insert / delete | O(h) |
| Backtracking subsets | O(2^n · n) |
| Heap peek | O(1) |
| Heap push / pop | O(log n) |
| `heapify` | O(n) |
| Hash lookup | O(1) avg, O(n) worst |
| Adj list DFS / BFS | O(n + e) |
| Grid DFS / BFS | O(rows · cols) |
| Kahn topo | O(n + e) |
| 1-D DP (stairs, rob) | O(n) |
| Coin change | O(amount · coins) |
| LCS / unique paths | O(m · n) |
| 0/1 knapsack | O(n · cap) |
