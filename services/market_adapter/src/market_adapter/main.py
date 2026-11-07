"""Market adapter entry point.

Step 1: only starts up, connects to Redis and writes a heartbeat.
Step 2 adds the exchange WebSocket client and the order book.
"""

import asyncio
import logging

from redis.asyncio import Redis

from common.config import load_config
from common.heartbeat import run_heartbeat
from common.log_setup import setup_logging

SERVICE = "market-adapter"
log = logging.getLogger(SERVICE)


async def main() -> None:
    config = load_config()
    setup_logging(SERVICE, config.log_level)
    redis = Redis.from_url(config.redis_url)
    log.info("starting, redis=%s", config.redis_url)
    await run_heartbeat(redis, SERVICE)


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
