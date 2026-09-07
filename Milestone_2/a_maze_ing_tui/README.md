*This project has been created as part of the 42 curriculum by jmalsam and sshadrin.*

# A-Maze-ing

## Description

**A-Maze-ing** is a Python project developed as part of the 42 curriculum.

The goal of the project is to create a maze generator that reads its parameters from a configuration file, generates a valid maze, writes it to an output file using a hexadecimal wall representation, and provides a visual representation of the generated maze.

The project supports both **perfect** and **imperfect** mazes. A perfect maze contains exactly one path between the entry and the exit, while an imperfect maze can contain additional paths.

The maze generation itself is implemented as a reusable `MazeGenerator` class in the standalone `mazegen.py` module. The module can be imported independently and packaged for later reuse, as required by the subject.

The project also includes:

* A configuration file parser.
* Randomized maze generation.
* Reproducible generation through a seed.
* A mandatory `42` pattern.
* Perfect and imperfect maze generation.
* Shortest-path calculation.
* Hexadecimal maze output.
* A reusable Python package containing the maze generator.

---

## Instructions

### Requirements

The project requires:

* Python 3.10 or later
* `pydantic >= 2.0`
* `flake8`
* `mypy`

The Python package is configured for Python 3.10+ in `pyproject.toml`.

It is recommended to use a virtual environment during development.

### Installation

Install the project dependencies and package with:

```bash
make install
```

Alternatively, the Python package can be installed directly with:

```bash
pip install .
```

The package is named `mazegen-42` and is currently version `1.0.0`.

### Running the project

The main program follows the subject's required execution format:

```bash
python3 a_maze_ing.py config.txt
```

The configuration filename can be changed, as long as it is supplied as the only argument.

A Makefile is also provided for common development tasks:

```bash
make install
make run
make debug
make lint
make clean
make build-pkg
```

### Debugging

To run the program using Python's debugger:

```bash
make debug
```

This is useful when investigating configuration errors, maze-generation issues or unexpected behaviour.

### Linting

The project follows the subject's required linting rules:

```bash
make lint
```

The mandatory checks use `flake8` and `mypy` with the flags specified by the subject.

---

# Configuration File

The configuration file consists of one `KEY=VALUE` pair per line.

Lines beginning with `#` are treated as comments and ignored.

The following keys are mandatory according to the subject:

| Key           | Description                      | Example                |
| ------------- | -------------------------------- | ---------------------- |
| `WIDTH`       | Width of the maze in cells       | `WIDTH=20`             |
| `HEIGHT`      | Height of the maze in cells      | `HEIGHT=15`            |
| `ENTRY`       | Entry coordinates `(x,y)`        | `ENTRY=0,0`            |
| `EXIT`        | Exit coordinates `(x,y)`         | `EXIT=19,14`           |
| `OUTPUT_FILE` | Output filename                  | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | Whether the maze must be perfect | `PERFECT=True`         |

An additional seed parameter is supported by the maze generator to make randomized generation reproducible.

### Example

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

The configuration parser is responsible for reading and validating the configuration before passing the parameters to the rest of the application.

Invalid configuration files, invalid parameters and impossible maze configurations should result in a clear error message rather than an unexpected crash, as required by the subject.

---

# Maze Generation Algorithm

## Depth-First Search

The project uses a **Depth-First Search (DFS)** based backtracking algorithm to generate the maze.

The algorithm starts at the entry cell and repeatedly chooses an unvisited neighbouring cell. The wall between the current cell and the selected neighbour is removed, and the new cell becomes the current cell.

When a cell has no unvisited neighbours, the algorithm backtracks to the previous cell using a stack.

The implementation uses an explicit stack rather than recursive function calls.

### Algorithm overview

```text
Start at ENTRY
      │
      ▼
Mark current cell as visited
      │
      ▼
Find unvisited neighbours
      │
      ├── Neighbours available
      │       │
      │       ▼
      │   Choose one randomly
      │       │
      │       ▼
      │   Remove the wall
      │       │
      │       ▼
      │   Move to new cell
      │       │
      │       └──────────────► Repeat
      │
      └── No neighbours
              │
              ▼
         Backtrack
              │
              ▼
       Continue until done
```

## Why DFS?

DFS was chosen because it is well suited to generating **perfect mazes** using the recursive-backtracker technique.

It provides several advantages for this project:

