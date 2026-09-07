"""Graphical user interface and window management module using MLX."""

from mlx import Mlx
import os
from collections import deque
from enum import Enum
from src.events import Event, EventTypes
import time
import typing
from src.utils import THEMES


class ConfigWin:
    def __init__(self, width: int, height: int) -> None:
        """ Initialize the ConfigWin object. """

        self.width = 260 + ((width * 2) + 1) * 10
        self.height = max(((height * 2) + 1) * 10, 360)

        self.current_theme_index = 0

        self.current_color_num = 0xFF555522
        self.cur_color_wall = 0xFF283799
        self.current_color_path = THEMES[0].get("path", 0xFFFFFFFF)

        self.cur_color_start_cell = (THEMES[self.current_theme_index]
                                     .get("start_cell", 0xFFFFFFFF))
        self.cur_color_end_cell = (THEMES[self.current_theme_index]
                                   .get("end_cell", 0xFFFFFFFF))

        self.size_cell = 10
        self.show_path = True

        self.needs_redraw = True
        self.needs_redraw_maze = False
        self.needs_redraw_maze_animation = True

        self.animation_finished_at = 0.0

        self.buttons = {
            "REGENERATE": {
                "disabled": False
            },
            "HIDE_SHOW": {
                "disabled": False
            },
            "CHANGE_WALL": {
                "disabled": False
            },
            "CHANGE_NUMBER": {
                "disabled": False
            },
        }


class TypeButton(Enum):
    REGENERATE = 0
    HIDE_SHOW = 1
    CHANGE_WALL = 2
    CHANGE_NUMBER = 3
    CHANGE_THEME = 4


