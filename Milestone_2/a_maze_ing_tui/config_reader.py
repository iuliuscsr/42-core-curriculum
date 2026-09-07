from enum import Enum, auto
import random
import typing

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    model_validator
    )


class Config(Enum):
    """Keys recognised in the maze configuration file."""

    WIDTH = auto()
    HEIGHT = auto()
    ENTRY = auto()
    EXIT = auto()
    OUTPUT_FILE = auto()
    PERFECT = auto()
    SEED = auto()


CoordinateInt = typing.Annotated[int, Field(ge=0, le=255)]


class MazeConfig(BaseModel):
    """Validated, typed representation of a maze configuration file."""

    WIDTH: int = Field(ge=1, le=255)
    HEIGHT: int = Field(ge=1, le=255)
    ENTRY: tuple[CoordinateInt, CoordinateInt]
    EXIT: tuple[CoordinateInt, CoordinateInt]
    OUTPUT_FILE: str = Field(min_length=1, max_length=255)
    PERFECT: bool = True
    SEED: typing.Optional[int | float] = Field(
        default_factory=lambda: random.randint(0, 4294967295),
        ge=0,
        le=4294967295,
    )

    @model_validator(mode="after")
    def check_entry_and_exit(self) -> "MazeConfig":
        """Ensure ENTRY/EXIT are in-bounds and distinct."""
        if not (0 <= self.ENTRY[0] < self.WIDTH):
            raise ValueError("ENTRY x-coordinate is outside the maze")
        if not (0 <= self.ENTRY[1] < self.HEIGHT):
            raise ValueError("ENTRY y-coordinate is outside the maze")
        if not (0 <= self.EXIT[0] < self.WIDTH):
            raise ValueError("EXIT x-coordinate is outside the maze")
        if not (0 <= self.EXIT[1] < self.HEIGHT):
            raise ValueError("EXIT y-coordinate is outside the maze")
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different cells")
        return self


class ReaderConfig:
    """Reads a KEY=VALUE configuration file into a validated MazeConfig."""

    def __init__(self, name_file: str) -> None:
        """Load, parse, and validate the given configuration file."""

        self.file_path = name_file
        self.__lines: list[str] = []
        self.__params: dict[Config, typing.Any] = {}
        self.__params_errors: list[typing.Any] = []
        self.__is_error: bool = False

        if not self.__read_file():
            return
        self.__parser()
        self.__check_params()

    def __read_file(self) -> bool:
        """Read non-comment, non-empty lines from
           the config file, checks vor validity."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.__lines.append(line)
            return True
        except OSError:
            self.__is_error = True
            self.__params_errors.append(
                f"Config file '{self.file_path}' not found or unreadable"
            )
            return False

    def __parser(self) -> None:
        """Parse each KEY=VALUE line into the internal params dict."""

        for param in self.__lines:
            try:
                key_name, value = param.split("=", 1)
                config_key = Config[key_name.strip()]
                self.__params[config_key] = self.__detect_type(value)
            except (ValueError, KeyError):
                self.__params_errors.append(param)

    def __check_params(self) -> bool:
        """Validate collected params against the MazeConfig schema."""

        raw: dict[Config, typing.Any] = self.__params
        try:
            response = MazeConfig(
                WIDTH=typing.cast(typing.Any, raw.get(Config.WIDTH)),
                HEIGHT=typing.cast(typing.Any, raw.get(Config.HEIGHT)),
                ENTRY=typing.cast(typing.Any, raw.get(Config.ENTRY)),
                EXIT=typing.cast(typing.Any, raw.get(Config.EXIT)),
                OUTPUT_FILE=typing.cast(
                    typing.Any, raw.get(Config.OUTPUT_FILE)
                ),
                PERFECT=typing.cast(
                    typing.Any, raw.get(Config.PERFECT, True)
                ),
                SEED=typing.cast(typing.Any, raw.get(Config.SEED)),
            )

            self.__params = {
                Config.WIDTH: response.WIDTH,
                Config.HEIGHT: response.HEIGHT,
                Config.ENTRY: response.ENTRY,
                Config.EXIT: response.EXIT,
                Config.OUTPUT_FILE: response.OUTPUT_FILE,
                Config.PERFECT: response.PERFECT,
                Config.SEED: response.SEED,
            }
            return True

        except ValidationError as error:
            self.__is_error = True

            for item_error in error.errors():
                self.__params_errors.append({
                    "param": (
                        item_error["loc"][0] if item_error["loc"]
                        else "unknown"
                    ),
                    "error": {
                        "loc": item_error.get("loc"),
                        "input": item_error.get("input"),
                        "message": item_error.get("msg"),
                    }
                })
            return False

    def __detect_type(self, value: str) -> typing.Any:
        """Infer bool/tuple/int/float/str from a raw string value."""

        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        if "," in value:
            try:
                return tuple(int(i.strip()) for i in value.split(","))
            except ValueError:
                pass

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        return value

    def is_error(self) -> bool:
        """Return whether the config failed to load or validate."""

        return self.__is_error

    def get_errors(self) -> list[typing.Any]:
        """Return the list of parsing/validation error entries."""

        return self.__params_errors

    def get_value(self, key: Config) -> typing.Any:
        """Return a single validated config value."""

        return self.__params.get(key)

    def config_args(self) -> dict[str, typing.Any]:
        """Map the validated params to MazeGenerator constructor."""
        return {
            "width": self.get_value(Config.WIDTH),
            "height": self.get_value(Config.HEIGHT),
            "entry": self.get_value(Config.ENTRY),
            "exit_": self.get_value(Config.EXIT),
            "perfect": self.get_value(Config.PERFECT),
            "output_file": self.get_value(Config.OUTPUT_FILE),
            "seed": self.get_value(Config.SEED),
        }
