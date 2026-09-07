#!/usr/bin/env python3
"""A interactive maze generator and visualization
application built with MLX."""

import sys
import random
import time
import typing
from src.utils import THEMES

missing_modules = []
REQUIRED_MODULES = [
    "mlx",
    "pydantic",
    "random",
    "collections",
    "threading",
]

for module in REQUIRED_MODULES:
    try:
        __import__(module)
    except ImportError:
        print(f"[Error] The module '{module}' is not installed!")
        missing_modules.append(module)

if missing_modules:
    exit()

from src.events import EventTypes  # noqa: E402
from src.mazegen.generator import MazeGenerator  # noqa: E402
from src.config_reader import ReaderConfig  # noqa: E402
from src.gui import Window, TypeButton  # noqa: E402
from src.utils import rgb  # noqa: E402


def is_config() -> None:
    """ check if config is correctly set """

    if len(sys.argv) != 2:
        print("Don't have config file, please set config file.")
        print("For example: -> python3 a_maze_ing.py config.txt")

        exit()


if __name__ == "__main__":
    is_config()

    config = ReaderConfig(sys.argv[1])
    if config.is_error():
        for error in config.get_errors():
            if isinstance(error, dict):
                print(f"Param: {error['param']}")
                print(f"Input: {error['error']['input']}")
                print(f"Message: {error['error']['message']}")
            else:
                print(f"Error: {error}")
            print()
        sys.exit(1)

    cfg = config.config_args()
    win = Window(cfg["width"], cfg["height"])
    maze = MazeGenerator(**cfg)
    theme = THEMES[win.config_win.current_theme_index]

    document_object_module: list[dict[str, typing.Any]] = [
        {
            # Element
            "tag": "div",
            "x": 0,
            "y": 0,
            "width": 260,
            "height": win.calculate_pixel_height("100%"),
            "background": theme["sidebar"],
        },
        {
            # Element
            "tag": "button",
            "target": TypeButton.REGENERATE,
            "x": 42,
            "y": 30,
            "width": 175,
            "height": 42,
            "radius": 8,
            "background": theme["button"],
            "background-hover": rgb(255, 0, 127),
            "background-current": theme["button"],

            # Text
            "color": 0xFFFFFF,
            "label": "Re-generate",
            "text-align": "center",
        },
        {
            # Element
            "tag": "button",
            "target": TypeButton.HIDE_SHOW,
            "x": 42,
            "y": 30 + (42 + 15),
            "width": 175,
            "height": 42,
            "radius": 8,
            "background": theme["button"],
            "background-hover": rgb(255, 0, 127),
            "background-current": theme["button"],

            # Text
            "color": 0xFFFFFF,
            "label": "Show/Hide",
            "text-align": "center",
        },
        {
            # Element
            "tag": "button",
            "target": TypeButton.CHANGE_WALL,
            "x": 42,
            "y": 30 + (42 + 15)*2,
            "width": 175,
            "height": 42,
            "radius": 8,
            "background": theme["button"],
            "background-hover": rgb(255, 0, 127),
            "background-current": theme["button"],

            # Text
            "color": 0xFFFFFF,
            "label": "Change wall",
            "text-align": "center",
        },
        {
            # Element
            "tag": "button",
            "target": TypeButton.CHANGE_NUMBER,
            "x": 42,
            "y": 30 + (42 + 15)*3,
            "width": 175,
            "height": 42,
            "radius": 8,
            "background": theme["button"],
            "background-hover": rgb(255, 0, 127),
            "background-current": theme["button"],

            # Text
            "color": 0xFFFFFF,
            "label": "Change color 42",
            "text-align": "center",
        },

        {
            # Element
            "tag": "button",
            "target": TypeButton.CHANGE_THEME,
            "x": 42,
            "y": 30 + (42 + 15)*4,
            "width": 175,
            "height": 42,
            "radius": 8,
            "background": theme["button"],
            "background-hover": rgb(255, 0, 127),
            "background-current": theme["button"],

            # Text
            "color": 0xFFFFFF,
            "label": "Change THEME",
            "text-align": "center",
        },
    ]

    def handle_click(data_event: typing.Any) -> None:
        """ Handle click events """

        target = data_event.get("target")

        if target:
            if target == TypeButton.REGENERATE:
                button_config: dict[str, bool] | None \
                    = win.config_win.buttons.get("REGENERATE")

                if button_config and button_config.get("disabled"):
                    return

                if button_config is not None:
                    button_config["disabled"] = True
                    win.set_status_maze_animation(True)

                    win.clear_maze_pixels()
                    maze.generate_maze()
                    handle_maze_final()

            if target == TypeButton.HIDE_SHOW:
                button_config = win.config_win.buttons.get("HIDE_SHOW")

                if button_config and button_config.get("disabled"):
                    return

                if button_config is not None:
                    button_config["disabled"] = True

                    if win.config_win.show_path:
                        win.config_win.show_path = False
                    else:
                        win.config_win.show_path = True

                    win.set_status_maze_animation(False)

                    win.clear_maze_pixels()
                    handle_maze_final(None)

            if target == TypeButton.CHANGE_WALL:
                button_config = win.config_win.buttons.get("CHANGE_WALL")

                if button_config and button_config.get("disabled"):
                    return

                if button_config is not None:
                    button_config["disabled"] = True
                    win.set_status_maze_animation(False)

                    win.config_win.cur_color_wall = rgb(
                        *tuple(random.randint(0, 255) for _ in range(3)))
                    win.render_dfs(maze.grid, win.config_win.cur_color_wall)

                    win.render_blocked_cells(maze.blocked_cells,
                                             win.config_win.current_color_num)

            if target == TypeButton.CHANGE_NUMBER:
                button_config = win.config_win.buttons.get("CHANGE_NUMBER")

                if button_config and button_config.get("disabled"):
                    return

                if button_config is not None:
                    button_config["disabled"] = True
                    win.config_win.current_color_num = rgb(
                        *tuple(random.randint(0, 255) for _ in range(3)))
                    win.render_blocked_cells(maze.blocked_cells,
                                             win.config_win.current_color_num)

            if target == TypeButton.CHANGE_THEME:
                win.config_win.current_theme_index = (
                        (win.config_win.current_theme_index + 1) % len(THEMES))
                theme = THEMES[win.config_win.current_theme_index]

                win.config_win.cur_color_wall = theme["wall"]
                win.config_win.current_color_path = theme["path"]
                win.config_win.cur_color_start_cell = theme["start_cell"]
                win.config_win.cur_color_end_cell = theme["end_cell"]

                for obj in document_object_module:
                    if obj.get("tag", None) == "button":
                        obj["background"] = theme["button"]
                        obj["background-current"] = theme["button"]

                    elif obj.get("tag", None) == "div":
                        obj["background"] = theme["sidebar"]

                win.set_status_maze_animation(False)
                win.clear_maze_pixels()
                win.need_draw_ui(True)
                handle_maze_final(None)

    def handle_finished_maze_animation(args: typing.Any) -> None:
        """ handle finished maze animation """

        win.config_win.buttons["REGENERATE"]["disabled"] = False
        win.config_win.buttons["HIDE_SHOW"]["disabled"] = False
        win.config_win.buttons["CHANGE_WALL"]["disabled"] = False
        win.config_win.buttons["CHANGE_NUMBER"]["disabled"] = False

        win.config_win.animation_finished_at = time.time()

    def handle_begin_loop(args: typing.Any) -> None:
        """ handle begin loop """
        maze.generate_maze()
        handle_maze_final()

    def handle_maze_final(args: typing.Any = None) -> None:
        """ handle maze final """
        win.render_dfs(maze.grid, win.config_win.cur_color_wall)
        win.render_blocked_cells(maze.blocked_cells,
                                 win.config_win.current_color_num)

        if win.config_win.show_path:
            win.render_shortest_path(
                maze.entry,
                maze.shortest_path(),
                )

    try:
        win.init()
        win.add_event_listener(EventTypes.MOUSE_CLICK, handle_click)
        win.add_event_listener(EventTypes.BEGIN, handle_begin_loop)
        win.add_event_listener(EventTypes.RENDER_MAZE_ANIMATION_FINISHED,
                               handle_finished_maze_animation)

        win.loop(document_object_module)
    except KeyboardInterrupt:
        print("Critical close app...")
    except Exception as error:
        print(error)
    finally:
        win.shutdown()
