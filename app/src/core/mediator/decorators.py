from typing import Any, Callable, Dict, Type, TypeVar

T = TypeVar('T')

registry: Dict[str, Dict[Type[Any], Any]] = {
    "request_handlers": {},
    "notification_handlers": {},
}

def request_handler(request_type: Type[Any]) -> Callable[[Type[T]], Type[T]]:
    """Decorator to register a request handler."""
    def decorator(cls: Type[T]) -> Type[T]:
        registry["request_handlers"][request_type] = cls()
        return cls
    return decorator

def notification_handler(notification_type: Type[Any]) -> Callable[[Type[T]], Type[T]]:
    """Decorator to register a notification handler."""
    def decorator(cls: Type[T]) -> Type[T]:
        registry["notification_handlers"].setdefault(notification_type, []).append(cls())
        return cls
    return decorator
