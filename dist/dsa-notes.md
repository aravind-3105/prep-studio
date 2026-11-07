# Algorithms and data structures — revision

Based on NeetCode *Algorithms & Data Structures for Beginners* (full course: Arrays through Bit operations). Examples use Python 3. This is the structure-and-algorithm layer after the Python-tools track. You already know `list`, `deque`, `sort`/`sorted`, and `bisect` as APIs. These notes explain what those structures *are*, why the costs look the way they do, and how to implement the operations by hand.

Read in the order below. For every snippet, be able to say what it returns, what it mutates, and the time/space cost. Question practice comes after you can explain each structure without the notes.

## 1. RAM

Interviews treat memory as a giant array of **bytes**. Each byte has an integer **address**. RAM means the CPU can read or write any address in O(1) — you do not scan from address 0 to find address 1000.

A value larger than one byte occupies consecutive addresses. A 32-bit integer is 4 bytes; a 64-bit integer is 8. If a 4-byte integer starts at address 1000, it occupies 1000–1003.

### Why array indexing is O(1)

An array stores elements of a known size **contiguously** (back to back). If the first element starts at `base` and each element is `size` bytes:

```
address of index i  =  base + i * size
```

No loop. The CPU computes the address and reads it.

```python
# Mental model, not Python syntax:
# base = 1000, size = 4 (a 32-bit int)
# arr[0] lives at 1000
# arr[1] lives at 1004
# arr[3] lives at 1012
```

That formula is the whole reason `arr[i]` is O(1) and `linked_list.get(i)` is O(n). A linked list has no `base + i * size` — you must walk `i` pointers.

**Cost:** random access in an array is O(1) because of address arithmetic, not because the computer “knows” the value.

### Contiguous vs scattered

```
Array of 4 ints at base 1000:

1000 [ 7 ] 1004 [ 3 ] 1008 [ 9 ] 1012 [ 1 ]
      arr[0]     arr[1]     arr[2]     arr[3]
```

The next element is always `size` bytes away. That is also why arrays have good **cache locality**: loading `arr[0]` often pulls neighbors into the CPU cache, so a linear scan is fast in practice, not only in Big-O.

A linked list stores nodes wherever the allocator put them. Walking `node.next` can jump across memory. Same O(n) walk, worse constants.

### What Python actually stores

A C array of `int` stores the integers themselves. A **Python list stores pointers** (references) to objects. `nums = [7, 3, 9]` is a contiguous array of addresses, each address pointing at an `int` object elsewhere.

```python
nums = [7, 3, 9]
# nums[0], nums[1], nums[2] sit next to each other in the list's buffer.
# The objects 7, 3, 9 live on the heap. The list holds pointers to them.
```

That is why `nums[i] = 4` is still O(1) (overwrite one pointer) and why `b = a` still aliases the same list object — the RAM model did not replace the reference rules from the Python track.

**Trap:** do not say “a Python list of ints is an array of 4-byte integers.” It is an array of pointers. Interviews still use the C-array model when they ask “why is indexing O(1)?” Answer with `base + i * size`. Then, if they ask about Python, add that the “elements” are pointers of a fixed size, so the same formula applies.

### Bits, bytes, and word size (just enough)

| Unit | Size |
|---|---|
| Bit | 0 or 1 |
| Byte | 8 bits |
| 32-bit word | 4 bytes |
| 64-bit word | 8 bytes |

A 64-bit process uses 8-byte pointers. That is why a Python list of `n` objects needs on the order of `8n` bytes for the pointer buffer, plus the objects themselves.

You do not need to compute heap layouts in an interview. You do need: **address arithmetic, contiguous layout, O(1) index, O(n) to walk something without indexes.**

## 2. Static arrays

A **static array** has a length that is fixed when it is created. Capacity never changes. You can read and write existing slots. You cannot grow past the allocated size.

Python’s `list` is *not* static (next lesson). Interviews still want the static-array costs, because that is the building block, and because languages like C and Java (`int[]`) expose it directly.

Teaching model: a buffer plus a `length` that counts how many slots are in use. Capacity is the allocated size. `length <= capacity`.

```python
class StaticArray:
    def __init__(self, capacity):
        self.data = [None] * capacity   # the buffer
        self.capacity = capacity
        self.length = 0                 # how many are in use
```

### Get and set — O(1)

```python
def get(self, i):
    if i < 0 or i >= self.length:
        raise IndexError
    return self.data[i]

def set(self, i, value):
    if i < 0 or i >= self.length:
        raise IndexError
    self.data[i] = value
```

`get` / `set` use the RAM formula. Bounds-check is O(1). Out of range is an error, not a wrap.

### Insert at the end — O(1) if there is room

```python
def push(self, value):
    if self.length == self.capacity:
        raise OverflowError("array is full")
    self.data[self.length] = value
    self.length += 1
```

Walkthrough, capacity 4:

```
[]                 length 0
push 4  →  [4]     length 1
push 5  →  [4, 5]
push 6  →  [4, 5, 6]
push 7  →  [4, 5, 6, 7]   now full
push 8  →  OverflowError
```

### Insert in the middle — O(n), because of shifting

To insert `9` at index `1` in `[4, 5, 6]` (capacity 5), every element from index 1 onward must move one slot **right**, or `5` would be overwritten.

```
before:  [4, 5, 6, _, _]   length 3
shift 6: [4, 5, 6, 6, _]
shift 5: [4, 5, 5, 6, _]
write 9: [4, 9, 5, 6, _]   length 4
```

Shift from the **end**, otherwise you overwrite values you still need.

```python
def insert(self, i, value):
    if self.length == self.capacity:
        raise OverflowError("array is full")
    if i < 0 or i > self.length:
        raise IndexError
    for j in range(self.length, i, -1):    # right to left
        self.data[j] = self.data[j - 1]
    self.data[i] = value
    self.length += 1
```

Worst case: insert at index 0, shift `n` elements → O(n). Best case: insert at `length` (a `push`) → O(1).

### Delete — also O(n), shift the other way

Delete index 1 from `[4, 9, 5, 6]`:

```
before:  [4, 9, 5, 6, _]   length 4
shift:   [4, 5, 6, 6, _]   copy left
length:  [4, 5, 6, _, _]   length 3; leftover 6 is unused
```

```python
def remove(self, i):
    if i < 0 or i >= self.length:
        raise IndexError
    for j in range(i, self.length - 1):
        self.data[j] = self.data[j + 1]
    self.length -= 1
```

`remove` at the end is O(1): decrement `length`. `remove` at 0 is O(n).

**Trap:** the leftover slot after a delete still holds an old value. Length is what makes it unused. If you iterate `range(capacity)` instead of `range(length)`, you will read garbage.

### Static-array costs

| Operation | Time | Why |
|---|---|---|
| get / set index | O(1) | Address arithmetic |
| insert / remove at end | O(1) | Write a slot, change length |
| insert / remove at i | O(n) | Must shift the tail |
| search by value | O(n) | No index for values |

Space is Θ(capacity), even if `length` is smaller. That wasted room is the price of a fixed buffer.

**Interview rule:** when someone says “array insert is O(n),” they mean insert in the middle or at the front, which shifts. End-insert on a static array is O(1) until it is full, and then it is impossible.

## 3. Dynamic arrays

A **dynamic array** is a static array that **grows** when it runs out of room. Python `list`, Java `ArrayList`, and C++ `vector` are dynamic arrays.

Growth strategy interviews assume: when `length == capacity`, allocate a **new** buffer of twice the capacity, copy every element, then append. That copy is O(n) *on that one call*. Across a sequence of appends it averages out.

### Why doubling is amortized O(1)

Start empty, capacity 1. Append 1 through 8. Resizes happen when the buffer is full, just before the next write.

```
append 1:  cap 1 → [1]
append 2:  full, new cap 2, copy [1], write 2     copies: 1
append 3:  full, new cap 4, copy [1, 2], write 3  copies: 2
append 4:  [1, 2, 3, 4]                           copies: 0
append 5:  full, new cap 8, copy 4, write 5       copies: 4
append 6, 7, 8: no resize
```

Copies so far: `1 + 2 + 4 = 7`. After `n` appends with doubling, total copies are `1 + 2 + 4 + … + n/2 < n`. Total work for `n` appends is O(n). **Average (amortized) cost per append is O(1).**

The expensive append that doubles still takes O(n) *that time*. Amortized does not mean every append is O(1); it means n appends together are O(n).

### Why not grow by 1

If each full append allocated `capacity + 1` and copied everything:

```
n appends copy 0 + 1 + 2 + … + (n-1) = n(n-1)/2  →  O(n²)
```

Geometric growth (×2, or ×1.5) is the difference between “append is cheap” and “append is quadratic.”

**Trap:** “Python append is O(1)” is the amortized statement. A single `append` that triggers a resize is O(n). You will not feel it in an interview solution; you *will* lose points if you say every append is strictly O(1) with no hedge.

CPython does not always double. It overallocates by a geometric factor (around 1.125 for large lists). Interviews want doubling. Mention the real factor only if asked.

### Insert and delete are still O(n) in the middle

Resizing only helps **end** operations. Insert at index `i` still shifts `n - i` elements, then may also resize. Delete at `i` still shifts. `list.insert(0, x)` and `list.pop(0)` are O(n). That is the same trap as in the Python-tools track; now you can say *why*: shifting in a contiguous buffer.

```python
nums = [4, 5, 6]
nums.append(7)       # amortized O(1)  → [4, 5, 6, 7]
nums.pop()           # O(1)            → [4, 5, 6]
nums.insert(0, 9)    # O(n)            → [9, 4, 5, 6]
nums.pop(0)          # O(n)            → [4, 5, 6]
```

### Teaching implementation

```python
class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.length = 0
        self.data = [None] * self.capacity

    def append(self, value):
        if self.length == self.capacity:
            self._resize()
        self.data[self.length] = value
        self.length += 1

    def _resize(self):
        self.capacity *= 2
        new = [None] * self.capacity
        for i in range(self.length):
            new[i] = self.data[i]
        self.data = new
```

`_resize` is O(n). `append` is amortized O(1). Index get/set stay O(1).

### Dynamic-array costs

| Operation | Time | Notes |
|---|---|---|
| get / set index | O(1) | Same as static |
| append / `pop()` | Amortized O(1) | Occasional O(n) resize |
| `pop()` from end | O(1) | No shift |
| insert / pop at i | O(n) | Shift, maybe resize |
| search by value | O(n) | Unless sorted + binary search |

Space: Θ(n), with up to a constant factor of unused capacity (at most about half just after a doubling).

**Interview rule:** Python `list` is a dynamic array. Use it for random access, append, and pop from the end. Do not use it as a queue. When you need a stack, `append`/`pop` on a list *is* the right structure.

## 4. Stacks

A **stack** is LIFO: last in, first out. The only interesting end is the **top**. Push adds to the top; pop removes from the top; peek reads the top without removing.

A plate stack is the usual picture. The last plate you set down is the first you pick up.

A dynamic array already gives you a stack: the end of the list *is* the top.

```python
stack = []
stack.append(1)         # push
stack.append(2)
stack.append(3)
# [1, 2, 3]  ← top is 3
stack[-1]               # peek → 3
stack.pop()             # → 3
stack.pop()             # → 2
```

| Operation | List | Time |
|---|---|---|
| push | `append(x)` | Amortized O(1) |
| pop | `pop()` | O(1) |
| peek | `stack[-1]` | O(1) |
| empty | `if not stack` | O(1) |

**Trap:** `stack.pop(0)` is not a stack pop. That removes the *bottom* and shifts, O(n). `stack[-1]` on an empty list is `IndexError` — check `if stack:` first.

### Call stack (this is a real stack)

Every function call pushes a **frame**: locals, parameters, and “where to resume.” Return pops the frame. Recursion (next section) is this mechanism calling itself. Infinite recursion blows the stack (`RecursionError` in Python).

