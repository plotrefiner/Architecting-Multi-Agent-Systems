"""A tiny in-memory event bus."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict

Event = dict[str, Any]
EventHandler = Callable[[Event], None]


class EventBus:
    """Simple synchronous event bus for local demos.

    Production systems may use queues, workflow engines, cloud event systems,
    or streaming platforms. This class keeps the chapter example framework-neutral.
    """

    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, list[EventHandler]] = defaultdict(list)
        self.event_log: list[Event] = []

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        event_type = event.get("event_type")
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("Event must include a non-empty event_type.")

        self.event_log.append(event)
        for handler in self._subscribers.get(event_type, []):
            handler(event)
