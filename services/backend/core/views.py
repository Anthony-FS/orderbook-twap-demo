"""Health check: one endpoint that reports on every part of the system.

It's the first thing to open when something looks wrong, and the frontend uses
it in step 1 to prove the whole chain works:
browser -> nginx -> Django -> Postgres / Redis -> worker heartbeats.
"""

import redis
from django.conf import settings
from django.db import connection
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.keys import WORKER_SERVICES, heartbeat_key


def _check_database() -> str:
    try:
        connection.ensure_connection()
        return "ok"
    except Exception:
        return "down"


def _check_redis_and_workers() -> dict[str, str]:
    results = {"redis": "down"}
    results.update({name: "unknown" for name in WORKER_SERVICES})
    try:
        # Short timeouts: a health check that hangs is worse than one that says "down".
        client = redis.Redis.from_url(
            settings.REDIS_URL, socket_connect_timeout=1, socket_timeout=1
        )
        client.ping()
        results["redis"] = "ok"
        for name in WORKER_SERVICES:
            results[name] = "ok" if client.exists(heartbeat_key(name)) else "down"
    except Exception:
        pass  # Redis down: worker status can't be known, stays "unknown".
    return results


class HealthView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def get(self, request):
        services = {"database": _check_database(), **_check_redis_and_workers()}
        all_ok = all(status == "ok" for status in services.values())
        return Response({"status": "ok" if all_ok else "degraded", "services": services})
