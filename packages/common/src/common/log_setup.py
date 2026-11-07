import logging


def setup_logging(service: str, level: str = "INFO") -> None:
    """One log format for every service, prefixed with the service name.

    In `docker compose logs` all services are interleaved, so the name in each
    line is what lets you follow one of them.
    """
    logging.basicConfig(
        level=level.upper(),
        format=f"%(asctime)s {service} %(levelname)s %(name)s: %(message)s",
    )
