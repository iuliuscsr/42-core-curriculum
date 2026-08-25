#!/usr/bin/env python3
import sys
import os
from mazegen import MazeGenerator
from config_reader import ReaderConfig


class DisplayMaze:
    """Standard terminal renderer, via ANSI-Escapes to display the maze."""

    WALL_COLORS: list[str] = [
        "\033[30m",         # black
        "\033[38;5;23m",    # lila
        "\033[90m",         # darkgrey
        "\033[38;5;238m",   # violet
        "\033[38;5;65m",     # blue
        "\033[38;5;52m",     # Bordaux
    ]

    RESET: str = "\033[0m"
    YELLOW: str = "\033[33m"
    ORANGE: str = "\033[38;5;208m"
    WHITE: str = "\033[38;5;250m"

    BLOCK: str = "██"
    EMPTY: str = "  "

    def __init__(self) -> None:
        """Initializes class with attributes."""

        self.show_solution: bool = True
        self.color_index: int = 0

    def cycle_wall_colour(self) -> None:
        """Enables the ability to change wall colors."""

        self.color_index = (self.color_index + 1) % len(self.WALL_COLORS)

    def is_wall(
            self,
            maze_generator: MazeGenerator,
            x: int,
            y: int,
            bit: int
            ) -> bool:
        """Return true, if given wall bit is set on cell (x,y)."""

        return bool(maze_generator.grid[y][x] & bit)

    def cell_mask(
            self,
            maze_generator: MazeGenerator,
            x: int,
            y: int,
            ) -> str:
        """Returns the chars, being displayed within a cell."""

        pos: tuple[int, int] = (x, y)
        if pos == maze_generator.entry:
            return f"{self.YELLOW}EN{self.RESET}"
        if pos == maze_generator.exit:
            return f"{self.YELLOW}EX{self.RESET}"
        if pos in maze_generator.blocked_cells:
            return f"{self.ORANGE}{self.BLOCK}{self.RESET}"
        return self.EMPTY

    def render(
            self,
            maze_generator: MazeGenerator,
            solution: list[str] | None = None
            ) -> str:
        """Renders the generated maze from Mazegen and its solution."""

        wall_color: str = self.WALL_COLORS[self.color_index]
        height: int = maze_generator.height
        width: int = maze_generator.width

        wall: str = f"{wall_color}{self.BLOCK}{self.RESET}"
        maze: list[list[str]] = []

        for _ in range(2 * height + 1):
            row: list[str] = []
            for _ in range(2 * width + 1):
                row.append(wall)
            maze.append(row)

        for y in range(height):
            for x in range(width):
                dy, dx = y * 2 + 1, x * 2 + 1
                maze[dy][dx] = self.cell_mask(maze_generator, x, y)

                if not self.is_wall(maze_generator, x, y, MazeGenerator.NORTH):
                    maze[dy - 1][dx] = f"{wall_color}{self.EMPTY}{self.RESET}"
                if not self.is_wall(maze_generator, x, y, MazeGenerator.WEST):
                    maze[dy][dx - 1] = f"{wall_color}{self.EMPTY}{self.RESET}"

        if self.show_solution and solution is not None:
            x, y = maze_generator.entry
            for direction in solution:
                dx, dy, _, _ = maze_generator.DIRECTIONS[direction]
                nx, ny = x + dx, y + dy
                conn_y = (y * 2 + 1) + dy
                conn_x = (x * 2 + 1) + dx
                maze[conn_y][conn_x] = f"{self.WHITE}{self.BLOCK}{self.RESET}"
                x, y = nx, ny
                if (x, y) not in (maze_generator.entry, maze_generator.exit):
                    WHITE_block: str = f"{self.WHITE}{self.BLOCK}{self.RESET}"
                    maze[y * 2 + 1][x * 2 + 1] = WHITE_block

        return "\n".join("".join(row) for row in maze)


def main() -> None:
    """Displays terminal user interface."""

    if len(sys.argv) != 2:
        print("[Error] Usage: python3 a_maze_ing.py"
              " <config_file>", file=sys.stderr)
        sys.exit(1)
    try:
        config_path: str = sys.argv[1]
        reader = ReaderConfig(config_path)

        if reader.is_error():
            print("[Error] loading file configuartion:")
            for err in reader.get_errors():
                print(err, file=sys.stderr)
            sys.exit(1)

        maze = MazeGenerator(**reader.config_args())
        maze.generate_maze()
        renderer = DisplayMaze()

        while True:
            os.system("clear" if os.name != "nt" else "cls")
            solution = maze.shortest_path() if renderer.show_solution else None
            print(renderer.render(maze, solution))
            print("\n====A-Maze-ing====")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice: str = input("Choice? (1-4): ").strip()
            match choice:
                case "1":
                    maze.generate_maze()
                case "2":
                    renderer.show_solution = not renderer.show_solution
                case "3":
                    renderer.cycle_wall_colour()
                case "4":
                    print("Goodbye!")
                    break
                case _:
                    pass
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        sys.exit(1)
    except Exception as err:
        print(f"\n[Error] An unexpected error occurred: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
