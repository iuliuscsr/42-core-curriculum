*This project has been created as part of the 42 curriculum by jawosylu, jmalsam.*

---

# push_swap

> Sort data on a stack with a limited set of instructions, using the lowest possible number of operations.

---

## Description

`push_swap` is a sorting algorithm project from the 42 curriculum. The goal is to sort a list of integers stored in **stack a** using only two stacks (`a` and `b`) and a restricted set of operations, while minimising the total number of moves.

What makes this project unique is not just sorting — it's sorting *efficiently*. The program must select an appropriate strategy based on the input size and its disorder level. Four distinct sorting strategies are embedded into the binary, each targeting a different complexity class.

**Available operations:**

| Operation | Description |
|-----------|-------------|
| `sa` / `sb` / `ss` | Swap top two elements of stack a / b / both |
| `pa` / `pb` | Push top of b to a / top of a to b |
| `ra` / `rb` / `rr` | Rotate stack a / b / both upward |
| `rra` / `rrb` / `rrr` | Reverse-rotate stack a / b / both |

---

## Instructions

### Compilation

```bash
make        # Compiles push_swap
make bonus  # Compiles the checker program
make clean  # Removes object files
make fclean # Removes object files and binaries
make re     # Full recompile
```

### Usage

```bash
./push_swap [--simple | --medium | --complex | --adaptive] <integers> [--bench]
```

**Strategy flags (optional):**

| Flag | Algorithm | Complexity |
|------|-----------|------------|
| `--simple` | Bubble Sort / Selection Sort | O(n²) |
| `--medium` | Chunk Sort | O(n√n) |
| `--complex` | Radix Sort (LSD) | O(n log n) |
| `--adaptive` | Adaptive (default) | Depends on disorder |

If no flag is given, `--adaptive` is used automatically.

**Benchmark mode:**

Add `--bench` to any command to print metrics to `stderr`:
- Computed disorder (% with 2 decimals)
- Strategy name and complexity class
- Total number of operations
- Per-operation breakdown (`sa`, `sb`, `ss`, `pa`, `pb`, `ra`, `rb`, `rr`, `rra`, `rrb`, `rrr`)

```bash
./push_swap --adaptive 4 67 3 87 23 --bench
./push_swap --complex $(shuf -i 0-9999 -n 500) | wc -l
```

### Checker (Bonus)

```bash
ARG="4 67 3 87 23"
./push_swap --complex $ARG | ./checker $ARG
# Output: OK
```

### Error handling

```bash
./push_swap 1 2 one 4    # Error: non-integer argument
./push_swap 1 2 2 4      # Error: duplicate values
./push_swap              # No output, returns prompt
```

---

## Algorithms

### Disorder Metric

Before any sorting begins, the program computes a **disorder score** between `0.0` (perfectly sorted) and `1.0` (worst case). It counts all inversions — pairs `(i, j)` where `i < j` but `a[i] > a[j]` — and divides by the total number of pairs:

```
disorder = inversions / (n * (n - 1) / 2)
```

This metric drives the adaptive strategy selection.

---

### Normalisation

All algorithms that rely on index-based logic (chunk sort, radix sort, selection sort for 3 elements) begin with a **normalisation step**. The function `ft_normalize` maps each element's raw value to its rank (0 to n−1) by:

1. Copying the stack contents into a temporary array.
2. Sorting the array in place using a simple selection sort.
3. Walking back over the stack and assigning each node its rank as `index`.

This makes the sorting logic independent of the actual values and simplifies bit-based or range-based operations.

---

### 1. Simple — Bubble Sort & Selection Sort — O(n²)

**For n ≤ 5 (both algorithms):**
`selection_sort` handles sizes 2 and 3 directly with hardcoded optimal move sequences, then for n > 3 it iteratively finds the minimum of stack a, rotates it to the top via `ra`/`rra` (choosing the shorter direction), pushes it to b with `pb`, and after reducing a to 3 elements calls the 3-element handler. All elements are then pushed back from b to a with `pa`.

**Bubble Sort (n > 5):**
Iterates over stack a with a sliding window of `ra` moves. Each time the top two elements are in the wrong order, `sa` is called. After a full pass (size−1 rotations + one final `ra` to realign), the loop repeats until `is_sorted` returns true. Because `bubble_sort` delegates to `selection_sort` for n ≤ 5, both entry points converge to the same small-case handler.

**Why:** These algorithms need no normalisation and are straightforward to implement and debug. They are correct for any input and serve as the verified baseline. For large inputs their operation count climbs as O(n²), but for nearly-sorted inputs (low disorder) the inner loop terminates early, making them competitive with more complex strategies in that regime.

**Complexity argument:** At most n passes, each requiring O(n) rotate/swap operations → O(n²) push_swap operations in the worst case.

---

### 2. Medium — Chunk Sort — O(n√n)

**Phase 1 — push to b in chunk windows:**
After normalisation, the input is divided into chunks of size `chunk_size ≈ √n` (computed as the largest integer `k` such that `(k+1)² ≤ n`). The algorithm maintains a sliding upper bound `chunk_max` and scans stack a with `ra`. Any element whose normalised index falls within `[0, chunk_max]` is pushed to b with `pb`; otherwise it is skipped with `ra`. Once `chunk_size` elements have been pushed, `chunk_max` advances by `chunk_size`.

**rb optimisation:**
Immediately after each `pb`, if the freshly pushed element's index falls in the lower half of the current chunk window (index ≤ `chunk_max − chunk_size / 2`), it is sunk to the bottom of b with `rb`. This clusters larger-index elements — those needed sooner when pushing back — near the top of b, and reduces the average rotation distance during phase 2.