* It is relatively simple to implement and understand.
* It naturally produces a connected maze.
* The stack-based implementation avoids recursion-depth problems.
* Random neighbour selection creates different mazes for different seeds.
* The resulting maze can be extended with additional openings to create an imperfect maze.

The use of a dedicated seeded `random.Random` instance also makes the generation reproducible when the same seed is used.

---

# Perfect and Imperfect Mazes

The generator supports two modes through the `PERFECT` configuration option.

### Perfect maze

When `PERFECT=True`, the maze is generated using the DFS backtracking algorithm without additional wall removal.

This produces a maze with a unique path between connected cells.

### Imperfect maze

When `PERFECT=False`, additional walls are removed after the initial maze has been generated.

The current implementation removes approximately **2% of the total number of cells worth of walls**, creating additional connections and therefore potentially multiple paths through the maze.

---

# The 42 Pattern

The subject requires the generated maze to contain a visible **42** pattern made from fully closed cells. The pattern may be omitted if the maze is too small.

The implementation contains a predefined 7×5 pattern:

```text
#...###
#.....#
###.###
..#.#..
..#.###
```

The occupied cells are placed in the centre of the maze and are marked as blocked during maze generation.

The generator requires at least a 9×7 maze for the pattern to fit with the required surrounding space.

Entry and exit cells are not allowed to overlap with the pattern.

---

# Maze Representation

Each maze cell is represented by a single hexadecimal digit.

The four least significant bits represent the four possible walls:

| Bit | Direction |
| --: | --------- |
| `0` | North     |
| `1` | East      |
| `2` | South     |
| `3` | West      |

A closed wall has its corresponding bit set to `1`, while an open wall has its bit set to `0`.

The implementation uses the following values:

```text
NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8
```

For example:

```text
F = 1111
```

means that all four walls are closed.

```text
0 = 0000
```

means that all four walls are open.

The maze starts with every cell fully closed (`15`) and walls are removed as paths are created.

---

# Output File Format

The maze is written row by row, with one hexadecimal character per cell.

After the maze, the output contains an empty line followed by:

1. The entry coordinates.
2. The exit coordinates.
3. The shortest valid path from entry to exit.

This follows the output format specified by the subject.

### Example structure

```text
FFFFFFFFFFFFFFFF
F123456789ABCDEF1
F23456789ABCDEF01
FFFFFFFFFFFFFFFF

0,0
19,14
EESSSEENNEESW
```

The exact maze and solution depend on the configuration and random seed.

---

# Shortest Path

After generating the maze, the project calculates a shortest path from the entry to the exit using **Breadth-First Search (BFS)**.

BFS explores the maze level by level. For every visited cell, the implementation stores the previous cell and the direction used to reach it.

Once the exit has been found, the path is reconstructed backwards and then reversed to obtain the correct entry-to-exit sequence.

The resulting solution uses only:

```text
N
E
S
W
```

For example:

```text
EESSWN
```

represents a sequence of movements from the entry to the exit.

If no path exists, the generator reports that no path could be found.

---

# Visual Representation

The subject requires the maze to be visually displayed, with the visual representation showing:

* Maze walls
* Entry
* Exit
* Solution path

It must also provide interaction to:

* Generate and display a new maze.
* Show or hide a valid shortest path.
* Change maze wall colours.

The project follows these requirements through its visualisation component. The exact rendering method depends on the implementation of the main application.

---

# Code Reusability

One of the main requirements of the project is that the maze-generation logic must be reusable.

The project therefore separates the maze generator into the standalone `mazegen.py` module.

The module exposes the `MazeGenerator` class, which can be instantiated independently of the main application.

The package configuration explicitly exposes `mazegen` as a Python module.

## Basic Usage

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    perfect=True,
    output_file="maze.txt",
    seed=42
)

