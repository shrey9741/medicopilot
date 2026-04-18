import time
import uuid
import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from logging_config import request_id_var, doctor_id_var

logger = structlog.get_logger("request")

class RequestTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())[:8]
        request_id_var.set(req_id)

        doctor = "anonymous"
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                from auth.jwt_handler import verify_token
                payload = verify_token(auth_header[7:])
                if payload:
                    doctor = payload.get("sub", "unknown")
            except Exception:
                pass
        doctor_id_var.set(doctor)

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=req_id,
            doctor=doctor,
            method=request.method,
            path=request.url.path,
        )

        start = time.perf_counter()
        logger.info("request.start")
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 1)
        logger.info("request.end", status=response.status_code, duration_ms=duration_ms)

        response.headers["X-Request-ID"] = req_id
        return response
