import logging
import os
import structlog
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")
doctor_id_var: ContextVar[str] = ContextVar("doctor_id", default="")

ENV = os.getenv("ENV", "production")

def configure_logging() -> None:
    log_level = logging.DEBUG if ENV == "dev" else logging.INFO

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if ENV == "dev":
        renderer = structlog.dev.ConsoleRenderer(colors=True)
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=shared_processors + [renderer],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(format="%(message)s", level=log_level)

def get_logger(name: str = __name__):
    return structlog.get_logger(name)
