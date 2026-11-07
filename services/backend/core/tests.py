from django.test import override_settings
from rest_framework.test import APIClient


@override_settings(REDIS_URL="redis://127.0.0.1:1/0")  # nothing listens on port 1
def test_health_reports_each_service(db):
    response = APIClient().get("/api/health/")

    assert response.status_code == 200
    body = response.json()
    assert body["services"]["database"] == "ok"
    # Redis is unreachable, so the system is degraded and workers are unknown.
    assert body["services"]["redis"] == "down"
    assert body["services"]["market-adapter"] == "unknown"
    assert body["status"] == "degraded"
