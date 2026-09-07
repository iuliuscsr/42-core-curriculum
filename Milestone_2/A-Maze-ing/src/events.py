"""Event handling module providing an enum-based event dispatcher."""

from enum import Enum, auto
import typing
from threading import Thread


class EventTypes(Enum):
    BEGIN = auto()
    MOUSE_CLICK = auto()
    FINISH = auto()
    RENDER_MAZE_ANIMATION_FINISHED = auto()


class Event:
    def __init__(self) -> None:
        """ initialize the event object """

        self._listeners: dict[
            EventTypes,
            list[typing.Callable[[typing.Any], typing.Any]]
        ] = {}

    def add_event_listener(
            self,
            event_type: EventTypes,
            callback: typing.Callable[[typing.Any], typing.Any]
    ) -> None:
        """ add an event listener """

        if event_type not in self._listeners:
            self._listeners[event_type] = []

        self._listeners[event_type].append(callback)

    def emit(self, event_type: EventTypes, *data_event: typing.Any | None) \
            -> None:
        """ emit an event """

        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                thread = Thread(target=callback, args=data_event, daemon=True)
                thread.start()
