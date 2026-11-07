"""Environment-based configuration shared by the worker services.

Every setting comes from an environment variable (12-factor style), with a
default that works for local development. Docker Compose sets the real values.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    redis_url: str
    rabbitmq_url: str
    log_level: str


def load_config() -> Config:
    return Config(
        redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        rabbitmq_url=os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
