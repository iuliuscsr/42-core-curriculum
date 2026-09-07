#!/usr/bin/env python3
"""
Reusable maze generation module.
Provides a MazeGenerator, a standalone class to generate perfect or
imperfect mazes with a hexadecimal wall representation
"""

import random
import sys
from collections import deque


class MazeGenerator():
    """Generates a maze as a grid of wall-bitmask integers."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    DIRECTIONS = {
        'N': (0, -1, NORTH, SOUTH),
        'E': (1, 0, EAST, WEST),
        'S': (0, 1, SOUTH, NORTH),
        'W': (-1, 0, WEST, EAST)
    }

    PATTERN_42 = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]
    PATTERN_WIDTH = 7
    PATTERN_HEIGHT = 5

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit_: tuple[int, int],
            perfect: bool,
            output_file: str,
            seed: int | None
    ) -> None:
        """Set up generation parameters."""

        super().__init__()

        self._rng = random.Random(seed)
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.perfect = perfect
        self.output_file = output_file
        self.seed = seed
        self.rng = random.Random(seed)
        self.grid: list[list[int]] = []
        self.blocked_cells: set[tuple[int, int]] = set()
        self.initialize_closed_grid()

    def generate_maze(self) -> tuple[list[list[int]], list[str]]:
        """Generates the maze."""

        self.initialize_closed_grid()
        self.create_42_pattern()
        self.carve_maze()
        if not self.perfect:
            self.imperfect_maze()
        self.hex_output()

        return self.grid, self.shortest_path()

    def initialize_closed_grid(self) -> None:
        """Initializes a closed grit with zero open walls."""

        self.grid = [
                    [15 for _ in range(self.width)] for _ in range(self.height)
                ]

    def remove_wall(self, x: int, y: int, wall: int) -> None:
        """Removes a chosen wall."""

        if self.grid[y][x] & wall:
            self.grid[y][x] -= wall

    def create_path(
            self,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            direction: str
            ) -> None:
        """Creates a path between two cells."""

        _, _, wall_from, wall_to = self.DIRECTIONS[direction]
        self.remove_wall(x1, y1, wall_from)
        self.remove_wall(x2, y2, wall_to)

    def create_42_pattern(self) -> None:
        """Embeds the '42' pattern within the grid"""

        min_width = self.PATTERN_WIDTH + 2
        min_height = self.PATTERN_HEIGHT + 2

        if self.width < min_width or self.height < min_height:
            print(
                f"Error: Maze dimensions {self.width}x{self.height}"
                f"are too small for generating '42' pattern. The "
                f"minimum needed is {min_width}x{min_height}.",
                file=sys.stderr
            )
            return
        start_x = (self.width - self.PATTERN_WIDTH) // 2
        start_y = (self.height - self.PATTERN_HEIGHT) // 2

        for py in range(self.PATTERN_HEIGHT):
            for px in range(self.PATTERN_WIDTH):
                if self.PATTERN_42[py][px] == 1:
                    gx = start_x + px
                    gy = start_y + py
                    if (gx, gy) == self.entry or (gx, gy) == self.exit:
                        print(
                            "Error: Maze ENTRY or EXIT overlaps"
                            "with '42' pattern.", file=sys.stderr
                        )
                        return
        for py in range(self.PATTERN_HEIGHT):
            for px in range(self.PATTERN_WIDTH):
                if self.PATTERN_42[py][px] == 1:
                    gx = start_x + px
                    gy = start_y + py
                    self.blocked_cells.add((gx, gy))
                    self.grid[gy][gx] = 15

    def check_neighbors(
            self,
            x: int,
            y: int,
            visited: set[tuple[int, int]]
            ) -> list[tuple[str, int, int]]:
        """Checks a coordinate for available neighbors by
           validating each direction within a set."""

        neighbors: list[tuple[str, int, int]] = []
        for direction, (dx, dy, _, _) in self.DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in visited:
                    neighbors.append((direction, nx, ny))
        return neighbors

    def carve_maze(self) -> None:
        """Carves a perfect maze, using the DFS algorithm
           (depth-first-search) a stack based
            backtracker, skipping blocked cells."""

        visited: set[tuple[int, int]] = set(self.blocked_cells)
        visited.add(self.entry)
        stack: list[tuple[int, int]] = [self.entry]
        while stack:
            x, y = stack[-1]
            neighbors: list[tuple[str, int, int]] = self.check_neighbors(
                x, y, visited
            )
            if not neighbors:
                stack.pop()
                continue
            direction, nx, ny = self.rng.choice(neighbors)
            self.create_path(x, y, nx, ny, direction)
            visited.add((nx, ny))
            stack.append((nx, ny))

    def shortest_path(self) -> list[str]:
        """Finds the shortest way from entry to exit using the bfs
        algorithm (breadth-first-seach), analog to a reverse linked list."""

        prev_next: dict[
            tuple[int, int], tuple[tuple[int, int], str] | None
        ] = {}
        visited: set[tuple[int, int]] = {self.entry}
        memory: deque[tuple[int, int]] = deque([self.entry])
        while memory:
            x, y = memory.popleft()
            if (x, y) == self.exit:
                break
            for direction, (nx, ny, wall, _) in self.DIRECTIONS.items():
                if self.grid[y][x] & wall:
                    continue
                neighbor = (x + nx, y + ny)
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                prev_next[neighbor] = ((x, y), direction)
                memory.append(neighbor)
        else:
            raise Exception("No path found between entry and exit")
        path_coords: list[str] = []
        current = self.exit
        while current != self.entry:
            step = prev_next.get(current)
            assert step is not None
            previous, direction = step
            path_coords.append(direction)
            current = previous
        path_coords.reverse()
        return path_coords

    def hex_output(self) -> None:
        """
        Writes the maze in an output file using one hexadecimal digit per cell.
        """

        hex_string: list[str] = []

        for y in range(self.height):
            for x in range(self.width):
                bit: int = self.grid[y][x]
                hex_string.append(f"{bit:X}")
            hex_string.append("\n")

        output_maze: str = "".join(hex_string)
        output_solution: str = "".join(self.shortest_path())
        entry_x, entry_y = (self.entry)
        exit_x, exit_y = (self.exit)
        entry_str = f"{entry_x},{entry_y}"
        exit_str = f"{exit_x},{exit_y}"

        with open(self.output_file, "w", encoding="utf-8") as file:
            file.write(output_maze)
            file.write("\n")
            file.write(f"{entry_str}\n")
            file.write(f"{exit_str}\n")
            file.write(output_solution)

    def imperfect_maze(self) -> None:
        """Removes 5% of total walls, in order to make the maze imperfect."""

        percentage: float = 0.05
        tot_cells: int = self.height * self.width
        remove_tot: int = int(tot_cells * percentage)
        remove_curr: int = 0

        while remove_curr < remove_tot:
            x: int = self.rng.randint(0, self.width - 1)
            y: int = self.rng.randint(0, self.height - 1)
            if (x, y) in self.blocked_cells:
                continue
            direction: str = self.rng.choice(list(self.DIRECTIONS.keys()))
            dx, dy, wall_from, _ = self.DIRECTIONS[direction]
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and (nx, ny) not in self.blocked_cells
            ):
                if self.grid[y][x] & wall_from:
                    self.create_path(x, y, nx, ny, direction)
                    remove_curr += 1