generator.generate_maze()
```

The constructor accepts the maze dimensions, entry and exit, maze type, output file and random seed.

The generated structure can also be accessed through the generator instance, including the internal `grid` representation and the calculated shortest path.

The reusable module can be built as a Python package. The subject requires the package to use the `mazegen-*` naming convention and provide all files necessary to rebuild it from the repository.

---

# Project Structure

```text
.
├── a_maze_ing.py
├── config_reader.py
├── mazegen.py
├── pyproject.toml
├── Makefile
├── config.txt
├── README.md
└── ...
```

The exact structure of the repository may contain additional files for the visualisation and testing components.

---

# Team & Project Management

The project was developed collaboratively by:

* **jmalsam**
* **sshadrin**

## Roles

### jmalsam

Responsible primarily for the maze-generation and core project logic:

* Design and implementation of the `MazeGenerator`.
* Maze representation using hexadecimal wall bitmasks.
* DFS-based maze generation.
* Perfect and imperfect maze generation.
* Integration of the `42` pattern.
* BFS-based shortest-path calculation.
* Maze output generation.
* Integration of the different components.
* Review, improvement and integration of the `config_reader`.
* Debugging and refinement of the overall project.

### sshadrin

Responsible primarily for the configuration component:

* Initial implementation of the `config_reader`.
* Parsing the configuration file.
* Handling configuration values required by the maze generator.
* Integration of the configuration component with the rest of the project.
* Testing and debugging of the configuration handling.

The `config_reader` was initially developed by **sshadrin** and subsequently reviewed and improved by **jmalsam** to ensure that it integrated correctly with the rest of the application.

This division allowed both team members to work on clearly separated components while still collaborating on the integration and refinement of the complete project.

---

# Planning & Evolution

At the beginning of the project, the work was divided into two main areas:

1. Configuration handling.
2. Maze generation and the remaining application logic.

`sshadrin` initially focused on implementing the configuration reader, while `jmalsam` focused on the maze generator and the core maze-related algorithms.

As development progressed, the components were integrated and the boundaries between them became less strict. In particular, the configuration reader was reviewed and adapted to work consistently with the maze generator and the rest of the application.

This iterative approach allowed problems discovered during integration to be addressed rather than keeping the individual components completely isolated.

---

# What Worked Well

* Separating the reusable maze generator from the main application.
* Using DFS for maze generation provided a clear and manageable algorithm.
* Using BFS for shortest-path calculation gave a straightforward way to guarantee a shortest valid path.
* Using a random seed makes maze generation reproducible.
* Separating configuration parsing from maze generation made the code easier to organize.
* Working on separate components initially allowed both team members to make progress in parallel.
* Reviewing the components together during integration helped identify inconsistencies between the configuration and maze-generation logic.

# What Could Be Improved

* More time could have been dedicated to testing edge cases earlier in the development process.
* Integration testing between the configuration reader, generator and visualisation could have started earlier.
* The planning could have included more explicit milestones for integration instead of focusing mainly on individual components.
* More automated tests would make future modifications safer and easier to validate.

---

# Tools

The following tools were used during development:

* **Python 3.10+** — main programming language.
* **Git** — version control and collaboration.
* **Make** — automation of common development commands.
* **flake8** — code-style checking.
* **mypy** — static type checking.
* **Python debugger (`pdb`)** — debugging.
* **pip / Python packaging tools** — package installation and building.
* **AI tools** — used as a support and review tool during development, particularly for checking approaches, identifying potential errors, discussing implementation details and improving documentation. AI-generated suggestions were reviewed and adapted rather than being used blindly, in accordance with the project's AI guidelines.

---

# Resources

The following resources were useful for understanding the concepts used in this project:

* Python documentation — https://docs.python.org/3/
* Python `random` module — https://docs.python.org/3/library/random.html
* Python `collections.deque` — https://docs.python.org/3/library/collections.html#collections.deque
* Python type hints — https://docs.python.org/3/library/typing.html
* Python packaging — https://packaging.python.org/
* `flake8` documentation — https://flake8.pycqa.org/
* `mypy` documentation — https://mypy.readthedocs.io/

The main algorithmic concepts used in the project are **Depth-First Search**, **Breadth-First Search**, graph traversal, backtracking and bitmask representations.

---

# Makefile

The Makefile is used to automate common project tasks.

| Command          | Purpose                           |
| ---------------- | --------------------------------- |
| `make install`   | Install project dependencies      |
| `make run`       | Run the main application          |
| `make debug`     | Run the application with `pdb`    |
| `make lint`      | Run `flake8` and `mypy`           |
| `make clean`     | Remove temporary files and caches |
| `make build-pkg` | Build the reusable Python package |

The Makefile follows the mandatory development workflow required by the subject.

---

# Conclusion

A-Maze-ing combines configuration parsing, randomized maze generation, graph algorithms, hexadecimal bitmask representation and visualisation into a single project.

The core maze generator is kept independent from the main application so that it can be reused and packaged separately. The project also demonstrates the practical use of DFS for maze generation and BFS for shortest-path calculation while respecting the specific constraints of the 42 subject.
