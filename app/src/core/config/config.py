"""Application configuration."""

import os
from typing import Literal, Union

EnvironmentType = Union[
    Literal["production"], Literal["development"], Literal["staging"]
]
ENVIRONMENT: EnvironmentType = os.getenv("ENVIRONMENT", "development")  # type: ignore
IS_DEVELOPMENT: bool = ENVIRONMENT == "development"
IS_STAGING: bool = ENVIRONMENT == "staging"
IS_PRODUCTION: bool = ENVIRONMENT == "production"