**Phase 2 — push back to a in descending order:**
`push_chunk_back_a` repeatedly locates the global maximum in b using `ft_find_max_pos`, then rotates it to the front via `rb` (forward, if it is in the first half) or `rrb` (backward, if it is in the second half), and pushes it to a with `pa`. Since each element lands at the top of a in descending index order, a ends up sorted ascending.

**Why:** Dividing into √n groups means each element costs at most O(√n) rotations to locate, both during the push-to-b scan and the push-back. The rb optimisation in phase 1 cuts the average cost of phase 2 by roughly 10–15% in practice without adding complexity.

**Complexity argument:** n pushes × O(√n) average rotation cost = O(n√n) push_swap operations.

---

### 3. Complex — Radix Sort (LSD) — O(n log n)

After normalisation, radix sort processes the normalised indices bit by bit from the least significant bit (LSB) to the most significant bit. The number of passes is `max_bits(n) = ⌈log₂(n)⌉`.

In each pass, every element of stack a is examined once:
- If its current bit is `0`: `pb` (push to b).
- If its current bit is `1`: `ra` (rotate to the back of a).

After all n elements have been processed, the entire b is flushed back to a with `pa`. After `⌈log₂(n)⌉` passes the indices in a are in ascending order.

**Why:** Radix sort maps cleanly onto the two-stack constraint. It requires no comparisons between elements — only bit tests — and processes every element exactly once per pass. The operation count grows as O(n log n) regardless of the initial disorder, making it the best strategy for large, heavily shuffled inputs.

**Complexity argument:** ⌈log₂(n)⌉ passes × 2n operations per pass (n bit-check moves + n pushes back) = O(n log n) push_swap operations.

---

### 4. Adaptive Algorithm

The adaptive strategy measures the disorder of the input and selects the most appropriate algorithm automatically:

| Disorder range | Strategy used | Complexity |
|----------------|---------------|------------|
| `disorder < 0.2` | Selection Sort | O(n²) |
| `0.2 ≤ disorder < 0.5` | Chunk Sort | O(n√n) |
| `disorder ≥ 0.5` | Radix Sort (LSD) | O(n log n) |

**Threshold rationale:**
- Below `0.2`: Only a small fraction of pairs are inverted. The overhead of normalisation and chunk or radix passes outweighs the benefit. Selection sort resolves the few out-of-place elements cheaply.
- Between `0.2` and `0.5`: Partial disorder makes range-based grouping effective. Chunk sort avoids the full bitwise pass overhead while still reducing the search cost per element from O(n) to O(√n).
- Above `0.5`: More than half of all pairs are inverted. Only a logarithmic algorithm scales acceptably for large n. Radix sort's fixed O(n log n) cost is predictable and independent of the specific disorder pattern.

---

## Performance Targets

| Input size | Pass | Good | Excellent |
|------------|------|------|-----------|
| 100 numbers | < 2000 ops | < 1500 ops | < 700 ops |
| 500 numbers | < 12000 ops | < 8000 ops | < 5500 ops |

---

## Contributors

| Login | Contributions |
|-------|--------------|
| **jawosylu** |chunk sort algorithm, bubble sort algorithm, checker implementation |
| **jmalsam** | radix sort algorithm, selection sort algorithm, benchmark mode (`--bench`) |

Both contributors were present and involved in the design of the overall architecture, the dispatch logic (`dispatch_algorithm.c`), the Input parsing & validation, strategy flags (`--simple`, `--medium`, `--complex`, `--adaptive`), stack operations and the adaptive strategy thresholds.

---

## Resources

### Core References

- Knuth, D. E. — *The Art of Computer Programming, Vol. 3: Sorting and Searching* — foundational reference for sorting complexity and inversion counting
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/) — quick reference for time and space complexity across common algorithms
- [Visualgo — Sorting Algorithms](https://visualgo.net/en/sorting) — interactive step-by-step visualisation of sorting algorithms including radix and selection sort

### Algorithm-Specific

- [Radix Sort — GeeksForGeeks](https://www.geeksforgeeks.org/radix-sort/) — explanation of LSD radix sort with worked examples
- [Counting Inversions in an Array — GeeksForGeeks](https://www.geeksforgeeks.org/counting-inversions/) — background on the inversion-counting formula used for the disorder metric
- [Bucket Sort — Wikipedia](https://en.wikipedia.org/wiki/Bucket_sort) — conceptual basis for dividing a range into equal-width buckets (chunks)
- [Stack Data Structure — GeeksForGeeks](https://www.geeksforgeeks.org/stack-data-structure/) — reference for stack operations and linked-list-based stack implementation
- [Push_swap visualizer by o-reo](https://github.com/o-reo/push_swap_visualizer) — used throughout development to visually validate and debug operation sequences
- [push_swap — The least amount of moves with two stacks (Jamie Dawson, Medium)](https://medium.com/@jamierobertdawson/push-swap-the-least-amount-of-moves-with-two-stacks-d1e76a71789a) — walkthrough of chunk-based and radix approaches with operation count analysis
- [push_swap — 42 Project Explained (YouTube, oceano)](https://www.youtube.com/watch?v=OaG81sDEpVk) — video walkthrough of the project requirements and algorithm strategy overview

### AI Usage

AI tools (Claude) were used in the following limited and reviewed ways during this project:

- **README drafting:** The structure and wording of this README were initially drafted with AI assistance, then reviewed, corrected, and expanded by both contributors to accurately reflect our implementation.

All AI-generated content was critically reviewed, tested against the checker, and understood by both learners before being included in the project. No function was copied from AI output without full understanding and peer review.