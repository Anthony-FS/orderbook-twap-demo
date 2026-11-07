"""A tiny liveness signal for background workers.

Workers have no HTTP endpoint, so how does anyone know they're alive? Each one
writes a Redis key every few seconds with a short expiry (TTL). If the worker
dies or hangs, it stops refreshing the key, the key expires, and the backend's
health check reports the worker as down. No extra infrastructure needed.
"""

import asyncio
import logging
import time

from redis.asyncio import Redis

from common.keys import HEARTBEAT_TTL_SECONDS, heartbeat_key

log = logging.getLogger(__name__)


async def run_heartbeat(redis: Redis, service: str, interval: float = 3.0) -> None:
    key = heartbeat_key(service)
    while True:
        try:
            await redis.set(key, str(time.time()), ex=HEARTBEAT_TTL_SECONDS)
        except Exception as exc:  # Redis briefly down: log and keep trying.
            log.warning("heartbeat write failed: %s", exc)
        await asyncio.sleep(interval)
