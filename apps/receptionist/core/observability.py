import time, uuid, logging
from typing import Callable
from fastapi import Request, APIRouter, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logger = logging.getLogger('receptionist')
logger.setLevel(logging.INFO)

REQS = Counter('receptionist_requests_total', 'Total requests', ['path','method','status'])
LATENCY = Histogram('receptionist_request_latency_seconds', 'Request latency', ['path','method'])

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        cid = request.headers.get('x-correlation-id', str(uuid.uuid4()))
        start = time.time()
        response = await call_next(request)
        dur = time.time() - start
        try:
            REQS.labels(request.url.path, request.method, str(response.status_code)).inc()
            LATENCY.labels(request.url.path, request.method).observe(dur)
        except Exception:
            pass
        response.headers['x-correlation-id'] = cid
        return response

metrics_router = APIRouter()

@metrics_router.get('/metrics')
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
