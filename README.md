*This project has been created as part of the 42 curriculum by jmalsam, jawosylu.*

# push_swap

## Description

push_swap is a sorting algorithm project from the 42 curriculum. The goal is to sort a stack of integers using two stacks (`a` and `b`) and a restricted set of operations, while minimizing the total number of operations used.

The program implements four distinct sorting strategies and selects the appropriate one based on a strategy flag or, by default, adapts automatically based on the measured disorder of the input. The project demonstrates algorithmic complexity in a concrete, hands-on way — sorting is easy, but sorting *efficiently* with only two stacks and eleven allowed moves is an entirely different challenge.

The core data structure is a **doubly linked list**, allowing efficient manipulation of both ends of each stack. An `env` struct tracks operation counts, strategy selection, benchmark data, and disorder metrics across the entire program.

## Instructions

### Compilation

```bash
make
```

This produces the `push_swap` binary. To clean up:

```bash
make clean    # removes object files
make fclean   # removes object files and binary
make re       # fclean + all
```

### Usage

```bash
./push_swap [--simple | --medium | --complex | --adaptive] [--bench] <integers>
```

**Strategy flags (optional):**

| Flag | Algorithm | Complexity |
|------|-----------|------------|
| `--simple` | Bubble sort | O(n²) |
| `--medium` | Chunk sort | O(n√n) |
| `--complex` | Radix sort | O(n log n) |
| `--adaptive` | Disorder-based selection | varies |

If no strategy flag is given, `--adaptive` is used by default.

**Benchmark flag:**

Adding `--bench` prints sorting statistics to `stderr` after sorting:
- Disorder value (percentage, two decimals)
- Strategy name and complexity class
- Total number of operations
- Per-operation counts (sa, sb, ss, pa, pb, ra, rb, rr, rra, rrb, rrr)

### Examples

```bash
# Sort five numbers with the default adaptive strategy
./push_swap 5 3 1 4 2

# Force radix sort and count operations
ARG="4 67 3 87 23"; ./push_swap --complex $ARG | wc -l

# Verify correctness with the provided checker
ARG="4 67 3 87 23"; ./push_swap --complex $ARG | ./checker_linux $ARG

# Run with benchmark output
./push_swap --bench --adaptive 5 3 1 4 2

# Large input performance test
shuf -i 0-9999 -n 500 > args.txt && ./push_swap $(cat args.txt) | wc -l
```

### Error handling

The program prints `Error` to `stderr` and exits on:
- Non-integer arguments
- Integers outside the valid `int` range
- Duplicate values

```bash
./push_swap 0 one 2 3     # Error
./push_swap 3 2 3         # Error
```

## Algorithms

### Disorder metric

Before any moves are made, the program computes a disorder value between 0 (already sorted) and 1 (worst-case order) by counting inversions across all pairs:

```
disorder = number_of_inverted_pairs / total_pairs
```

This value is used by the adaptive strategy to choose the most suitable algorithm at runtime.

### Simple — Bubble Sort (O(n²))

Bubble sort repeatedly scans the stack, swapping adjacent elements that are out of order, until no swaps are needed. Each pass bubbles the largest unsorted element to the bottom. In the push_swap model, this translates to sequences of `sa`, `ra`, and `rra` operations.

Chosen as the simple baseline because it is straightforward to adapt to a stack: a single pass maps cleanly to rotate-compare-swap cycles. It is well-suited for small or nearly-sorted inputs where the low constant factor matters more than asymptotic class.

**Space:** O(1) additional push_swap operations overhead (no extra stack usage beyond working space).

### Medium — Chunk Sort (O(n√n))

The input is divided into approximately √n equal-sized chunks based on normalized index ranges. Elements belonging to each chunk are pushed to stack `b` in order; once a full chunk is on `b`, the elements are pushed back to `a` in sorted order by finding the min/max and rotating accordingly.

Chunk sort sits between the simplicity of bubble sort and the overhead of a full O(n log n) approach. For medium-disorder inputs, the chunk size keeps rotation costs bounded per group, giving a practical operation count well below a naive O(n²) approach without the implementation complexity of radix or merge sort.

**Space:** uses stack `b` as working space; at most O(√n) elements on `b` at any point per chunk pass.

### Complex — Radix Sort (O(n log n))

Values are first normalized to non-negative indices (0 to n−1). Sorting then proceeds bit by bit (LSD radix sort): for each bit position, elements whose bit is 0 are pushed to `b`, elements whose bit is 1 stay or are rotated in `a`, then all of `b` is pushed back to `a`. This is repeated for log₂(n) bit rounds.

Radix sort adapts naturally to the two-stack model because the 0/1 bit decision maps directly to a `pb`/`ra` branch, making it one of the cleanest O(n log n) implementations possible in this constraint. Normalization ensures the bit width stays at ⌈log₂(n)⌉, giving a predictable and tight operation budget.

**Space:** stack `b` holds at most n elements during each bit pass; total extra operations are O(n log n).

### Adaptive strategy

The adaptive algorithm measures disorder first and then delegates:

| Disorder range | Strategy used | Target complexity |
|----------------|---------------|-------------------|
| < 0.2 | Bubble sort | O(n²) |
| 0.2 – 0.49 | Chunk sort | O(n√n) |
| ≥ 0.5 | Radix sort | O(n log n) |

**Rationale for thresholds:**

- Below 0.2, the stack is nearly sorted. Bubble sort's low operation overhead per pass means it converges in very few total moves; heavier algorithms would waste operations on setup.
- Between 0.2 and 0.5, partial disorder makes bubble sort inefficient but the input is structured enough for chunk sort's locality to shine without the full overhead of bit-level passes.
- At and above 0.5, the input is effectively random. Chunk sort degrades toward O(n²) in the worst case here, while radix sort's consistent O(n log n) behaviour makes it the safe, predictable choice.

## Resources

- Knuth, D. E. — *The Art of Computer Programming, Vol. 3: Sorting and Searching* — the foundational reference for sorting algorithms and complexity analysis.
- [Wikipedia — Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) — overview of complexity classes and algorithm families.
- [Wikipedia — Radix sort](https://en.wikipedia.org/wiki/Radix_sort) — LSD/MSD radix sort explanation and complexity derivation.
- [Visualgo — Sorting visualizations](https://visualgo.net/en/sorting) — interactive visualization of bubble, insertion, and other O(n²) sorts.
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/) — quick reference for time and space complexity across common algorithms.

### AI usage

AI (Claude) was used during this project for the following tasks:
- Explaining the theoretical complexity of radix sort in the two-stack model and helping reason about why bit-width equals ⌈log₂(n)⌉ after normalization.
- Discussing trade-offs between chunk sort bucket sizes and operation counts to motivate the √n choice.
- Generating this README skeleton based on our implemented algorithms and project structure.

All AI-generated content was reviewed, tested, and rewritten where necessary by both team members before inclusion in the project.

## Contributors

| Login | Contributions |
|-------|---------------|
| jmalsam | [describe your part] |
| jawosylu | [describe their part] |
