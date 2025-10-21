"""Application configuration."""

import os
from typing import Literal, Union

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv not installed, environment variables should be set externally
    pass

EnvironmentType = Union[
    Literal["production"], Literal["development"], Literal["staging"]
]
ENVIRONMENT: EnvironmentType = os.getenv("ENVIRONMENT", "development")  # type: ignore
IS_DEVELOPMENT: bool = ENVIRONMENT == "development"
IS_STAGING: bool = ENVIRONMENT == "staging"
IS_PRODUCTION: bool = ENVIRONMENT == "production"

# API Configuration
API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))
API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"