class Window(Event):
    def __init__(self, width: int, height: int) -> None:
        """ initalize the Window object. """

        super().__init__()

        self.ui_img_data = None
        self.ui_size_line = None
        self.ui_img_ptr = None
        self.maze_img_data: typing.Optional[memoryview] = None
        self.maze_size_line: int
        self.maze_img_ptr = None
        self.size_line = None
        self.elements: list[dict[str, typing.Any]] = []
        self.config_win = ConfigWin(width, height)
        self.last_render_time = 0.0
        self.pixels_buffer: deque[tuple[int, int, int, int]] = deque()
        self.img_ptr = None
        self.__mlx = Mlx()
        self.__mlx_ptr = None
        self.__win_ptr = None
        self.CHAR_WIDTH = 10
        self.CHAR_HEIGHT = 20
        self.last_check_time = 0.0

    def init(self) -> None:
        """ initialize the window. """

        self.__mlx_ptr = self.__mlx.mlx_init()
        self.__win_ptr = self.__mlx.mlx_new_window(
            self.__mlx_ptr,
            self.config_win.width,
            self.config_win.height,
            "A-Maze-ing | sshadrin - jmalsam"
        )

        self.init_pixels_buffer()
        self.init_handlers()

    def init_pixels_buffer(self) -> None:
        """ initialize the pixels buffer. """

        self.maze_img_ptr = self.__mlx.mlx_new_image(
            self.__mlx_ptr,
            self.config_win.width,
            self.config_win.height
        )
        (maze_data, _,
         self.maze_size_line,
         _) = self.__mlx.mlx_get_data_addr(self.maze_img_ptr)
        self.maze_img_data = maze_data.cast('I')

        self.ui_img_ptr = self.__mlx.mlx_new_image(
            self.__mlx_ptr,
            260,
            self.config_win.height
        )
        (ui_data, _,
         self.ui_size_line, _) = self.__mlx.mlx_get_data_addr(self.ui_img_ptr)
        self.ui_img_data = ui_data.cast('I')

    def init_handlers(self) -> None:
        """ initialize the handlers. """

        self.__mlx.mlx_key_hook(self.__win_ptr, self.handle_keys, self)
        self.__mlx.mlx_hook(
            self.__win_ptr, 33, 0, lambda p: os._exit(0), self)
        # self.__mlx.mlx_hook(
        #     self.__win_ptr, 6, 1 << 6, self.handle_mouse_motion, self)

        self.__mlx.mlx_mouse_hook(self.__win_ptr, self.handle_mouse,
                                  None)

    def save_maze_pixel(self, x: int, y: int, color: int = 0xFFFFFFFF) -> None:
        """ Save the pixel at the given location. """

        if 0 <= x < self.config_win.width and 0 <= y < self.config_win.height:
            if self.maze_img_data is not None:
                self.maze_img_data[
                    (y * (self.maze_size_line // 4)) + x
                ] = color

    def save_ui_pixel(self, x: int, y: int, color: int = 0xFFFFFFFF) -> None:
        """ Save the pixel at the given location. """

        if 0 <= x < 260 and 0 <= y < self.config_win.height:
            if self.ui_img_data is not None:
                self.ui_img_data[(y * (self.ui_size_line // 4)) + x] = color

    def render(self) -> None:
        """ render the window. """

        self.__mlx.mlx_put_image_to_window(self.__mlx_ptr, self.__win_ptr,
                                           self.ui_img_ptr, 0, 0)

    def render_maze(self) -> None:
        """ render the maze. """

        self.__mlx.mlx_put_image_to_window(self.__mlx_ptr, self.__win_ptr,
                                           self.maze_img_ptr, 260, 0)

    def clear_pixels_ui(self) -> None:
        """ clear the ui pixels. """

        if self.ui_img_data is not None:
            self.ui_img_data.obj[:] = b'\x00' * (
                    260 * self.config_win.height * 4)

    def clear_maze_pixels(self, color: int = 0xFF000000) -> None:
        """ clear the maze pixels. """

        height = self.config_win.height
        pixels_per_line = self.maze_size_line // 4

        if self.maze_img_data is not None:
            for y in range(height):
                line_offset = y * pixels_per_line
                for x in range(self.config_win.width):
                    self.maze_img_data[line_offset + x] = color

        self.render_maze()

    def hit_test(
            self,
            offset_x: int,
            offset_y: int,
            x: int,
            y: int,
            width: int,
            height: int
    ) -> bool:
        """ hit testing for mouse movement. """

        return ((offset_x <= x <= offset_x + width) and
                (offset_y <= y <= offset_y + height))

    def calculate_pixel_height(self, height_input: str) -> int:
        """ calculate the height of a pixel. """

        height_str = str(height_input).strip()

        if "%" in height_str:
            percentage = height_str.split("%")[0]

            return int(self.config_win.height * int(percentage) / 100)

        return int(height_input)

    def loop(self, vertices: list[dict[str, typing.Any]]) -> None:
        """ loop through the vertices. """

        self.elements = vertices

        self.emit(EventTypes.BEGIN, None)

        self.__mlx.mlx_loop_hook(self.__mlx_ptr, self.draw, self)
        self.__mlx.mlx_loop(self.__mlx_ptr)

    def draw(self, param: typing.Any) -> int:
        """ draw the elements. """

        if self.config_win.needs_redraw:
            self.config_win.needs_redraw = False

            self.clear_pixels_ui()

            for element in self.elements:
                self.draw_element_buffer(element)

            self.render()

            for element in self.elements:
                self.draw_element_text(element)

        self.render_pixel_from_buffer_animation()

        return 0

    def need_draw_ui(self, status: bool) -> None:
        """ check if we need to draw the ui. """

        self.config_win.needs_redraw = status

    def draw_element_buffer(self, element: dict[str, typing.Any]) -> None:
        """ draw the element buffer """

        offset_x = element.get("x", 0)
        offset_y = element.get("y", 0)
        width = element.get("width", 0)
        height = element.get("height", 0)

        radius = element.get("radius", 0)
        radius = min(radius, width // 2, height // 2)

        current_bg = element.get("background-current", element.get(
            "background", 0xFF000000))

        for x in range(offset_x, width + offset_x):
            for y in range(offset_y, height + offset_y):
                draw_pixel = True

                if radius > 0:
                    relation_x = x - offset_x
                    relation_y = y - offset_y

                    # top-left
                    if relation_x < radius and relation_y < radius:
                        if ((radius - relation_x)**2 +
                                (radius - relation_y)**2 > radius**2):
                            draw_pixel = False

                    # top-right
                    if relation_x >= (width - radius) and relation_y < radius:
                        if ((relation_x - (width - radius))**2 +
                                (radius - relation_y)**2 > radius**2):
                            draw_pixel = False

                    # bottom-right
                    if relation_x < radius and relation_y >= (height - radius):
                        if ((radius - relation_x)**2 +
                                (relation_y - (height - radius))**2 >
                                radius**2):
                            draw_pixel = False

                    # bottom-right
                    if (relation_x >= (width - radius) and
                            relation_y >= (height - radius)):
                        if ((relation_x - (width - radius))**2 +
                                (relation_y - (height - radius))**2 >
                                radius**2):
                            draw_pixel = False

                if draw_pixel:
                    self.save_ui_pixel(x, y, current_bg)

    def draw_element_text(self, element: dict[str, typing.Any]) -> None:
        """ draw the element text """

        if not element.get("label"):
            return

        offset_x = element.get("x", 0)
        offset_y = element.get("y", 0)
        width = element.get("width", 0)
        height = element.get("height", 0)
        text_align = element.get("text-align", None)
        text_width = len(element["label"]) * self.CHAR_WIDTH

        # default coords
        text_x = offset_x
        text_y = offset_y

        if text_align:
            text_x = offset_x + (width - text_width) // 2
            text_y = offset_y + (height - self.CHAR_HEIGHT) // 2

        self.__mlx.mlx_string_put(self.__mlx_ptr,
                                  self.__win_ptr,
                                  text_x, text_y, element["color"],
                                  element["label"])

    def handle_keys(self, key: int, param: typing.Any) -> int:
        """ handle key presses. """

        # ESC
        if key == 65307 or key == 53:
            os._exit(0)

        return 0

    def handle_mouse_motion(self, x: int, y: int, param: typing.Any) \
            -> int:
        """ handle mouse motion. """
        changed = False

        for item in self.elements:
            offset_x = item.get("x", 0)
            offset_y = item.get("y", 0)
            width = item.get("width", 0)
            height = item.get("height", 0)
            is_hovered = self.hit_test(offset_x, offset_y, x, y, width, height)

            if is_hovered:
                if (item.get("background-current") and
                        item.get("background-hover") and
                        item.get("background-current") !=
                        item.get("background-hover")):
                    item["background-current"] = item["background-hover"]
                    changed = True
            else:
                if (item.get("background-current") and
                        item.get("background") and
                        item.get("background-current") !=
                        item.get("background")):
                    item["background-current"] = item["background"]
                    changed = True

        if changed:
            self.config_win.needs_redraw = True

        return 0

    def handle_mouse(
            self,
            button: int,
            x: int,
            y: int,
            param: typing.Any
    ) -> int:
        """ handle mouse events. """

        if button == 1:
            if time.time() - self.config_win.animation_finished_at < 0.15:
                return 0

            for item in reversed(self.elements):
                offset_x = item.get("x", 0)
                offset_y = item.get("y", 0)
                width = item.get("width", 0)
                height = item.get("height", 0)
                is_clicked = self.hit_test(offset_x,
                                           offset_y, x, y, width, height)

                if is_clicked:
                    btn_enum = item.get("target")

                    if btn_enum:
                        btn_string_key = btn_enum.name
                        btn_con = self.config_win.buttons.get(btn_string_key)

                        if btn_con and btn_con.get("disabled"):
                            return 0

                    self.emit(EventTypes.MOUSE_CLICK, item)

                    break

        return 0

    def shutdown(self) -> None:
        """ shutdown the GUI """

        self.__mlx.mlx_destroy_window(self.__mlx_ptr, self.__win_ptr)
        self.__mlx.mlx_release(self.__mlx_ptr)

    def render_pixel_from_buffer_animation(self) -> None:
        """ render the pixel buffer animation """

        if not self.config_win.needs_redraw_maze:
            return

        self.config_win.needs_redraw_maze = False

        while True:
            if not self.pixels_buffer:
                break

            x, y, size, color = self.pixels_buffer.popleft()

            for fill_x in range(x, x + size):
                for fill_y in range(y, y + size):
                    self.save_maze_pixel(fill_x, fill_y, color)

            if self.config_win.needs_redraw_maze_animation:
                self.render_maze()

        if not self.config_win.needs_redraw_maze_animation:
            self.render_maze()

        self.emit(EventTypes.RENDER_MAZE_ANIMATION_FINISHED, self)

    def update_render(self, buffer: tuple[int, int, int, int]) -> None:
        """ update the render buffer """

        self.pixels_buffer.append(buffer)

    def render_dfs(self, data: list[list[int]], color: int) -> None:
        """ render the df """

        self.config_win.needs_redraw_maze = True

        for y, row in enumerate(data):
            for x, bit in enumerate(row):
                grid_x = x * 2 + 1
                grid_y = y * 2 + 1

                for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    cell_x = (grid_x + dx) * self.config_win.size_cell
                    cell_y = (grid_y + dy) * self.config_win.size_cell

                    self.update_render((cell_x, cell_y,
                                        self.config_win.size_cell, color))

                # 0001
                if bit & 1:
                    cell_x = grid_x * self.config_win.size_cell
                    cell_y = (grid_y - 1) * self.config_win.size_cell

                    self.update_render((cell_x, cell_y,
                                        self.config_win.size_cell, color))

                # 0010
                if bit & 2:
                    cell_x = (grid_x + 1) * self.config_win.size_cell
                    cell_y = grid_y * self.config_win.size_cell

                    self.update_render((cell_x, cell_y,
                                        self.config_win.size_cell, color))

                # 0100
                if bit & 4:
                    cell_x = grid_x * self.config_win.size_cell
                    cell_y = (grid_y + 1) * self.config_win.size_cell

                    self.update_render((cell_x, cell_y,
                                        self.config_win.size_cell, color))

                # 1000
                if bit & 8:
                    cell_x = (grid_x - 1) * self.config_win.size_cell
                    cell_y = grid_y * self.config_win.size_cell

                    self.update_render((cell_x, cell_y,
                                        self.config_win.size_cell, color))

    def render_blocked_cells(
            self,
            blocked_cells: set[tuple[int, int]],
            color: int
    ) -> None:
        """ render the blocked cells """

        self.config_win.needs_redraw_maze = True

        for x, y in blocked_cells:
            grid_x = x * 2 + 1
            grid_y = y * 2 + 1

            cell_x = grid_x * self.config_win.size_cell
            cell_y = grid_y * self.config_win.size_cell
            self.update_render((cell_x,
                                cell_y, self.config_win.size_cell, color))

            # top
            if (x, y - 1) in blocked_cells:
                self.update_render((grid_x * self.config_win.size_cell,
                                    (grid_y - 1) * self.config_win.size_cell,
                                    self.config_win.size_cell, color))

            # left
            if (x - 1, y) in blocked_cells:
                self.update_render(((grid_x - 1) * self.config_win.size_cell,
                                    grid_y * self.config_win.size_cell,
                                    self.config_win.size_cell, color))

            # bottom
            if (x, y + 1) in blocked_cells:
                self.update_render((grid_x * self.config_win.size_cell,
                                    (grid_y + 1) * self.config_win.size_cell,
                                    self.config_win.size_cell, color))

            # right
            if (x + 1, y) in blocked_cells:
                self.update_render(((grid_x + 1) * self.config_win.size_cell,
                                    grid_y * self.config_win.size_cell,
                                    self.config_win.size_cell, color))

    def render_shortest_path(self, start_cell: tuple[int, int],
                             path_directions: list[str]) -> None:
        """ render the shortest path """

        self.config_win.needs_redraw_maze = True

        dir_offsets = {
            "N": (0, -1),
            "S": (0, 1),
            "W": (-1, 0),
            "E": (1, 0)
        }

        x, y = start_cell
        grid_x = x * 2 + 1
        grid_y = y * 2 + 1

        # render start cell
        self.update_render(
            (
                grid_x * self.config_win.size_cell,
                grid_y * self.config_win.size_cell,
                self.config_win.size_cell,
                self.config_win.cur_color_start_cell
            )
        )

        # render full path without start and end cell
        for direction in path_directions:
            if direction not in dir_offsets:
                continue

            dx, dy = dir_offsets[direction]

            wall_x = grid_x + dx
            wall_y = grid_y + dy
            self.update_render((wall_x * self.config_win.size_cell,
                                wall_y * self.config_win.size_cell,
                                self.config_win.size_cell,
                                self.config_win.current_color_path))

            grid_x += dx * 2
            grid_y += dy * 2

            self.update_render((grid_x * self.config_win.size_cell,
                                grid_y * self.config_win.size_cell,
                                self.config_win.size_cell,
                                self.config_win.current_color_path))

        # render end cell
        self.update_render((grid_x * self.config_win.size_cell,
                            grid_y * self.config_win.size_cell,
                            self.config_win.size_cell,
                            self.config_win.cur_color_end_cell))

    def set_status_maze_animation(self, animation: bool) -> None:
        """ set the animation of the maze """

        self.config_win.needs_redraw_maze_animation = animation
