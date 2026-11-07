"""TWAP executor entry point.

Step 1: connects to RabbitMQ and declares the order queue, then heartbeats.
Step 6 adds consuming orders, slicing them and simulating fills.
"""

import asyncio
import logging

import aio_pika
from redis.asyncio import Redis

from common.config import load_config
from common.heartbeat import run_heartbeat
from common.log_setup import setup_logging

SERVICE = "twap-executor"
ORDER_QUEUE = "twap.orders"
log = logging.getLogger(SERVICE)


async def main() -> None:
    config = load_config()
    setup_logging(SERVICE, config.log_level)

    # connect_robust reconnects to RabbitMQ automatically and re-declares
    # queues and consumers afterwards. We still rely on it in step 6.
    connection = await aio_pika.connect_robust(config.rabbitmq_url)
    channel = await connection.channel()
    # durable=True: the queue survives a RabbitMQ restart, so orders already
    # submitted aren't lost if the broker restarts.
    await channel.declare_queue(ORDER_QUEUE, durable=True)
    log.info("connected to rabbitmq, queue %r declared", ORDER_QUEUE)

    redis = Redis.from_url(config.redis_url)
    await run_heartbeat(redis, SERVICE)


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
