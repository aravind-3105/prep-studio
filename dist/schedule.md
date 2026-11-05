# Interview prep schedule

Working assumption: 60–75 minutes a day, five focused days per week, one light review day, and one rest/buffer day. Use relative weeks until an interview date is confirmed. This plan focuses on Python and general coding interviews; ML theory, ML system design, and role-specific rounds need a separate track once the format is known.

## Week 1 — Python revision now

Use [Python revision notes](Python%20Basics/Revision%20Notes.md), based on your screenshot topics.

| Day | Content | Time |
|---|---|---|
| 1 | Variables, references, types, casting; arithmetic and Boolean operators | 45–60 min |
| 2 | Functions, return values, scope, defaults; conditionals and truthiness | 60 min |
| 3 | Loops; strings, indexing, slicing, immutability | 60 min |
| 4 | Lists, tuples, aliasing, shallow copies, sorting | 60–75 min |
| 5 | Sets, dictionaries, hashability, operation costs | 60–75 min |
| 6 | Stdin and exceptions; reread marked weak spots | 30–45 min |
| 7 | Rest / buffer | — |

For each revision session: 5 minutes recalling yesterday's concepts, 30–40 minutes reading and tracing examples, then 10–15 minutes explaining the key rules aloud and recording weak spots. Optional: type a worked example from memory, then compare it. No problem sets or timed questions in this first phase.

Move on when you can explain the notes' readiness checklist without prompting. If needed, repeat only the weak sections rather than restarting the whole week.

## Weeks 2–6 — DSA progression

The following is the roadmap; detailed notes and question selection come after the Python revision. Within each topic, revise the concept and implementation first, then introduce practice.

| Week | Fundamentals to revise | Practice phase, when ready |
|---|---|---|
| 2 | Big-O time/space; arrays and strings; hash maps/sets; sorting; prefix sums | Arrays/hashing, two pointers, sliding windows |
| 3 | Stack, queue/`deque`, linked lists, binary search and boundaries | Stack problems, linked-list operations, binary search |
| 4 | Recursion and call stack; tree traversals; BSTs; heaps/priority queues | DFS/BFS on trees, BST operations, top-k |
| 5 | Graph representations; visited sets; BFS/DFS; backtracking; topological sorting | Grid/graph traversal, subsets/permutations, dependencies |
| 6 | Intervals and greedy reasoning; DP states/transitions/base cases; basic bit operations | Introductory 1D/2D DP, mixed review, mock interviews |

For a five-day DSA week: days 1–2 cover concepts and worked implementations, days 3–4 cover selected problems, day 5 revisits mistakes and mixes earlier topics. Day 6 is light recall; day 7 is a buffer. Week 6 should reserve two sessions for mocks. Treat this as an initial pass, not a guarantee of mastery; extend weak topics as needed.

A later practice session can use: 10 minutes recall, 15 minutes concept review, 30–40 minutes independent coding, 10 minutes explanation and mistake review. Start with one carefully reviewed problem per session rather than chasing a problem count.

## Rebuild independent fluency

During recall and later practice, close coding agents and autocomplete. Use assistance after your own attempt to review reasoning and identify gaps. Revisit each weak concept the next day, about three days later, and the following week.

For each future problem, explain the approach before coding, state the invariant and complexity, then trace empty/single-element inputs, duplicates, and boundary cases. Record the specific mistake and the rule that prevents it.

## If the interview becomes urgent

For roughly two weeks of lead time: use 2–3 days for Python, then prioritize Big-O, arrays/hashing, two pointers/sliding windows, binary search, stacks/queues, and tree/graph traversal. Reserve the final two sessions for mocks and reviewing mistakes. Add heaps, backtracking, and DP according to the interview format and remaining time.

Start today with Week 1, Day 1. The immediate deliverable is confident recall of Python behavior; question practice begins after that revision.
