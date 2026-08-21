#!/usr/bin/env python3
from mazegen import MazeGenerator


class DisplayMaze:
    """Standard terminal renderer, via ANSI-Escapes to display the maze."""

    WALL_COLORS: list[str] = [
        "\033[37m",         # white
        "\033[90m",         # grey
        "\033[94m",         # lightblue
        "\033[36m",         # cyan
        "\033[38;5;141m",   # lila
    ]

    RESET: str = "\033[0m"
    YELLOW: str = "\033[33m"
    ORANGE: str = "\033[38;5;208m"
    RED: str = "\033[31m"

    BLOCK: str = "██"
    EMPTY: str = "  "

    def __init__(self) -> None:
        """Initializes class with attributes."""
        self.show_path: bool = False
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
            wall_color: str
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

    def render(self, maze_generator: MazeGenerator) -> str:
        wall_color: str = self.WALL_COLORS[self.color_index]
        height: int = maze_generator.height
        width: int = maze_generator.width

        maze = [
            [f"{wall_color}{self.BLOCK}{self.RESET}" for _ in range(2 * width + 1)]
            for _ in range(2 * height + 1)
        ]

        for y in range(height):
            for x in range(width):
                dy, dx = y * 2 + 1, x * 2 + 1
                maze[dy][dx] = self.cell_mask(maze_generator, x, y, wall_color)
                if not self.is_wall(maze_generator, x, y, MazeGenerator.NORTH):
                    maze[dy - 1][dx] = f"{wall_color}{self.EMPTY}{self.RESET}"
                if not self.is_wall(maze_generator, x, y, MazeGenerator.WEST):
                    maze[dy][dx - 1] = f"{wall_color}{self.EMPTY}{self.RESET}"
        return "\n".join("".join(row) for row in maze)


def main() -> None:
    maze = MazeGenerator(width=30, height=30, entry=(0, 0), exit_=(29, 29), perfect=True, seed=None)
    maze.generate_maze()

    renderer = DisplayMaze()

    print("=== TEST 1: Standard-Color ===")
    print(renderer.render(maze))

    print("\n=== TEST 2: Change-Color ===")
    renderer.cycle_wall_colour()
    print(renderer.render(maze))


if __name__ == "__main__":
    main()
