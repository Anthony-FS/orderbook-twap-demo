"""Names of Redis keys, channels and RabbitMQ queues.

Several services read and write the same keys. Keeping the names in one module
means a typo becomes an import error instead of a silent bug where one service
writes `heartbeat:market_adapter` and another reads `heartbeat:market-adapter`.
"""

HEARTBEAT_PREFIX = "heartbeat:"
HEARTBEAT_TTL_SECONDS = 10

# Services that report a heartbeat. The backend health check looks these up.
WORKER_SERVICES = ("market-adapter", "twap-executor")


def heartbeat_key(service: str) -> str:
    return f"{HEARTBEAT_PREFIX}{service}"