```python
def outer():
    x = 1
    inner()          # push inner's frame; outer waits
    return x         # resumes after inner pops

def inner():
    y = 2
    return y
```

While `inner` runs, `outer`’s `x` is still on the stack, just not the top frame.

### Worked example: valid parentheses

Push opening brackets. On a closer, the top must be the matching opener.

```python
def is_valid(s):
    match = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack or stack[-1] != match[ch]:
                return False
            stack.pop()
    return not stack
```

Trace `"([)]"`:

```
(      stack ['(']
([     stack ['(', '[']
([)    closer ) needs (, top is [  → False
```

Trace `"([])"`:

```
(      ['(']
([     ['(', '[']
([]    pop [  → ['(']
([])   pop (  → []     empty at the end → True
```

Leftover openers (`"("`) fail the final `not stack`. A closer when the stack is empty (`")"` ) fails immediately.

### Where stacks show up

- Undo, browser back, nested structures, function calls
- Monotonic stack (next greater element) — later practice
- DFS can be recursive (call stack) or an explicit `stack` of nodes

**Interview rule:** if the problem is “the most recent unfinished thing has to finish first,” it is a stack. Implement it with a list. Do not import anything.

## 5. Singly linked lists

A **singly linked list** is a chain of nodes. Each node holds a value and a pointer to the **next** node. The list is the pointer to the first node (`head`). The last node’s `next` is `None`.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 1 → 2 → 3 → None
head = ListNode(1, ListNode(2, ListNode(3)))
```

There is **no index formula**. `get(i)` walks `i` steps from `head`. That is O(i), worst case O(n).

```python
def get(head, i):
    cur = head
    for _ in range(i):
        if cur is None:
            raise IndexError
        cur = cur.next
    if cur is None:
        raise IndexError
    return cur.val
```

### Insert at the head — O(1)

You already have `head`. Point the new node at the old head, then move `head`.

```
head → 2 → 3
insert 1 at head:
  node=1, node.next=head, head=node
head → 1 → 2 → 3
```

```python
def insert_head(head, val):
    return ListNode(val, head)
```

No shifting. That is the linked-list advantage over arrays for front inserts.

### Insert after a known node — O(1)

If you already hold node `A`, splicing `X` after it is two pointer writes:

```
A → C
A → X → C
```

```python
def insert_after(node, val):
    node.next = ListNode(val, node.next)
```

Finding that node is usually O(n). The splice itself is O(1). Interviews distinguish those.

### Delete — you need the *previous* node

To delete `B` in `A → B → C`, you must set `A.next = C`. You cannot ask `B` who came before it. A singly linked node does not store `prev`.

```python
def delete_value(head, val):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == val:
            prev.next = prev.next.next
            break
        prev = prev.next
    return dummy.next
