from typing import Any, Dict, List, Type

from .abstractions import INotification, IRequest


class Mediator:
    """Mediator implementation for handling requests and notifications."""

    def __init__(self):
        """Initialize the mediator."""
        self._request_handlers: Dict[Type[Any], Any] = {}
        self._notification_handlers: Dict[Type[Any], List[Any]] = {}

    def register_request_handler(self, request_type: Type[Any], handler: Any) -> None:
        """Register a request handler."""
        self._request_handlers[request_type] = handler

    def register_notification_handler(
        self, notification_type: Type[Any], handler: Any
    ) -> None:
        """Register a notification handler."""
        if notification_type not in self._notification_handlers:
            self._notification_handlers[notification_type] = []
        self._notification_handlers[notification_type].append(handler)

    async def send(self, request: IRequest[Any]) -> Any:
        """Send a request and return response."""
        handler = self._request_handlers.get(type(request))
        if not handler:
            raise ValueError(f"No handler registered for {type(request)}")
        return await handler.handle(request)

    async def publish(self, notification: INotification) -> None:
        """Publish a notification to all handlers."""
        handlers = self._notification_handlers.get(type(notification), [])
        for handler in handlers:
            await handler.handle(notification)
