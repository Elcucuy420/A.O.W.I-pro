# Add to FastAPI

To enable the embed widget, privacy middleware, and metrics endpoint in your FastAPI application, update your `server/fastapi_app.py` file as follows.

```
from fastapi.staticfiles import StaticFiles
from server.metrics import router as metrics_router
from server.middleware.privacy import PrivacyMiddleware

app = FastAPI()

# Mount static files so the chat widget can be served
app.mount("/static", StaticFiles(directory="server/static"), name="static")

# Include the metrics endpoint for health checks
app.include_router(metrics_router)

# Add the privacy middleware to redact sensitive information
app.add_middleware(PrivacyMiddleware)
```

After making these changes, restart your server. The widget script will be served at `/static/embed.js` and the `/metrics` endpoint will return a simple health check JSON.
