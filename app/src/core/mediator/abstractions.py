from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Generic type variable for request types.
T = TypeVar('T')

# Generic type variable for response types.
R = TypeVar('R')

class IRequest(Generic[R], ABC):
    """
    Abstract base class for request objects in the mediator pattern.

    This interface defines the contract for request objects that can be processed
    by a mediator. Each request is associated with a specific response type through
    the generic type parameter TResponse.

    Type Parameters:
        R: The type of response that this request will produce when processed.

    Usage:
        Inherit from this class to create specific request types:
        
        class GetUserRequest(IRequest[User]):
            def __init__(self, user_id: int):
                self.user_id = user_id
    """


class IRequestHandler(Generic[T, R], ABC):
    """
    Abstract base class for handling requests in a mediator pattern.

    This interface defines the contract for request handlers that process a specific
    type of request and return a corresponding response. It uses generics to provide
    type safety for both the request and response types.

    Type Parameters:
        T: The type of request this handler can process
        R: The type of response this handler returns

    Methods:
        handle(request: T) -> R:
            Processes the given request and returns an appropriate response.
            Must be implemented by concrete handler classes.

    Example:
        class GetUserHandler(IRequestHandler[GetUserRequest, User]):
            def handle(self, request: GetUserRequest) -> User:
                # Implementation logic here
                return user
    """
    @abstractmethod
    async def handle(self, request: T) -> R:
        """
        Handle a request and return a response.

        Args:
            request (T): The request object to be processed.

        Returns:
            R: The response object resulting from processing the request.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """


class INotification(ABC):
    """
    Abstract base class for notifications in the mediator pattern.

    This interface defines the contract for notification objects that can be
    sent through the mediator to notify handlers without expecting a response.
    Notifications are typically used for fire-and-forget operations, logging,
    event broadcasting, or triggering side effects.

    Classes implementing this interface should contain the data and context
    needed for the specific notification type.

    Example:
        class UserRegisteredNotification(INotification):
            def __init__(self, user_id: str, email: str):
                self.user_id = user_id
                self.email = email
    """


class INotificationHandler(Generic[T], ABC):
    """
    Abstract base class for notification handlers in the mediator pattern.

    This interface defines the contract for handlers that process notifications
    of a specific type. Notification handlers are used to implement the observer
    pattern within the mediator, allowing for decoupled handling of domain events
    or other notifications.

    Type Parameters:
        T: The type of notification that this handler can process.

    Methods:
        handle: Processes the given notification of type T.

    Example:
        class UserCreatedNotificationHandler(INotificationHandler[UserCreatedNotification]):
            def handle(self, notification: UserCreatedNotification) -> None:
                # Handle the user created notification
    """
    @abstractmethod
    async def handle(self, notification: T) -> None:
        """
        Handle a notification request.

        This method processes a notification of type T. Notifications are 
        typically one-way messages that don't return a response, used for triggering
        side effects or notifying multiple handlers about an event.

        Args:
            notification (T): The notification object containing the data
                                   and context needed for processing.

        Returns:
            None: This method doesn't return any value as notifications are
                  fire-and-forget operations.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
