import random
from abc import ABC, abstractmethod
from asyncio import sleep
from typing import Any, Callable, Type, cast

from logger import logger
from pydantic import BaseModel, ValidationError

from src.core.mediator.abstractions import IRequest
from src.core.mediator.exceptions import ExceptionHandlerRegistry, ValidationException
from src.core.mediator.mediator import Mediator
from src.core.mediator.validation import validator_registry


class IPipelineBehavior(ABC):
    """
    Abstract base class for pipeline behaviors in the mediator pattern.

    Pipeline behaviors allow for cross-cutting concerns to be implemented in a
    request/response pipeline. Each behavior can perform logic before and/or after
    the next behavior in the pipeline is executed.

    This interface defines the contract that all pipeline behaviors must implement
    to participate in the request processing pipeline.

    Example:
        class LoggingBehavior(IPipelineBehavior):
                print(f"Processing request: {type(request).__name__}")
                response = await next_handler(request)
                print(f"Completed processing: {type(request).__name__}")
                return response
    """

    @abstractmethod
    async def handle(self, request: Any, next_handler: Callable[..., Any]) -> Any:
        """
        Handle a request and optionally call the next behavior in the pipeline.

        Args:
            request (Any): The request object to be processed.
            next_handler (Callable): The next behavior or handler in the pipeline.

        Returns:
            Any: The response from processing the request.
        """


class LoggingBehavior(IPipelineBehavior):
    """Pipeline behavior for logging requests."""

    async def handle(self, request: Any, next_handler: Callable[..., Any]) -> Any:
        logger.info(f"Handling request {type(request).__name__}")
        response = await next_handler()
        logger.info(f"Finished handling {type(request).__name__}")
        return response


class ValidationBehavior(IPipelineBehavior):
    """Pipeline behavior for validating requests."""

    async def handle(self, request: Any, next_handler: Callable[..., Any]) -> Any:
        print(f"[VALIDATION] Validating {type(request).__name__}")
        if not request.is_valid():
            raise ValueError("Request is not valid")
        return await next_handler()


class PydanticValidationBehavior(IPipelineBehavior):
    """Pipeline behavior for Pydantic model validation."""

    async def handle(self, request: Any, next_handler: Callable[..., Any]) -> Any:
        if isinstance(request, BaseModel):
            try:
                # Re-validate Pydantic model (in case it was constructed unsafely)
                request.__class__.model_validate(request.model_dump())
            except ValidationError as e:
                error_dict = {str(i): error for i, error in enumerate(e.errors())}
                logger.error(f"Validation error: {error_dict}")
                raise ValidationException(errors=error_dict) from e
        return await next_handler()


class MediatorWithPipeline(Mediator):
    """Mediator with pipeline behavior support."""

    def __init__(self):
        super().__init__()
        self._pipeline: list[IPipelineBehavior] = []

    def add_behavior(self, behavior: IPipelineBehavior) -> None:
        """Add a behavior to the pipeline."""
        self._pipeline.append(behavior)

    async def send(self, request: IRequest[Any]) -> Any:
        """Send a request through the pipeline."""
        handler = self._request_handlers.get(type(request))
        if not handler:
            raise ValueError(f"No handler registered for {type(request)}")

        async def invoke_handler():
            return await handler.handle(request)

        # Apply middleware stack
        pipeline = invoke_handler
        for behavior in reversed(self._pipeline):
            pipeline = self._wrap_behavior(behavior, request, pipeline)

        return await pipeline()

    def _wrap_behavior(
        self, behavior: IPipelineBehavior, request: Any, next_handler: Callable[[], Any]
    ) -> Callable[[], Any]:
        """Wrap a behavior in the pipeline."""
        return lambda: behavior.handle(request, next_handler)


class RetryBehavior(IPipelineBehavior):
    """Pipeline behavior for retrying failed requests."""

    def __init__(
        self,
        retries: int = 3,
        delay: float = 0.5,
        backoff_factor: float = 2.0,
        jitter: bool = True,
    ) -> None:
        self.retries = retries
        self.delay = delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

    async def handle(self, request: Any, next_handler: Callable[..., Any]) -> Any:
        current_delay = self.delay
        for attempt in range(1, self.retries + 1):
            try:
                return await next_handler()
            except RuntimeError as e:
                logger.warning(f"[Retry] Attempt {attempt} failed: {e}")
                if attempt == self.retries:
                    logger.error(
                        f"[Retry] Max retries reached for {type(request).__name__}"
                    )
                    raise  # re-raise after max retries
                sleep_time: float = current_delay
                if self.jitter:
                    sleep_time += random.uniform(0, 0.1)
                await sleep(sleep_time)
                current_delay *= self.backoff_factor


class ExceptionHandlingBehavior(IPipelineBehavior):
    """Pipeline behavior for handling exceptions."""

    def __init__(self, registry: ExceptionHandlerRegistry):
        self.registry = registry

    async def handle(self, request: Any, next_handler: Callable[..., Any]) -> Any:
        try:
            return await next_handler()
        except Exception as e:
            print(f"[ExceptionHandler] Caught exception: {e}")
            handler = self.registry.get_handler(e)
            if handler:
                return handler.handle(e, request)
            raise


def fallback_response(exception: Exception, request: Any) -> str:
    """Default fallback response for exception handling."""
    return f"Error handled for {type(request).__name__}: {str(exception)}"


class FluentValidationBehavior(IPipelineBehavior):
    """Pipeline behavior for fluent validation."""

    async def handle(self, request: Any, next_handler: Callable[..., Any]) -> Any:
        request_type = cast(Type[Any], type(request))
        validator = validator_registry.get(request_type)
        if validator:
            errors = validator.validate(request)
            if errors:
                error_dict = {str(i): error for i, error in enumerate(errors)}
                logger.error(f"Validation error: {error_dict}")
                raise ValidationException(errors=error_dict)
        return await next_handler()