```

The **dummy node** (`0 → original head`) makes “delete the head” the same code as “delete the middle.” Without it you special-case `if head.val == val: return head.next`.

**Trap:** `cur = cur.next.next` without a `prev` loses the only pointer to `cur.next` if you still needed it. Always keep a predecessor, or keep `prev` and `cur` together.

### Reverse a singly linked list

This is the standard pointer walk. Three names: `prev`, `cur`, `nxt`.

```python
def reverse(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # save the rest
        cur.next = prev     # flip this arrow
        prev = cur          # advance
        cur = nxt
    return prev             # new head
```

Trace `1 → 2 → 3`:

```
start     prev=None  cur=1 → 2 → 3
after 1   prev=1 → None    cur=2 → 3
after 2   prev=2 → 1 → None    cur=3
after 3   prev=3 → 2 → 1 → None    cur=None
return 3
```

Save `nxt` **before** flipping `cur.next`, or you lose the rest of the list.

### Singly-list costs

| Operation | Time | Notes |
|---|---|---|
| get / set index i | O(n) | Walk from head |
| insert / delete at head | O(1) | Pointer change |
| insert / delete at tail | O(n) | Unless you store a tail pointer (insert only) |
| insert after a known node | O(1) | Finding the node is extra |
| delete a known node | O(n) | Need the predecessor |
| search by value | O(n) | Linear walk |
| reverse | O(n) time, O(1) extra | The three-pointer walk |

A tail pointer makes **append** O(1), but **pop from tail** is still O(n) in a singly list: you must find the node *before* the tail.

**Interview rule:** draw the arrows. Then write the pointer assignments. Do not try to hold the whole list in your head as values only.

## 6. Doubly linked lists

Each node has `val`, `next`, **and** `prev`. You can walk either direction. Delete no longer needs a separate predecessor hunt: `node.prev` *is* the predecessor.

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

### Delete a known node in O(1)

```
A ⇄ B ⇄ C     delete B
A ⇄ C         A.next = C, C.prev = A
```

```python
def delete_node(node):
    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev
```

You still have to be careful at the head and tail (the `if`s above). A dummy head *and* dummy tail make every real node look like a middle node, which is why LRU-cache implementations use sentinels.

### Head and tail pointers

Store both ends:

- insert/delete at head: O(1)
- insert/delete at tail: O(1)  ← this is the singly-list gap
- walk either way: O(n)

```python
# append at tail, given tail pointer
def append(tail, val):
    node = DListNode(val, prev=tail, next=None)
    tail.next = node
    return node          # new tail
```

### Cost of the extra pointer

Each node stores two references instead of one. More memory per element. For interview-size n that rarely matters; the reason to mention it is to explain *why* people still use singly lists (simpler, enough for reverse/merge/cycle).

### Where it shows up

- LRU cache: hashmap from key → node, doubly list for recency. Hash gives O(1) lookup; the list gives O(1) move-to-front and O(1) evict-from-tail.
- `deque` is implemented as a doubly linked block structure. That is why both ends are O(1).
- Browser history, some text-editor buffers

**Trap:** after deleting `B`, do not walk through `B.next` expecting the old chain unless you saved it. After splicing, `B.prev` / `B.next` may still point at A and C; the *list* no longer goes through B. Clear them if the node might be reused.

**Interview rule:** if you must delete in O(1) given only the node, you need `prev` (doubly) or a trick (copy the next node’s value into this node — works only if it is not the tail). Prefer the doubly-list answer unless they constrain you to singly.

## 7. Queues

A **queue** is FIFO: first in, first out. Enqueue adds at the **back**. Dequeue removes from the **front**. A coffee line: the person who arrived first is served first.

You already use `collections.deque` for this (`append` / `popleft`). This lesson is the implementations underneath, and why a list is the wrong one.

### Why a list is the wrong queue

```python
q = []
q.append(1)             # enqueue, amortized O(1)
q.append(2)
q.pop(0)                # dequeue, O(n) — every remaining element shifts
```

n enqueues and n dequeues on a list cost O(n²). That is the same shift you traced in static arrays.

### Circular buffer (array queue)

Keep a fixed buffer plus two indexes: `front` (next to dequeue) and `size` (how many are filled). Enqueue writes at `(front + size) % capacity`. Dequeue reads `data[front]` and does `front = (front + 1) % capacity`. No shifting.

Capacity 4, enqueue 10, 20, 30, dequeue, enqueue 40, 50:

```
enqueue 10  [10, _, _, _]   front 0  size 1
enqueue 20  [10, 20, _, _]  front 0  size 2
enqueue 30  [10, 20, 30, _] front 0  size 3
dequeue 10  [_, 20, 30, _]  front 1  size 2
enqueue 40  [_, 20, 30, 40] front 1  size 3
enqueue 50  [50, 20, 30, 40] front 1  size 4   ← 50 wrapped to index 0
dequeue 20  [50, _, 30, 40] front 2  size 3
```

The `% capacity` wrap is the whole trick. Occupied slots are a ring, not a prefix.

```python
class CircularQueue:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.capacity = capacity
        self.front = 0
        self.size = 0

    def enqueue(self, value):
        if self.size == self.capacity:
            raise OverflowError("queue is full")
        tail = (self.front + self.size) % self.capacity
        self.data[tail] = value
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise IndexError("queue is empty")
        value = self.data[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return value
```

Both operations are O(1). Capacity is fixed unless you resize like a dynamic array (copy into a new buffer and reset `front` to 0).

**Trap:** storing `front` and `rear` without `size` makes “full” and “empty” look the same (`front == rear`). Either keep a `size`, or leave one slot unused as a sentinel.

### Linked-list queue

Singly list plus a **tail** pointer: enqueue at tail O(1), dequeue at head O(1).

```
head → A → B → C ← tail
enqueue D:  C.next = D, tail = D
dequeue:    head = head.next          (A dropped)
```

Empty-queue is the awkward case: after the last dequeue, set `tail = None` as well as `head = None`. After enqueue into an empty queue, `head` and `tail` both point at the new node.

### deque, in one sentence

Python’s `deque` gives you O(1) at both ends. Use it. The circular buffer and the linked-list queue are what you *explain* or *implement* when asked “build a queue.”

```python
from collections import deque
q = deque()
q.append("Alex")        # enqueue
q.append("Bob")
q.popleft()             # dequeue → 'Alex'
```

### Queue vs stack vs deque

| Word | What it is |
|---|---|
| Queue | FIFO *rule* |
| Enqueue / dequeue | The add / remove operations |
| Stack | LIFO *rule* |
| Deque | The *structure* (said “deck”) that can do either, both ends O(1) |

BFS needs a queue so nodes are processed in discovery order. A stack (or recursion) would go deep first instead.

**Interview rule:** say “queue” for the rule, implement it with `deque`. If they want you to build one, circular buffer or linked list with head and tail. Never `list.pop(0)`.

## 8. Recursion

Recursion is a function calling itself. Two pieces, always:

- **Base case** — a smallest input that returns without another call. Without this, the call stack grows until `RecursionError`.
- **Recursive case** — a smaller input, plus the work that combines the result.

The call stack from the stacks lesson *is* the memory. Each call has its own locals. The caller waits.

### Factorial, with the stack drawn

`n! = n * (n-1)!`, and `1! = 1` (or `0! = 1`).

```python
def fact(n):
    if n <= 1:                 # base
        return 1
    return n * fact(n - 1)     # recursive
```

Trace `fact(4)`. Each call waits for the one below it:

```
fact(4)  n=4, waits for fact(3)
  fact(3)  n=3, waits for fact(2)
    fact(2)  n=2, waits for fact(1)
      fact(1)  n=1, returns 1
    2 * 1 = 2
  3 * 2 = 6
4 * 6 = 24
```

Frames on the stack at the deepest point: four (`fact(4)` … `fact(1)`). Space is O(n). Time is O(n) — one call per value down to 1.

The loop version does the same multiply with O(1) extra space:

```python
def fact_iter(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

Same answer. Recursion is not faster here. It is the shape you need when the problem *tree* is not a straight line (trees, divide-and-conquer, backtracking).

**Trap:** `return fact(n - 1)` without multiplying by `n` computes 1 for every `n`. `return n * fact(n)` never shrinks the argument and recurses forever.

Python does not optimize tail recursion. `return fact(n - 1)` still uses O(n) stack frames. Do not write “tail-recursive so O(1) space” in a Python interview.

Default recursion limit is around 1000 (`sys.getrecursionlimit()`). `fact(2000)` raises `RecursionError` even though the math is fine. Deep linear recursion belongs in a loop.

### Fibonacci, and why the naive tree explodes

`0, 1, 1, 2, 3, 5, 8, 13, 21, …` — each term is the sum of the previous two. `F(0) = 0`, `F(1) = 1`, `F(n) = F(n-1) + F(n-2)`.

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

Factorial was a **chain**. Fibonacci is a **tree**. `fib(4)`:

```
              fib(4)
             /      \
        fib(3)      fib(2)
        /    \      /    \
    fib(2) fib(1) fib(1) fib(0)
    /    \
fib(1) fib(0)
```

`fib(2)` runs **twice**. `fib(3)` would run twice if you went to `fib(5)`. The same subproblem is not shared; each call starts from scratch.

`T(n) = T(n-1) + T(n-2) + O(1)` is Θ(φ^n), φ ≈ 1.618. Counting every function entry (including bases): `fib(4)` is 9 calls, `fib(8)` is **67** calls for the answer **21**, `fib(40)` is tens of millions. Time is not “O(n) because we go down to 0.”

### Memoization — remember the smaller answers

Memoization stores a finished result so the next call with the same argument returns it. Recursion still breaks the problem down; the dict is a notebook.

```python
def fib(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]                          # already known
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

`if n in memo` is the cache hit. Otherwise compute once, write `memo[n]`, return it. Pass the **same** dict into both recursive calls so they share the notebook.

Same `fib(8) = 21`, but **15** function entries instead of 67 (every `k` from 0 to 8, plus the cache-hit calls of the form `fib(k-2)` after `fib(k-1)` already filled it). Each distinct `n` is computed at most once, so time is O(n). Extra space is O(n) for the dict **and** O(n) call-stack depth.

| n | Result | Plain calls | Memo calls |
|---|---|---|---|
| 4 | 3 | 9 | 7 |
| 8 | 21 | 67 | 15 |
| 10 | 55 | 177 | 19 |

Plain recursion grows explosively. Memoization grows linearly with n.

**Trap:** `def fib(n, memo={})` shares one dict across **unrelated** top-level calls. Use `None` and create `{}` inside, same mutable-default rule as the functions lesson.

### Recursion and memoization are not alternatives

| | Recursion | Memoization |
|---|---|---|
| What it is | A function calling itself | Storing a computed result |
| Purpose | Smaller subproblems | Skip work you already did |
| Memory | Call stack | A cache, usually a dict |
| Speed | Slow if work repeats | Fast when subproblems overlap |

You can have recursion without a cache (factorial, tree DFS). Recursion **with** a cache (Fibonacci). A cache without recursion (the bottom-up table below). Do not say “use memoization instead of recursion.” Say whether the recursive tree **repeats** work.

### `@cache` — the interview shortcut

Python 3.9+ remembers arguments for you:

```python
from functools import cache

@cache
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

Same O(n) behavior as the hand-rolled dict. On 3.8 write `@lru_cache(maxsize=None)`. Tell the interviewer you are memoizing; the decorator is allowed unless they want the dict written out.

`@cache` keys on the arguments. The function must be deterministic, and arguments must be hashable (`n` is an int — fine; a list is not).

### When a cache helps — and when it does not

Add memoization when **the same subproblem shows up more than once**: Fibonacci, climbing stairs, “min coins for amount `a`,” path counts that re-enter the same `(i, j)`. You will see that pattern named **overlapping subproblems** in the DP lessons.

Skip it when every subproblem is unique: factorial (`fact(5)` never needs `fact(5)` again), a tree walk that already has `seen`, merge sort’s disjoint halves. A cache there wastes memory and does not change the Big-O.

### Bottom-up is the same math without the stack

Fill a table from the bases toward `n`. That is **tabulation** / bottom-up DP. Memoized recursion is **top-down** DP. Both reuse overlapping answers.

```python
def fib_table(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

O(n) time, O(n) space. Rolling two variables is O(1) extra space:

```python
def fib_iter(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

`fib_iter(5)`: `(0,1) → (1,1) → (1,2) → (2,3) → (3,5)`. Same recurrence, no tree.

### How to talk about a recursive function

- Base case: what is the smallest input, and what does it return?
- Recursive case: how is the input smaller, and how do you combine?
- Time: how many calls, how much work per call? Do subproblems repeat?
- Space: depth of the stack, plus any cache.

For `fact`, calls = n, depth = n. For naive `fib`, calls = Θ(φ^n) (`fib(8)` → 67), depth = n. For memo / `@cache` `fib`, each n once (`fib(8)` → 15 entries), depth = n.

**Interview rule:** recursion is a tool, not a default. Use it when the natural structure is a tree or a smaller subproblem of the same shape. If the tree repeats work, add a cache (dict or `@cache`) or write the bottom-up loop. If the recursion is a straight line (factorial), a loop is simpler and will not hit `RecursionError`. If they ask for Fibonacci, give memoized or iterative unless they explicitly want the exponential tree.

## 9. Insertion sort

You already have the `sort`/`sorted` API and a comparison table in the interview-tools track. These four sorting lessons are the implementations: trace them, then write them from memory.

Insertion sort keeps a **sorted prefix** and inserts the next value into it — like sorting a hand of cards.

Running example: `[5, 1, 4, 2]`.

```
i=1, key=1   prefix [5]
  5 > 1, shift right     [5, 5, 4, 2]
  put 1                  [1, 5, 4, 2]

i=2, key=4   prefix [1, 5]
  5 > 4, shift           [1, 5, 5, 2]
  1 < 4, stop
  put 4                  [1, 4, 5, 2]

i=3, key=2   prefix [1, 4, 5]
  5 > 2, shift           [1, 4, 5, 5]
  4 > 2, shift           [1, 4, 4, 5]
  1 < 2, stop
  put 2                  [1, 2, 4, 5]
```

The “hole” moves left while `arr[j] > key`. Then `key` drops into the first slot that is not larger.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key, j = arr[i], i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

Compare `arr[j] > key`, not `>=`. Using `>` leaves an equal earlier element where it was, so the sort is **stable**. `>=` would slide past equals and become unstable.

### Why the costs look like that

- Best case: already sorted. The `while` never runs. One comparison per `i` → O(n).
- Worst case: reverse sorted. Each new key slides all the way to index 0. Shifts `1 + 2 + … + (n-1)` → O(n²).
- Average: also O(n²). Extra space O(1). In-place.

That best-case O(n) is why Timsort (Python’s `sort`) insertion-sorts short already-sorted **runs**. Insertion is the right tool for n ≲ 10, or for an almost-sorted array (one element out of place).

**Trap:** the outer loop starts at `1`, not `0` — a prefix of length 1 is already sorted. Forgetting `j >= 0` reads `arr[-1]` in Python (wraps) and corrupts the array; in other languages it is an out-of-range crash.

**Interview rule:** if they ask you to implement a simple in-place sort, insertion is the honest answer for tiny or nearly sorted input. Do not claim O(n log n).

## 10. Merge sort

Split in half, sort each half, merge two **already-sorted** lists. The merge is the whole algorithm.

```
[5, 1, 4, 2]
[5, 1]           [4, 2]
[5] [1]          [4] [2]
[1, 5]           [2, 4]
[1, 2, 4, 5]
```

Merge `[1, 5]` with `[2, 4]`: always take the smaller head.

```
heads 1 vs 2 → take 1     out [1]
heads 5 vs 2 → take 2     out [1, 2]
heads 5 vs 4 → take 4     out [1, 2, 4]
right empty  → take 5     out [1, 2, 4, 5]
```

Use `<=` when the heads are equal so the left (earlier) value wins — that is stability.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]
```

### Why it is always O(n log n)

The recursion tree has about `log n` levels (halving). At each level, every element is copied into some `out` exactly once, so each level is O(n). `log n` levels × O(n) = O(n log n). There is no “already sorted” shortcut: you still split and merge. Best = average = worst.

Extra space is O(n) for `out`, plus O(log n) stack frames. The `arr[:mid]` slices in the version above add more copies; an interview “in-place merge sort” still needs an O(n) helper buffer. True in-place merge is possible but not what they want.

Linked lists merge without random access: split by walking, merge by rewiring `next`. That is why list-sorting is often merge sort.

**Trap:** `if left[i] < right[j]` (strict) is unstable: equal keys from the right can jump ahead. Off-by-one on `mid`: `arr[:mid]` and `arr[mid:]` must cover the whole array with no overlap. `len <= 1` is the base; `len == 0` happens on empty input.

**Interview rule:** “implement a sort that is always O(n log n) and stable” → merge sort. Mention the extra O(n) memory. In Python production code you still call `sort`.

## 11. Quick sort

Pick a **pivot**, partition into “less than (or equal) pivot” and “greater than pivot,” put the pivot in its final index, recurse on both sides.

The extra-list version is the idea:

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

```
[5, 1, 4, 2]  pivot 4
less [1, 2]   equal [4]   more [5]
sort [1, 2] → [1, 2]
result [1, 2, 4, 5]
```

Interviews then ask for **in-place partition**. Lomuto: pivot is the last slot. `i` is the next index that should hold a small value. Scan `j` from `lo` to `hi - 1`; when `arr[j] <= pivot`, swap into `i` and bump `i`. Finally swap the pivot into index `i`.

```python
def quicksort(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    p = partition(arr, lo, hi)
    quicksort(arr, lo, p - 1)
    quicksort(arr, p + 1, hi)

def partition(arr, lo, hi):
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i
```

Trace `[5, 1, 4, 2]`, `lo=0`, `hi=3`, pivot `2`, `i=0`:

```
j=0  5 <= 2? no
j=1  1 <= 2? yes  swap i=0 with j=1   [1, 5, 4, 2]  i=1
j=2  4 <= 2? no
swap pivot with i                     [1, 2, 4, 5]  return 1
```

Pivot `2` is now at index 1, its final home. Left `[1]` is done. Right `[4, 5]` partitions with pivot `5` → already ordered.

### The O(n²) case

If the pivot is always the smallest or largest, one side is empty and the other has `n-1` elements. Already-sorted input + last-element pivot does this:

```
[1, 2, 3, 4]  pivot 4  →  left [1, 2, 3], right empty
T(n) = T(n-1) + O(n) = O(n²)
```

Average (random pivot, or shuffled input) is O(n log n): the split is reasonably balanced. Extra space is O(log n) stack on average, O(n) in the degenerate case. Typical in-place versions are **not stable** (swaps move equals).

Fixes you should name: pick a random index and swap it into `hi` before partitioning; or median-of-three (`lo`, mid, `hi`).

Hoare partition (two fingers inward) does fewer swaps; Lomuto is the one to write from memory in an interview.

**Trap:** `quicksort(arr, lo, p)` instead of `p - 1` can recurse on the pivot forever. Forgetting to swap the pivot into `i` at the end leaves it at the right and the partition is wrong. `arr = arr.sort()` is still wrong — this function mutates; it returns `None` unless you write it that way.

**Interview rule:** “fast average sort” → quicksort, then immediately say worst case O(n²) and how you pick the pivot. “Always n log n, stable” → merge. “Just sort this in Python” → `arr.sort()`.

## 12. Bucket sort

Comparison sorts cannot beat O(n log n) in the worst case: each comparison gives one bit, and there are n! orders. If keys have **structure** (small integers, digits, uniform reals in a range), you can do better.

### Counting sort — integers in `0..k`

Count how many times each value appears, then write the values out in order.

```python
def counting_sort(arr, k):
    counts = [0] * (k + 1)
    for x in arr:
        counts[x] += 1
    out = []
    for value, freq in enumerate(counts):
        out.extend([value] * freq)
    return out
```

```
[5, 1, 4, 2, 1]   k=5
counts index:  0 1 2 3 4 5
counts:        0 2 1 0 1 1
write: 1, 1, 2, 4, 5
```

Time and extra space O(n + k). If k is 10⁹, this is worse than n log n. If k is 100 and n is 10⁵, it wins.

The `extend` version is fine for identical integers. For **objects** with integer keys (or for radix), fill **right to left** from a prefix-sum of counts so equal keys keep input order — that pass is stable, which radix needs.

### Bucket sort — scatter, sort, concatenate

For numbers spread over a range, put them into `n` buckets by value, insertion-sort each bucket (they should be small), then concatenate.

```python
def bucket_sort(arr):
    n = len(arr)
    if n == 0:
        return arr
    lo, hi = min(arr), max(arr)
    if lo == hi:
        return list(arr)
    buckets = [[] for _ in range(n)]
    for x in arr:
        index = int((x - lo) / (hi - lo + 1e-12) * (n - 1))
        buckets[index].append(x)
    out = []
    for b in buckets:
        insertion_sort(b)
        out.extend(b)
    return out
```

Average O(n) when values are roughly uniform — each bucket stays O(1) size, insertion is cheap. Worst case all in one bucket → O(n²) insertion. Extra space O(n).

### Radix sort — sort digit by digit

Counting-sort by the least significant digit first, then the next, and so on. Each pass must be **stable** so earlier digit order survives. For d digits and base b: O(d · (n + b)).

```
[170, 45, 75, 90]
ones: 170, 90, 45, 75
tens: 170, 45, 75, 90
hundreds: 45, 75, 90, 170
```

**Trap:** “I will counting-sort the array of timestamps” is wrong if the range is huge. State n **and** k. Bucket sort on already-clustered data (everything near one value) degrades to insertion sort.

**Interview rule:** use `sort` unless keys are small integers or the question is “beat n log n.” Then counting or radix. Name the range. Bucket is the generalization; counting is the integer special case.

## 13. Binary search

On a **sorted** array, throw away half the remaining range each step. That is O(log n) comparisons versus O(n) to scan.

The invariant: if the target is in the array, it is inside `arr[lo..hi]` **inclusive**. Each step must shrink that window, or you loop forever.

Find `4` in `[1, 2, 4, 5, 7]`:

```
lo=0 hi=4  mid=2  arr[2]=4  found
```

Find `3` (absent):

```
lo=0 hi=4  mid=2  arr[2]=4 > 3   hi = mid-1 = 1
lo=0 hi=1  mid=0  arr[0]=1 < 3   lo = mid+1 = 1
lo=1 hi=1  mid=1  arr[1]=2 < 3   lo = mid+1 = 2
lo=2 hi=1  lo > hi  not found
```

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Empty array: `hi = -1`, the loop never runs, return `-1`. Single element: `lo == hi == 0`, one check.

### Why `mid + 1` and `mid - 1`

If `arr[mid] < target`, `mid` itself cannot be the answer, so the new range starts at `mid + 1`. Same idea on the other side. If you write `lo = mid` when `arr[mid] < target`, and `lo` is already `mid`, `lo` never moves.

**Trap:** `while lo < hi` with this inclusive version skips the last element. Pair `lo <= hi` with `hi = len - 1` and `mid ± 1`. The next lesson uses a different pairing (`lo < hi`, `hi = len`, `hi = mid`). Mixing the two is the usual off-by-one.

`(lo + hi) // 2` is fine in Python (ints do not overflow). In Java/C, `lo + hi` can overflow; they write `lo + (hi - lo) / 2`. Mention it if the interviewer is in that world.

The array **must be sorted** in the order you compare. Unsorted → wrong answer, not an error. Duplicates: this function returns *an* index, not the first or last. That is the next lesson.

**Interview rule:** say the invariant out loud, then write the loop. Trace an empty array, a missing value, and a hit at index 0 and at the last index.

## 14. Search range

Binary search’s useful form is often not “is x here?” but “where would x go?” That is a **boundary**: the first index that fails (or starts to satisfy) a predicate.

`bisect_left`: first index `i` with `arr[i] >= x` (lower bound; insertion point to keep sorted order, left of equals).

`bisect_right`: first index `i` with `arr[i] > x` (upper bound; insertion point after equals).

The window is now **half-open**: `lo` inclusive, `hi` exclusive, `hi` starts at `len(arr)`. Loop while `lo < hi`. When the mid is still a candidate, set `hi = mid` (do not skip it). When it cannot be, set `lo = mid + 1`.

```python
def bisect_left(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid          # mid might still be the first >= x
    return lo

def bisect_right(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

Trace `[1, 2, 2, 2, 4]`, `x = 2`:

```
bisect_left  — first >= 2
  lo=0 hi=5 mid=2  arr[2]=2 is not < 2   hi=2
  lo=0 hi=2 mid=1  arr[1]=2 is not < 2   hi=1
  lo=0 hi=1 mid=0  arr[0]=1 < 2          lo=1
  lo=1 hi=1  stop  → 1

bisect_right — first > 2
  lo=0 hi=5 mid=2  arr[2]=2 <= 2         lo=3
  lo=3 hi=5 mid=4  arr[4]=4 > 2          hi=4
  lo=3 hi=4 mid=3  arr[3]=2 <= 2         lo=4
  lo=4 hi=4  stop  → 4
```

So the run of `2` is `arr[1:4]`. Count = `right - left` = 3. First occurrence = 1. Last = `right - 1` = 3, but only if `left < right` (otherwise x is absent).

Insert `3` into that array: `bisect_left` → 4, in front of `4`. Insert another `2`: `bisect_left` → 1 (before existing equals) or `bisect_right` → 4 (after them).

```python
from bisect import bisect_left, bisect_right
arr = [1, 2, 2, 2, 4]
bisect_left(arr, 2)     # 1
bisect_right(arr, 2)    # 4
bisect_left(arr, 3)     # 4  — insertion point
```

`bisect.insort` uses this index, then inserts in O(n). You already have that cost from the interview-tools track.

### Binary search on an answer

The same loop searches a **numeric range**, not an array, when `feasible(m)` is monotonic (False, False, …, True, True). Find the first True:

```python
def first_true(lo, hi, feasible):    # hi exclusive, like bisect_left
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Same pairing as `bisect_left`. This is “search the range” in the interview sense: smallest capacity, first day, first index that works.

**Trap:** using the inclusive `lo <= hi` / `mid ± 1` template here, or the half-open template for exact-value search, is how off-by-ones happen. Pick one pair and stick to it. `bisect_left` on an absent value still returns a valid insertion index, not `-1` — check `lo < len(arr) and arr[lo] == x` if you needed “found.”

**Interview rule:** first / last occurrence, count of a value, or insertion point → `bisect_left` / `bisect_right`. Write the half-open loop. “Smallest x that works” on a monotonic predicate → the same loop on the answer range.

## 15. Binary trees

A **binary tree** is nodes with at most two children, usually named `left` and `right`. There is **no ordering rule** yet. That comes with BSTs.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

```
      A
     / \
    B   C
   / \
  D   E
```

- **Root** — the node you hold; here `A`. The whole tree is that pointer.
- **Leaf** — both children `None`; here `C`, `D`, `E`.
- **Parent / child / sibling** — `B` is parent of `D` and `E`; `D` and `E` are siblings.
- **Depth** of a node — steps from the root. `A` is 0, `B`/`C` are 1, `D`/`E` are 2.
- **Height** of a node — longest path down to a leaf. Height of a leaf is 0; height of this tree (the root) is 2. Some writers set a leaf’s height to 1 — pick one and stay with it. Interviews usually want “longest root-to-leaf edge count,” so a single node has height 0.

An **empty tree** is `None`. Always null-check before reading `.left` / `.val`.

### Shapes you should be able to name

- **Full:** every node has 0 or 2 children (no only-child).
- **Complete:** filled level by level, left to right. Heaps are complete binary trees.
- **Perfect:** every level is full. n = 2^(h+1) − 1 nodes.
- **Skewed:** every node has only one child. It is a tree that behaves like a linked list: height n − 1.

A complete tree can be stored in an **array** (heap style): index `i` has left child `2i+1` and right child `2i+2`, parent `(i-1)//2`. Interview trees are usually `TreeNode` objects. Use the array form when the tree is complete and you already have a buffer (heaps, next section).

### Why trees

A balanced binary tree of n nodes has height Θ(log n). Walking from the root to a leaf is O(log n) instead of O(n) on a list. A skewed tree is O(n). **Every tree cost is in terms of height h, and h is log n only if the tree is balanced.**

```python
def height(node):
    if node is None:
        return -1                 # so a leaf (both None) has height 0
    return 1 + max(height(node.left), height(node.right))
```

Time is O(n): you visit every node. Space is O(h) stack.

**Trap:** `if not node.left and not node.right` as “is a leaf” is right; `if not node.left or not node.right` is “has a missing child,” which includes nodes with one child. Recursing without `if node is None` crashes on a missing child.

**Interview rule:** draw the tree. Label root and `None` children. Then write code. A binary tree is a shape; a BST is a shape **plus** an invariant.

## 16. Binary search trees

A **BST** adds one rule, and it applies to **whole subtrees**, not just the immediate children:

Every node in the left subtree is **< node**. Every node in the right subtree is **> node**.

(Some codebases use `<=` on one side. Pick a convention and keep it. These notes use strict `<` / `>` and no duplicates unless stated.)

```
        4
       / \
      2   6
     / \ / \
    1  3 5  7
```

Check 4: left subtree `{1,2,3}` all `< 4`, right `{5,6,7}` all `> 4`. Check 2: `{1} < 2 < {3}`. The local picture “left child < node < right child” is necessary but **not enough**. This is not a BST:

```
      4
     / \
    2   6
   /
  5          5 is left of 4 but 5 > 4
```

### Search is a walk

Compare and go left or right. Stop at a match or at `None`.

```python
def search(node, target):
    while node:
        if target == node.val:
            return node
        node = node.left if target < node.val else node.right
    return None
```

On the tree above, search `5`: `4 → 6 → 5`. Search `0`: `4 → 2 → 1 → None`. Time O(h). Balanced: O(log n). Inserting `8, 9, 10, 11, …` into an empty tree with no rebalancing builds a stick: O(n).

Min is the leftmost node (`while node.left`). Max is the rightmost.

### Inorder is sorted

Left, node, right on a BST visits keys in increasing order: `1 2 3 4 5 6 7`. That is the proof the invariant holds, and it is how you dump a BST into a sorted array.

**Trap:** checking only `node.left.val < node.val < node.right.val` misses a descendant that violates the ancestor. Validate with a range: a node must lie in `(lo, hi)` inherited from above.

```python
def is_bst(node, lo=None, hi=None):
    if node is None:
        return True
    if lo is not None and node.val <= lo:
        return False
    if hi is not None and node.val >= hi:
        return False
    return is_bst(node.left, lo, node.val) and is_bst(node.right, node.val, hi)
```

**Interview rule:** BST operations are O(h), not magically O(log n). Say “log n if balanced, n if skewed.” Python has no balanced BST in the stdlib; `dict`/`set` are hash tables (unordered). Ordered queries need `bisect` on a sorted list, or a library like `sortedcontainers`.

## 17. BST insert and remove

### Insert

Walk as in search. When you hit `None`, attach a new node there. The first inserted value is the root.

```python
def insert(node, val):
    if node is None:
        return TreeNode(val)
    if val < node.val:
        node.left = insert(node.left, val)
    elif val > node.val:
        node.right = insert(node.right, val)
    return node                  # ignore duplicates
```

Start empty, insert `4, 2, 6, 1, 3`:

```
4
4
 \
  wait, 2 < 4:
      4
     /
    2
then 6 > 4:
      4
     / \
    2   6
then 1, 3 under 2:
      4
     / \
    2   6
   / \
  1   3
```

Iterative insert keeps a `parent` pointer so you can hang the new node off `parent.left` or `parent.right`. Time O(h).

### Delete

Three cases. Find the node first (O(h)), then:

**0 children (leaf).** Parent’s pointer becomes `None`. Delete `1` above: `2.left = None`.

**1 child.** Replace the node with that child. Delete `6` if it only had a right child `7`: the parent’s pointer that used to hold `6` now holds `7`.

**2 children.** You cannot drop the node and keep both subtrees with one pointer. Copy the **inorder successor** (minimum of the right subtree — leftmost in the right) into this node, then delete that successor from the right subtree. The successor has no left child, so its delete is case 0 or 1.

```python
def delete(node, val):
    if node is None:
        return None
    if val < node.val:
        node.left = delete(node.left, val)
    elif val > node.val:
        node.right = delete(node.right, val)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        succ = node.right
        while succ.left:
            succ = succ.left
        node.val = succ.val
        node.right = delete(node.right, succ.val)
    return node
```

Delete `2` from the tree (2 has two children). Successor of 2 is min of `{3}` = `3`. Copy `3` into 2’s slot, then delete the old `3` (a leaf):

```
before             after
    4                  4
   / \                / \
  2   6              3   6
 / \                /
1   3              1
```

Inorder predecessor (max of the left subtree) works too. Interviews usually want successor.

**Trap:** deleting the successor with `node.right = delete(node.right, succ.val)` — if you `delete(node, succ.val)` from the root instead, you can hit the node you just wrote and recurse forever. After a 2-child delete, the structure changed; do not keep using the old child pointers you stashed unless you updated them.

**Interview rule:** say the three cases out loud. For two children: “replace with inorder successor (min of right), then delete that successor.” Draw it.

## 18. Tree DFS

Depth-first search goes as deep as possible along one branch, then backtracks. On a binary tree that is “do this child, then the other.” The **call stack** from the recursion lesson *is* the DFS stack.

Three visit orders — the names say when you process **this node**:

| Order | When you record `node.val` | This tree `4 / 2 6 / 1 3 5 7` |
|---|---|---|
| Preorder | before both children | 4, 2, 1, 3, 6, 5, 7 |
| Inorder | between left and right | 1, 2, 3, 4, 5, 6, 7 |
| Postorder | after both children | 1, 3, 2, 5, 7, 6, 4 |

```python
def inorder(node, out=None):
    if out is None:
        out = []
    if node is None:
        return out
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)
    return out
```

Preorder: append, then left, then right. Postorder: left, right, then append. Same skeleton, move the `append`.

Recursive inorder on the BST:

```
inorder(4)
  inorder(2)
    inorder(1) → 1
    visit 2
    inorder(3) → 3
  visit 4
  inorder(6)
    inorder(5) → 5
    visit 6
    inorder(7) → 7
```

That is why BST inorder is sorted.

### Explicit stack (preorder)

```python
def preorder_iter(root):
    if not root:
        return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:                 # push right first so left pops first
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out
```

LIFO: last pushed is next visited, so push right before left to go left first.

Postorder with a stack is fiddlier (two stacks, or a “seen” flag). Recursive postorder is what you write unless they ban recursion.

Time O(n): every node once. Extra space O(h) for the stack (O(n) if skewed).

**Trap:** pushing left then right on a stack visits **right first**. Forgetting the `None` base case. Using DFS when you needed level order (next lesson) or shortest path in an unweighted graph (BFS).

**Interview rule:** “visit every node, care about parent-before-children / sorted / children-before-parent” → pre / in / post. Recursion first. Path-from-root problems are DFS plus a list you append and pop (backtracking, two lessons down).

## 19. Tree BFS

Breadth-first search visits **level by level**: root, then depth 1, then depth 2. That is FIFO, so a **queue**. Same reason BFS on graphs uses `deque`.

```
        4
       / \
      2   6
     / \ / \
    1  3 5  7

level 0: 4
level 1: 2, 6
level 2: 1, 3, 5, 7
```

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    q, out = deque([root]), []
    while q:
        node = q.popleft()
        out.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return out
    # [4, 2, 6, 1, 3, 5, 7]
```

### One list per level

The queue length at the start of a round is the size of the current level. Drain that many nodes, enqueue their children for the next round.

```python
def levels(root):
    if not root:
        return []
    q, out = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out
    # [[4], [2, 6], [1, 3, 5, 7]]
```

`for _ in range(len(q))` is fixed at the start of the loop; children appended during the round are not visited until the next round.

Time O(n). Extra space O(w) where w is the widest level (up to O(n) for a perfect tree’s last level).

Shortest path from root to a node, counting edges, **is** the BFS level of that node. DFS depth is a path length, not necessarily the shortest in a general graph; in a tree there is only one path, so DFS depth equals BFS level. The distinction matters once there are extra edges (graphs).

**Trap:** `list.pop(0)` as the queue. `stack.pop()` as BFS — that is DFS again. Enqueueing `None` children unless you actually want to record missing slots.

**Interview rule:** “level order, zigzag, right side view, minimum depth” → BFS with a queue. “Serialize / next pointer in a perfect tree” often BFS too. Recursion can fake level order with a `depth` argument; the queue is the straightforward version.

## 20. BST sets and maps

A balanced BST is an **ordered set**: membership plus min/max, successor/predecessor, and range queries. A **map** is the same tree with a `val` payload on each key.

| Need | Hash set / dict | BST set / map |
|---|---|---|
| Lookup / insert / delete | O(1) average | O(h) |
| Order | None | Inorder is sorted |
| Min / max | O(n) scan | O(h) leftmost / rightmost |
| Next key `>= x` | Not without extra structure | O(h) walk |
| Range `[a, b]` | O(n) | O(h + k) to walk k hits |

Python `set` / `dict` are hash tables. They do not give you successor. The interview-tools track used `bisect` on a sorted **list** as the stdlib stand-in; insert there is O(n). A real TreeMap (Java) or `sortedcontainers.SortedDict` is a balanced BST (or equivalent) with O(log n) insert.

### Successor and “first key `>= x`”

From a node, successor is: if there is a right child, min of the right subtree; else the nearest ancestor you came from on a **left** branch.

To find the first key `>= x` without a parent pointer, walk from the root and remember the last node that was `>= x`:

```python
def lower_bound(node, x):
    cand = None
    while node:
        if node.val >= x:
            cand = node
            node = node.left          # maybe a closer one
        else:
            node = node.right
    return cand
```

On the `1..7` tree, `lower_bound(3)` is `3`. `lower_bound(3.5)` is `4`. This is the tree form of `bisect_left`.

Range `[3, 6]`: find `lower_bound(3)`, then walk inorder until you pass 6. Or recurse: skip a subtree that is entirely outside `[3, 6]`.

A map node is `TreeNode(key, value, left, right)` — compare on `key`, return `value`. Same insert/delete as before.

**Trap:** using a `dict` when the question needs the next larger key. Using a BST when you only needed membership — a hash set is simpler and expected. Building a BST from sorted keys in insertion order makes a stick; build from the middle (like binary search) if you must stay balanced by hand, or say “assume a balanced tree / red-black.”

**Interview rule:** unordered + fast → hash. Ordered + next/prev/range → BST (or sorted list + `bisect` in Python, and mention the O(n) inserts).

## 21. Backtracking

Backtracking is DFS that **undoes** after each attempt so the next attempt sees a clean state. Choose, explore, unchoose.

The course’s picture is a **tree maze**: each node is a room, edges are doors, you try a door, and if that corridor fails you return and try the next door. The call stack holds the current path. Popping the frame (and unmarking) is the step back.

The same template walks a grid (the 2-D lists lesson) as a tree of moves:

```python
def exists_path(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if r == rows - 1 and c == cols - 1:
            return True                          # reached the exit
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 0
                    and (nr, nc) not in visited):
                visited.add((nr, nc))            # choose
                if dfs(nr, nc):                  # explore
                    return True
                visited.remove((nr, nc))         # unchoose
        return False

    visited.add((0, 0))
    return dfs(0, 0)
```

`0` is open, `1` is a wall. Bounds check **before** indexing. Visited key is a tuple `(r, c)` — lists are unhashable.

Trace a 2×2 open grid, start `(0,0)`, exit `(1,1)`:

```
choose down (1,0)
  choose right (1,1) → True, unwind
```

If that exit were a wall, you would unmark `(1,0)` and try right from the start instead. **Without unmark**, the failed corridor would stay blocked for every later path.

### Why unmark

Visited-for-the-whole-search (plain graph DFS) never unmarks: you only need to know if a node was ever seen. Backtracking unmarks because the mark means “on **this** path,” and a cell might be legal on a different path. Maze-with-one-visit-per-path unmarks. Word search in a grid unmarks. Subsets do not need a grid, but they still pop the last choice:

```python
def subsets(nums):
    out, path = [], []

    def bt(i):
        if i == len(nums):
            out.append(path[:])                  # copy the path
            return
        path.append(nums[i])                     # choose to include
        bt(i + 1)
        path.pop()                               # unchoose
        bt(i + 1)                                # choose to skip
    bt(0)
    return out
```

`subsets([1, 2])` → `[[1,2], [1], [2], []]` (order depends on include-first vs skip-first). The tree of calls *is* the decision tree. Time O(2^n) subsets, each copied in O(n).

Permutations: swap / used-array, recurse, swap back. N-queens: place, recurse next row, remove. Same three lines: choose, explore, unchoose.

**Trap:** `out.append(path)` without `path[:]` stores a reference; later pops empty every stored answer. Forgetting to unmark in a maze makes the first failed path poison the rest. Marking before the bounds/wall check, or checking after indexing. Recursing on the same `(r, c)` because visited was not set before the call (infinite loop).

**Interview rule:** if you build a path or a partial assignment and then try a different one, you need undo. Say “choose, recurse, unchoose.” Draw one failing branch and the pop. For a maze, also say bounds, wall, visited tuple.

## 22. Heap properties

You already use `heapq` as a min-heap API. These three lessons are the structure: a **complete binary tree** stored in an array, with a parent–child rule. It is **not** sorted and **not** a BST.

```
Tree:            2
               /   \
              4     6
             /
            5

Array:  index  0  1  2  3
        value  2  4  6  5
```

Complete means filled level by level, left to right — **no holes**. That is why an array works: index `i` has

```
parent(i) = (i - 1) // 2     (root has no parent)
left(i)   = 2 * i + 1
right(i)  = 2 * i + 2
```

Check: parent of index 3 is `(3-1)//2 = 1` (value 4). Left of 0 is 1 (value 4); right of 0 is 2 (value 6). Last parent is `n // 2 - 1`.

Because the tree is complete, height is always `⌊log₂ n⌋`. A BST can skew to height n; a heap cannot. That is the whole point of the shape.

### The heap rule (partial order)

**Min-heap:** every parent `<=` both children. Root is the minimum. **Max-heap:** parent `>=` children; root is the maximum.

`2 <= 4`, `2 <= 6`, `4 <= 5`. That is enough. There is **no** rule between siblings, or between a node and its nephew. `[2, 4, 6, 5]` is a valid min-heap; `[2, 4, 5, 6]` would also be; `[2, 5, 6, 4]` is not (`5 > 4` at parent 1).

Inorder is not sorted. Heap `[1, 3, 2, 7, 4, 5]` is not `[1, 2, 3, 4, 5, 7]`. Only the root is the extreme. To get the next extreme you must pop (next lesson).

```python
def is_min_heap(a):
    n = len(a)
    for i in range(n // 2):                 # every parent
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and a[i] > a[l]:
            return False
        if r < n and a[i] > a[r]:
            return False
    return True
```

### Heap vs BST vs sorted array

| Need | Structure |
|---|---|
| Min (or max) fast, insert/delete min | Heap — O(1) peek, O(log n) push/pop |
| Arbitrary search, ordered walk | BST |
| Random access, binary search | Sorted array |
| Fast unordered membership | Hash set |

A heap does not support “is 7 in here?” in less than O(n). Do not scan-and-hope in an interview; pick a set.

Python `heapq` is a min-heap on a **list**. `heap[0]` is the min. There is no `heap[i]` “k-th smallest” except i = 0.

**Trap:** “heaps are sorted.” They are not. “Heap height can be n, like a BST.” No — complete shape forbids it. Drawing a heap as a tree with a missing left child and a present right child — that is not complete, and the index formulas break.

**Interview rule:** say “complete tree in an array, parent `<=` children, only the root is known extreme.” Peek O(1), everything else waits for sift.

## 23. Heap push and pop

Both operations restore the heap rule after a change at one end of the array.

### Push — append, then sift-up

New value goes at the **end** (next free slot, so the tree stays complete). Then swap with the parent while the parent is larger (min-heap).

```python
def sift_up(a, i):
    while i > 0:
        p = (i - 1) // 2
        if a[p] <= a[i]:
            break
        a[p], a[i] = a[i], a[p]
        i = p

def heappush(a, val):
    a.append(val)
    sift_up(a, len(a) - 1)
```

Start from `[2, 4, 6, 5]`, push `1`:

```
append           [2, 4, 6, 5, 1]     i=4, parent=1 (4)
1 < 4, swap      [2, 1, 6, 5, 4]     i=1, parent=0 (2)
1 < 2, swap      [1, 2, 6, 5, 4]     i=0, stop
```

At most one swap per level → O(log n). The new root is 1, the old 2 slid down one edge — nothing else was sorted.

### Pop — swap with last, then sift-down

The min is `a[0]`. Overwrite it with the **last** value, `pop()` the end, then sift **down**: swap with the smaller child while the rule is broken.

```python
def sift_down(a, i, n=None):
    if n is None:
        n = len(a)
    while True:
        l, r = 2 * i + 1, 2 * i + 2
        smallest = i
        if l < n and a[l] < a[smallest]:
            smallest = l
        if r < n and a[r] < a[smallest]:
            smallest = r
        if smallest == i:
            break
        a[i], a[smallest] = a[smallest], a[i]
        i = smallest

def heappop(a):
    if not a:
        raise IndexError("empty heap")
    a[0], a[-1] = a[-1], a[0]
    val = a.pop()
    if a:
        sift_down(a, 0)
    return val
```

Pop from `[1, 2, 6, 5, 4]`:

```
swap 0 with last  [4, 2, 6, 5, 1]
pop last          [4, 2, 6, 5]        4 is at root
children of 0: 2 and 6; smaller is 2
swap              [2, 4, 6, 5]        4 vs child 5; 4 <= 5, stop
```

Returns 1. Again O(log n). Compare both children before swapping — picking an arbitrary child can break the other.

Memory: **insert → up** (the hole is at the end). **Remove root → down** (the hole is at the root).

Max-heap: the same code with the comparisons flipped, or negate values and use a min-heap (`heappush(h, -x)`, `-heappop(h)`). That is the interview-tools version; either explanation is fine.

**Trap:** `heappop` without moving the last item to the root leaves a hole at index 0 and the array is no longer complete. Sifting up on pop (or down on push) goes the wrong direction and does not restore the rule. Mutating `heap[i]` by hand without sifting breaks `heapq` too.

**Interview rule:** write `append` + sift-up, and “swap with last, pop, sift-down.” Name the index formulas. Peek is `heap[0]`, not a pop.

## 24. Heapify

`heapify` turns an **arbitrary** array into a heap in place, in **O(n)** — cheaper than n pushes (which would be O(n log n)).

You only need to sift **down** from the last parent to the root. Leaves already satisfy the rule (no children). Each sift-down assumes the two subtrees of `i` are already heaps, then pushes `a[i]` down into the right place — the same Floyd idea as “two heaps plus a new root.”

```python
def heapify(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):    # last parent → 0
        sift_down(a, i, n)
```

`[5, 3, 8, 1, 2]`, n = 5, last parent = `5//2 - 1 = 1`.

```
start            [5, 3, 8, 1, 2]
                  5
                 / \
                3   8
               / \
              1   2

i=1 (value 3), children 1 and 2 (values 1, 2)
  smaller child is 1; 3 > 1, swap     [5, 1, 8, 3, 2]
i=0 (value 5), children 1 and 8
  smaller is 1; 5 > 1, swap           [1, 5, 8, 3, 2]
  5 now at index 1, children 3 and 2
  smaller is 2; 5 > 2, swap           [1, 2, 8, 3, 5]
```

Root is 1. The list is not sorted (`[1, 2, 8, 3, 5]`).

### Why O(n), not O(n log n)

A sift-down from height h costs O(h). In a complete tree most nodes sit on the **bottom** levels, where h is 0 or 1:

```
~ n/2 leaves,          height 0,  cost 0
~ n/4 nodes,           height 1,  cost n/4
~ n/8 nodes,           height 2,  cost 2n/8
…
1 root,                height log n
```

Total `n · (1/4 + 2/8 + 3/16 + …) < n · Σ k/2^(k+1) = O(n)`.

n `heappush` calls from empty would sift each item up from a leaf, and the later ones travel Θ(log n) — that sum *is* Θ(n log n). Bottom-up down is the better build.

`heapq.heapify(nums)` is this algorithm. After it, `nums[0]` is the min; do not assume anything else is ordered.

Heapsort: `heapify`, then repeatedly swap root with the end and sift-down on the shrinking prefix. Always O(n log n), in-place, not stable. Interviews still prefer `sort` unless they ask for heapsort.

**Trap:** heapify from the **front** (sift-up each index) is the O(n log n) build. Starting at 0 instead of the last parent visits leaves first, when their children are not yet heaps, so the “subtrees are heaps” assumption is false.

**Interview rule:** “build a heap” → `heapify` in O(n), last parent down to 0. “n inserts” is the slower build. k largest stays the size-k heap from the interview-tools track.

## 25. Hash usage

A **hash table** maps a key to a bucket in O(1) average time: `index = hash(key) % capacity`. Python `dict` and `set` are hash tables. You already use them for frequency (`Counter`), grouping (`defaultdict(list)`), and visited cells (`(r, c)` tuples). This lesson is *when* the O(1) is real, and the patterns interviews actually want.

Average lookup / insert / delete: O(1). Worst case: O(n) — every key in one bucket (bad hash, or an adversary). Interviews quote O(1) average unless they ask about collisions.

Keys must be **hashable**: immutable, and `__hash__` consistent with `__eq__`. `int`, `str`, `tuple` of hashables: yes. `list`, `dict`, `set`: no. That is why a visited grid cell is `(r, c)`, not `[r, c]`.

### Patterns

**Membership / visited** — `seen = set()`. `if x in seen` is O(1) average; a list scan is O(n).

**First index of each value** — two-sum: store `value → index` as you walk. The complement is one lookup, not a nested loop.

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
```

`[2, 7, 11, 15]`, target 9: i=0 store `2→0`; i=1, `need=2`, already there → `[0, 1]`. Time O(n), extra space O(n). The O(n²) double loop is the thing this replaces.

**Frequency / anagram** — `Counter(s) == Counter(t)`, or a dict of counts. **Grouping** — `defaultdict(list)`: `groups[key].append(item)`.

**Dedup** — `set(nums)` loses order; `list(dict.fromkeys(nums))` keeps first-seen (dicts remember insertion order).

### Hash vs heap vs BST (again)

| Need | Use |
|---|---|
| “Have I seen this exact key?” | `set` / `dict` |
| Smallest / largest repeatedly | Heap |
| Next key `>= x`, range | BST or `bisect` |
| Two-sum, anagram, visited | Hash |

**Trap:** `if x in list` inside a loop is O(n²). Using a list as a dict key. Assuming `set` is ordered. Quoting O(1) for `in` on a list. `defaultdict` inserts on `[]`; `Counter` returns 0 and does not insert — that trap from the Python-tools track still applies.

**Interview rule:** exact-key fast path → hash. Say “average O(1), worst O(n) if everything collides.” Then write the dict. Do not implement a hash table unless they ask (next lesson).

## 26. Hash implementation

Under the API: an array of **buckets**. A hash function turns a key into an integer; `index = hash(key) % m` picks the bucket. Two keys can land in the same bucket — a **collision**. That is normal. The table’s job is to store both.

### Chaining

Each bucket is a list (or linked list) of `(key, value)` pairs. Lookup: hash, then scan that one chain for an equal key.

```python
class HashMap:
    def __init__(self, cap=8):
        self.buckets = [[] for _ in range(cap)]
        self.size = 0

    def _idx(self, key):
        return hash(key) % len(self.buckets)

    def put(self, key, val):
        b = self.buckets[self._idx(key)]
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, val)
                return
        b.append((key, val))
        self.size += 1
        if self.size * 4 > len(self.buckets) * 3:    # load > 0.75
            self._rehash()

    def get(self, key, default=None):
        for k, v in self.buckets[self._idx(key)]:
            if k == key:
                return v
        return default
```

Trace capacity 4, `put("a", 1)`, `put("b", 2)`. Suppose `hash("a") % 4 == 1` and `hash("b") % 4 == 1` — both in bucket 1: `[[], [("a",1), ("b",2)], [], []]`. Get `"b"` scans two pairs, not the whole table.

**Load factor** `α = n / m` (items / buckets). Expected chain length is α, so expected lookup is O(1 + α). Keep α bounded (Python-ish threshold ~2/3 to 3/4) by **rehashing**: allocate `2m` buckets, re-insert every pair. That copy is O(n), amortized like a dynamic array.

```python
    def _rehash(self):
        old = self.buckets
        self.buckets = [[] for _ in range(len(old) * 2)]
        self.size = 0
        for b in old:
            for k, v in b:
                self.put(k, v)
```

A terrible hash (`return 0` for every key) puts everything in one chain: lookup O(n). A good hash spreads keys. Interviews treat `hash(key)` as uniform unless they ask you to break it.

### Open addressing (what CPython dicts actually use)

No lists. One array of slots. On collision, probe the next slot (linear: `i+1, i+2, …`; or more mixed probes). Lookup follows the same probe sequence until the key or an empty slot. Deletion needs a **tombstone**, or later probes stop too early.

You do not implement this in a 45-minute interview unless asked. Know the name, and that Python `dict` is open-addressed, insertion-ordered (3.7+), and resizes by growing the table.

### Hashable, again, at this layer

`hash(key)` must not change while the key sits in the table. A list’s contents can change, so its hash would move buckets — that is why lists are unhashable. A tuple of ints is frozen, so it is safe.

**Trap:** `hash(key) % m` with a hash that can be negative is still fine in Python (`(-3) % 8 == 5`). In Java/C, negative mods are a bug — they use `& (m-1)` with m a power of two. Rehashing without resetting `size` double-counts. Comparing keys with `is` instead of `==`.

**Interview rule:** explain `hash % m`, collisions, chaining vs open addressing, load factor, amortized resize. Then say Python `dict`/`set` already do this; you write `seen = {}` unless the question is “implement a hashmap.”

## 27. Intro to graphs

A **graph** is nodes (vertices) plus edges. A tree is the special case: connected, undirected, no cycles. Graphs drop those restrictions — they can have extra edges, missing connections, directions, and weights.

```
A — B
|   |
C — D     undirected, one connected piece, has a cycle A-B-D-C-A
```

| Word | Meaning |
|---|---|
| Vertex / node | A thing |
| Edge | A connection; `{A,B}` undirected or `A → B` directed |
| Neighbor | A node sharing an edge |
| Degree | Number of neighbors (in-degree / out-degree if directed) |
| Path | A walk that does not repeat vertices |
| Cycle | A path back to its start |
| Connected | Every pair has some undirected path |
| Weighted | Edges carry a cost |

Directed: Twitter follows, course prerequisites. Undirected: two-way streets, an undirected grid. Weighted: flight prices. Unweighted: “one step” is the same cost — BFS shortest path applies.

### Two representations

**Adjacency matrix** — `n × n` of 0/1 (or weights). `matrix[u][v]` is O(1). Space Θ(n²) even when there are few edges. Fine for dense graphs (e ~ n²).

**Adjacency list** — for each node, a list of neighbors. Space Θ(n + e). Iterate neighbors in O(degree). Edge check is O(degree) unless you store sets. This is the default interview structure.

```python
# edges = [(0,1), (0,2), (1,2)]  undirected, nodes 0..2
n = 3
adj = [[] for _ in range(n)]
for u, v in [(0, 1), (0, 2), (1, 2)]:
    adj[u].append(v)
    adj[v].append(u)            # drop this line if directed
# adj[0] == [1, 2]
```

If node labels are strings, use `defaultdict(list)` instead of `range(n)`.

A **grid** is a graph you do not store explicitly: each cell is a node, and an edge exists to a 4-direction neighbor that is in bounds (and not a wall). Next two lessons.

### Costs to say out loud

Scanning every vertex and every edge is O(n + e) on a list, O(n²) on a matrix. DFS/BFS are O(n + e) list, O(n²) matrix. “n nodes, e edges” — always name both.

**Trap:** building an undirected graph and adding the edge only one way. Using a matrix for a sparse graph of 10⁵ nodes (memory dies). Forgetting that a tree’s e = n − 1, so O(n + e) = O(n). Treating a cycle as a second parent in undirected DFS without the “neighbor == parent” skip.

**Interview rule:** say directed or not, weighted or not, then pick list vs matrix. Default list. Grid problems are graphs with implicit edges.

## 28. Matrix DFS

A grid is a graph. `grid[r][c]`. Four neighbors: up, down, left, right. Bounds-check **before** indexing. Visited key is `(r, c)`.

Number of islands: a `1` is land. An island is a connected blob of land. Each DFS from an unvisited `1` paints that whole blob.

```
1 1 0
1 0 0
0 0 1
```

Two islands: the L in the top-left, and the single `1` at bottom-right.

```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "0"                    # mark visited in place
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                count += 1
    return count
```

Trace: `(0,0)` starts island 1, paints `(0,0)`, `(1,0)`, `(0,1)`. Later `(2,2)` starts island 2. Count 2.

Marking in place (`"1" → "0"`) saves a visited set when you are allowed to mutate. Otherwise `visited.add((r, c))` and skip cells already in it.

This is **not** the backtracking maze: you do **not** unmark. A cell belongs to at most one island; once painted, it stays painted. Unmarking would recount the same land.

Time O(rows · cols): each cell is entered a constant number of times. Space O(rows · cols) in the worst case for the recursion stack (a snake of land).

Flood fill, max-area island, surrounded regions: same DFS, different payload (count cells, or paint a value).

**Trap:** `grid[r][c]` before the bounds check. Eight directions when the problem said four (diagonals connect islands or not — read the prompt). Recursing on water. A visited set of lists. Independent rows: `[[0]*cols for _ in range(rows)]`, never `[row]*rows`.

**Interview rule:** “connected cells in a grid” → matrix DFS (or BFS). Bounds, wall/water, mark, 4-dir loop. For counting components, increment once per new start, not once per cell.

## 29. Matrix BFS

DFS finds *a* path. **BFS finds a shortest path** when every step has the same cost (unweighted grid). Same reason tree BFS gives the level: FIFO processes closer cells first.

```
S . #
. . .
# . E
```

`S = (0,0)`, `E = (2,2)`, `#` is a wall, `.` is open. One shortest route has length 4 (four steps): e.g. right, down, down, right.

```python
from collections import deque

def shortest(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque([(0, 0, 0)])                 # r, c, dist
    seen = {(0, 0)}
    while q:
        r, c, d = q.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] != "#"
                    and (nr, nc) not in seen):
                seen.add((nr, nc))
                q.append((nr, nc, d + 1))
    return -1
```

Mark **when you enqueue**, not when you dequeue. If you wait until dequeue, the same cell can sit in the queue many times and you lose the O(n) bound.

Trace (dist in parentheses):

```
enqueue (0,0,0)
pop (0,0)  enqueue (1,0,1), (0,1,1)
pop (1,0)  enqueue (1,1,2)
pop (0,1)  (0,2) is wall
pop (1,1)  enqueue (2,1,3), (1,2,3)
pop (2,1)  enqueue (2,2,4)
pop (1,2)
pop (2,2)  dist 4  — done
```

DFS could wander the long way around and return 6; the first time BFS hits `E` is the shortest.

`for _ in range(len(q))` still groups a level if you would rather store `dist` outside the tuple (rotting oranges, nearest-zero, walls-and-gates — **multi-source BFS**: start the queue with every source at dist 0).

Time O(rows · cols). Extra space the same for the queue and `seen`.

**Trap:** DFS + a running `min` still can be exponential if you unmark (re-explore) or wrong if you do not — just use BFS. `list.pop(0)`. Marking on dequeue. Forgetting walls. Weighted grid (each cell a different cost) is **Dijkstra / 0-1 BFS**, not this queue.

**Interview rule:** unweighted shortest path in a grid → BFS, mark on enqueue, return dist when you pop the exit. “Every gate / every rotten orange at once” → those cells start in the queue together.

## 30. Adjacency lists

Now the graph is explicit: nodes `0..n-1` (or names), neighbors in `adj[u]`.

### DFS and BFS

```python
def dfs(u, adj, seen):
    seen.add(u)
    for v in adj[u]:
        if v not in seen:
            dfs(v, adj, seen)

def bfs(start, adj):
    seen = {start}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
```

`seen` is required. A tree has one parent; a graph can reach the same node on two paths. Without `seen`, a cycle is infinite recursion.

Undirected cycle check: skip the parent.

```python
def has_cycle(u, parent, adj, seen):
    seen.add(u)
    for v in adj[u]:
        if v == parent:
            continue
        if v in seen or has_cycle(v, u, adj, seen):
            return True
    return False
```

`A—B`, `B—C`, `C—A`: from A to B to C, C sees A already in `seen` and A is not the parent (B is) → cycle.

### Connected components

On an undirected graph, each unvisited node starts a DFS/BFS. That walk is one component. Count how many times you start.

```python
def components(n, adj):
    seen, count = set(), 0
    for u in range(n):
        if u not in seen:
            dfs(u, adj, seen)
            count += 1
    return count
```

Same idea as islands; the “grid” is now `adj`.

### Topological sort (directed, acyclic)

Order nodes so every edge `u → v` has `u` before `v`. Only possible if there is **no cycle** (a DAG). Kahn’s algorithm: BFS on nodes with in-degree 0.

```python
def topo(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque([u for u in range(n) if indeg[u] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []     # empty → cycle
```

Courses 0→1, 0→2, 1→3, 2→3: start with 0, then 1 and 2 (indegree hits 0), then 3. If 3→0 as well, `len(order) < n`.

Time O(n + e) for DFS, BFS, components, and Kahn.

**Trap:** iterating `for v in adj[u]` when `u` is missing from a dict — use `defaultdict(list)` or `adj.get(u, [])`. Directed vs undirected: topo and “course schedule” are directed. Cloning a graph, or “clone graph,” still needs `seen` as `old_node → new_node`.

**Interview rule:** general graph → adjacency list, `seen`, DFS or BFS. Components = how many times you start. Directed no-cycle order → Kahn or DFS-finish-time reverse. Grid stays a matrix unless they gave edges.

## 31. 1-D dynamic programming

DP is recursion with a table. Two ingredients, both required:

- **Overlapping subproblems** — the same smaller input is needed many times (the Fibonacci tree).
- **Optimal substructure** — a best answer is built from best answers of smaller inputs.

If you only have the first, memoize a recursive function. If you only have the second, a greedy choice might exist. DP needs both.

You already solved Fibonacci that way: naive tree Θ(φ^n), memo or `@cache` (top-down), or a loop / `dp` table (bottom-up). All three that reuse answers are DP. The loop *is* 1-D tabulation. `dp[i]` = the answer for input `i`.

Top-down for the same idea, using the decorator from the recursion lesson:

```python
from functools import cache

@cache
def climb(n):
    if n <= 2:
        return n
    return climb(n - 1) + climb(n - 2)
```

That is legal in an interview if you say it is memoized recursion. The rest of this lesson writes the table form, because that is what people mean by “the DP array.”

### The four sentences you say before coding

- State: what does `dp[i]` mean?
- Base: the smallest `i` you can answer without a look-up.
- Transition: how `dp[i]` uses earlier cells.
- Order: the loop must fill those earlier cells first.

### Climbing stairs

`dp[i]` = ways to reach step `i`, taking 1 or 2 at a time. `dp[1]=1`, `dp[2]=2`, `dp[i]=dp[i-1]+dp[i-2]`. Same recurrence as Fibonacci, different base.

```python
def climb(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```

Two variables, not an array: you only need the previous two. Time O(n), space O(1).

### House robber

Houses in a line, values `nums`. Adjacent houses cannot both be robbed. `dp[i]` = max money using houses `0..i`.

```
dp[i] = max(dp[i-1],                # skip this house
            dp[i-2] + nums[i])      # take it, so skip i-1
```

`nums = [2, 7, 9, 3, 1]`:

```
i=0  dp=2
i=1  max(2, 7) = 7
i=2  max(7, 2+9) = 11
i=3  max(11, 7+3) = 11     taking 3 does not beat skipping it
i=4  max(11, 11+1) = 12    2+9+1
```

```python
def rob(nums):
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

`prev1` is “best through last house,” `prev2` through the one before. Empty input → 0.

### Coin change (unbounded)

Fewest coins to make `amount`. Each coin may be used any times. `dp[a]` = fewest coins for amount `a`, or a large sentinel if impossible.

```python
def coin_change(coins, amount):
    inf = amount + 1
    dp = [inf] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

`coins = [1, 3, 4]`, amount 6:

```
a=1  1
a=2  1+1 → 2
a=3  min(1+1+1, one 3) → 1
a=4  min(3+1, one 4) → 1
a=5  4+1 → 2
a=6  3+3 → 2          (not 4+1+1)
```

Greedy “always the biggest coin” would take 4+1+1 = 3 coins; DP finds 2. That is why this is not greedy.

Loop **amount, then coins** or **coins, then amount** both work here because a coin can be reused. **0/1** (each item once) must walk the amount **backward** so you do not reuse the same item in this round — next lesson.

Time O(amount · len(coins)). Extra space O(amount).

**Trap:** `dp = [0]*n` with no base. Off-by-one on “n stairs” vs “n houses.” Using a 2-D table when the state is a single index. Returning `inf` instead of `-1` when impossible. Mutating a default list.

**Interview rule:** write the four sentences, then the loop. If the interviewer asks complexity, it is (number of states) × (work per state). For 1-D, that is usually O(n) or O(n · k).

## 32. 2-D dynamic programming

Same four sentences; the state now has two indexes. `dp[i][j]` is “first `i` of this, first `j` of that,” or “cell `(i, j)`.” Fill so that the cells you read are already set — typically previous row and/or the cell to the left.

Independent rows: `dp = [[0]*cols for _ in range(rows)]`, never `[row]*rows`.

### Unique paths

Grid `m × n`, only right or down, start top-left, end bottom-right. `dp[r][c]` = ways to reach `(r, c)`.

```
dp[r][c] = dp[r-1][c] + dp[r][c-1]
```

First row and first column are all 1s (only one way: always right, or always down). 3×3:

```
1 1 1
1 2 3
1 3 6
```

Six paths. Time O(m·n). You can keep two rows, or even one, because you only need the top and left.

```python
def unique_paths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]
```

### Longest common subsequence

`dp[i][j]` = LCS length of `s[:i]` and `t[:j]` (prefixes — that is why the table is `(len+1) × (len+1)` with a 0 row/column).

```
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

`s = "abc"`, `t = "ac"`:

```
      ""  a  c
""     0  0  0
a      0  1  1
b      0  1  1
c      0  1  2
```

Matching `c` reads the diagonal `1` and writes `2`. Time O(len(s)·len(t)).

### 0/1 knapsack

Each item at most once. `dp[i][w]` = best value using the first `i` items with capacity `w`.

```
skip:   dp[i-1][w]
take:   dp[i-1][w - weight[i]] + value[i]    if it fits
dp[i][w] = max(skip, take)
```

Items `(weight, value)` = `(1,6), (2,10), (3,12)`, capacity 5. After all items, `dp[5]` (1-D rolling) is 22 = 10+12, weights 2+3.

Rolling 1-D **must** walk `w` **downward**, or `dp[w - weight]` already includes this item:

```python
def knapsack(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for x in range(cap, w - 1, -1):
            dp[x] = max(dp[x], dp[x - w] + v)
    return dp[cap]
```

Unbounded knapsack (coin change as value) walks `x` **upward** so the item can be reused. The direction of the inner loop is the whole 0/1 vs unbounded distinction.

**Trap:** mixing the two inner-loop directions. LCS comparing `s[i]` instead of `s[i-1]` when the table is prefix-indexed. Unique-paths on a grid with obstacles: a blocked cell is 0 ways, and it must not copy from a neighbor that would walk through it. `[[0]*n]*m` shared rows.

**Interview rule:** 2-D DP is a table. Draw a tiny one (3×3 is enough) and fill it by hand before coding. Name whether an item can be reused; that picks the loop direction.

## 33. Bit operations

Bits are the 0/1 digits of an integer. Interviews use a handful of identities, not hardware trivia.

| Op | Meaning | Example (`5` is `101`, `3` is `011`) |
|---|---|---|
| `a & b` | 1 where both are 1 | `5 & 3 = 1` |
| `a` OR `b` | 1 where either is 1 | `5` OR `3` = `7` (`111`) |
| `a ^ b` | 1 where they differ | `5 ^ 3 = 6` (`110`) |
| `~a` | Flip bits | Python `~5 = -6` because `~n = -n-1` |
| `a << k` | Shift left k, times 2^k | `5 << 1 = 10` |
| `a >> k` | Shift right k, floor divide by 2^k | `5 >> 1 = 2` |

Python ints have unlimited width, so `1 << 100` is fine. In Java/C, shifting off a 32-bit word wraps or is undefined — mention that if they are in that world.

**Do not** write `a || b` for bits; that is boolean or. Same for `&&`.

### The identities worth memorizing

```python
n & 1                 # last bit; 1 if odd
n >> 1                # drop last bit
n & (n - 1)           # turn off the lowest set bit
n & -n                # isolate the lowest set bit (two's complement)
n > 0 and n & (n - 1) == 0    # power of two (one bit set)
```

`n & (n - 1)` on `12` (`1100`): `n-1` is `1011`, and is `1000` = 8. One set bit gone. Loop this to **count bits** in O(number of 1s):

```python
def popcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
```

Power of two: 8 is `1000`, `8 & 7 = 0`. 6 is `110`, `6 & 5 ≠ 0`. Zero is not a power of two — check `n > 0`.

### XOR

`x ^ x = 0`, `x ^ 0 = x`, XOR is commutative and associative. XOR of a range that contains every value twice, plus one unique, is the unique:

```python
def single_number(nums):
    acc = 0
    for x in nums:
        acc ^= x
    return acc
```

`[2, 3, 2, 4, 4]` → 3. No extra set.

Swap without a temp: `a ^= b; b ^= a; a ^= b` — cute, not required; `a, b = b, a` is the Python.

### Set, clear, toggle, test bit `i` (0 = least significant)

```python
n | (1 << i)          # set
n & ~(1 << i)         # clear
n ^ (1 << i)          # toggle
(n >> i) & 1          # test
```

**Trap:** `~` in Python is not a 32-bit NOT; it is `-n-1`. Mask if you needed k bits: `~n & ((1 << k) - 1)`. Using `n % 2` instead of `n & 1` is correct but slower in spirit; interviewers want the bit form when the topic is bits. Shifting by a negative count. Treating signed right-shift in other languages as unsigned.

**Interview rule:** name the identity (`n & (n-1)`, XOR-to-unique, power of two) and trace one integer in binary. If the problem is “subsets via bits,” `for mask in range(1 << n)` and `if mask & (1 << i)` — 2^n masks, same family as the backtracking subsets tree.

## 34. Costs so far

Assume n elements and ordinary fixed-size values.

| Structure / operation | Time | Extra space |
|---|---|---|
| Array get / set | O(1) | — |
| Static insert / delete at i | O(n) | — |
| Dynamic append / pop end | Amortized O(1) | Θ(n) buffer |
| Dynamic insert / pop front | O(n) | — |
| Stack push / pop / peek | O(1) | — |
| Singly get i | O(n) | — |
| Singly insert / delete head | O(1) | — |
| Singly reverse | O(n) | O(1) extra |
| Doubly delete known node | O(1) | extra `prev` per node |
| Queue enqueue / dequeue (`deque` or circular / two-end list) | O(1) | — |
| List used as queue (`pop(0)`) | O(n) dequeue | — |
| `fact(n)` recursive | O(n) time, O(n) stack | — |
| `fib(n)` naive recursive | Θ(φ^n) | O(n) stack |
| `fib(n)` memo / iterative | O(n) | O(n) memo or O(1) iterative |
| Insertion sort | O(n²) worst / O(n) best | O(1), stable |
| Merge sort | O(n log n) always | O(n), stable |
| Quicksort | O(n log n) avg / O(n²) worst | O(log n) stack avg, not stable |
| Counting sort | O(n + k) | O(n + k) |
| Binary search | O(log n) | O(1) |
| `bisect_left` / `_right` | O(log n) find, O(n) insert | — |
| Tree height / DFS / BFS | O(n) | O(h) stack or O(w) queue |
| BST search / insert / delete | O(h) | O(h) if recursive |
| Balanced BST | O(log n) | — |
| Skewed BST | O(n) | — |
| Backtracking subsets | O(2^n · n) | O(n) path |
| Heap peek | O(1) | — |
| Heap push / pop | O(log n) | — |
| `heapify` | O(n) | in place |
| Hash lookup / insert | O(1) average, O(n) worst | O(n) table |
| Adj list DFS / BFS | O(n + e) | O(n) seen |
| Adj matrix DFS / BFS | O(n²) | O(n) |
| Grid DFS / BFS | O(rows · cols) | O(rows · cols) |
| Kahn topo | O(n + e) | O(n) |
| 1-D DP (stairs, rob) | O(n) | O(1) rolling |
| Coin change | O(amount · coins) | O(amount) |
| 2-D DP (LCS, paths) | O(m · n) | O(m · n) |
| 0/1 knapsack | O(n · cap) | O(cap) rolling |
| Bit identities | O(1) or O(set bits) | — |

**Cost:** if an operation needs to *find* a node first, add that walk. “Delete in a singly list is O(1)” is only true when you already hold the predecessor. Tree costs are O(h); say log n only when the tree is balanced. Heap height is always Θ(log n) because the tree is complete. DP time is (states) × (work per state).

## 35. Ready to move on

You should be able to explain these without looking them up:

- Why `arr[i]` is O(1): `address = base + i * size`. Why a linked-list “get i” is O(n).
- Python list stores pointers, not inline C ints; it is still a dynamic array of fixed-size slots.
- Static vs dynamic: fixed capacity vs resize. Why doubling makes append amortized O(1), and why grow-by-1 is O(n²) total.
- Insert/delete in the middle of an array shifts; that is the O(n).
- Stack = LIFO = `append`/`pop` on a list. The call stack is a stack of frames.
- Valid parentheses: push openers, pop on a matching closer, stack empty at the end.
- Singly list: `head`, `next`, dummy node, reverse with `prev` / `cur` / `nxt`. Delete needs the predecessor.
- Doubly list: `prev` makes delete-given-node O(1). Tail pointer makes append O(1).
- Queue = FIFO. Circular buffer or head+tail list, not `list.pop(0)`. `deque` is the Python choice. BFS needs a queue.
- Recursion: base + smaller case. Factorial stack trace. Naive Fibonacci is a duplicate tree (`fib(8)` → 67 calls); memo / `@cache` / a loop makes it O(n) (`fib(8)` → 15). Cache only when subproblems repeat. `memo=None`, not `memo={}`. Python has no tail-call optimization and a ~1000 frame limit.
- Insertion sort: sorted prefix, shift right while `arr[j] > key` (strict `>` keeps it stable). O(n) on already-sorted, O(n²) otherwise, in-place.
- Merge sort: split, merge with `<=` for stability. Always O(n log n), O(n) extra. The recursion tree has log n levels of n work.
- Quicksort: Lomuto partition, pivot at the end, recurse on `p-1` and `p+1`. Average O(n log n), worst O(n²) when the pivot is always extreme. Not stable. Randomize the pivot.
- Counting / bucket / radix only when keys have a small range or digits. State n and k. Comparison sorts cannot beat O(n log n) worst case.
- Binary search on a sorted array: invariant `arr[lo..hi]` inclusive, `lo = mid+1` / `hi = mid-1`, `while lo <= hi`.
- First / last / count / insertion point: half-open `bisect_left` / `bisect_right` (`lo < hi`, `hi = mid`). Do not mix the two templates. Monotonic “first True” uses the same half-open loop.
- Binary tree: `left`/`right`, root vs leaf, height vs depth. A skewed tree is a linked list. Array children `2i+1` / `2i+2` only for complete trees.
- BST: whole left subtree `<` node `<` whole right. Inorder is sorted. Search/insert/delete are O(h), log n only if balanced. Validate with a `(lo, hi)` range, not just the two children.
- BST delete: 0 children drop, 1 child splice, 2 children copy inorder successor (min of right) then delete that successor.
- DFS: pre / in / post by when you visit the node. Recursion uses the call stack. Explicit preorder stack: push right then left.
- BFS: queue, level order. `for _ in range(len(q))` freezes the current level. Shortest edge-path in an unweighted tree/graph.
- Ordered set / next key `>= x`: BST walk (or `bisect` on a list). Hash tables are unordered.
- Backtracking: choose, explore, unchoose. Maze unmarks visited. `out.append(path[:])` copies. Bounds, wall, tuple `(r, c)`.
- Heap: complete tree in an array, `parent=(i-1)//2`, children `2i+1` / `2i+2`. Min-heap: parent `<=` children. Not sorted; only the root is the extreme. Height is always log n.
- Push: append, sift-up. Pop: swap with last, sift-down. Both O(log n). Peek is `heap[0]`.
- `heapify`: last parent down to 0, O(n), because most nodes have small height. n pushes would be O(n log n).
- Hash usage: exact-key O(1) average. Two-sum with `value → index`. Visited `(r, c)` tuples. Not for “next larger key” (that is a BST / `bisect`).
- Hash implementation: `hash(key) % m`, collisions (chaining or open addressing), load factor, rehash. Worst O(n) if everything collides. Python `dict` is open addressing; you still just write `{}`.
- Graph: nodes + edges. Directed or not, weighted or not. Adj list O(n+e) default; matrix O(n²) and O(1) edge check. A grid is an implicit graph.
- Matrix DFS: islands — bounds, mark (no unmark), 4-dir, increment once per new start. Time O(rows·cols).
- Matrix BFS: unweighted shortest path. Mark **on enqueue**. Dist in the queue tuple. Multi-source = several starts at dist 0.
- Adj list: `seen` or you loop on a cycle. Undirected cycle: skip parent. Components: how many DFS starts. DAG order: Kahn, empty result means a cycle.
- DP: overlapping subproblems + optimal substructure. State, base, transition, fill order. 1-D: stairs / robber / coin change. Greedy coins can be wrong.
- 2-D: draw a tiny table. Unique paths add top+left. LCS diagonal on match. 0/1 knapsack inner loop **down**; unbounded **up**.
- Bits: `&` / OR / `^` / `~` (`~n = -n-1` in Python). `n & (n-1)` drops the lowest 1. `n > 0 and n & (n-1) == 0` is a power of two. XOR of pairs leaves the unique value.

This is the end of the NeetCode beginners notes. Next is problem practice, not more structure lectures: arrays/hashing, two pointers, windows, then trees/graphs, then DP. Use recall cards and the cheat sheet before a timed set.
