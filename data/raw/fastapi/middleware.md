# Middleware in FastAPI

## 1. Introduction

Middleware is a component that processes HTTP requests and responses as they pass through an application.

It sits between the client and the API endpoints.

Middleware can execute code:

- Before a request reaches an API endpoint.
- After an endpoint generates a response.
- Before the response is returned to the client.

Middleware is useful for implementing functionality that should apply to multiple endpoints.

Common use cases include:

- Request logging.
- Execution-time measurement.
- CORS configuration.
- Authentication-related request processing.
- Security headers.
- Response compression.
- HTTPS redirection.
- Request and response monitoring.

## 2. How Middleware Works

Middleware wraps the application and intercepts incoming requests and outgoing responses.

The basic execution flow is:

```text
       Client
          |
          | HTTP Request
          v
      Middleware
          |
          | Forward Request
          v
      FastAPI Router
          |
          v
      API Endpoint
          |
          | Generate Response
          v
      Middleware
          |
          | Process Response
          v
        Client
```

The middleware can inspect or modify the request before passing it to the endpoint.

It can also inspect or modify the response before returning it to the client.

## 3. Creating Custom Middleware

FastAPI provides the `@app.middleware("http")` decorator to create custom HTTP middleware.

Example:

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def custom_middleware(request: Request, call_next):

    print("Before request processing")

    response = await call_next(request)

    print("After response generation")

    return response

@app.get("/")
async def home():
    return {"message": "Hello World"}
```

Explanation:

- `request` contains information about the incoming HTTP request.
- `call_next` passes the request to the remaining application.
- `await call_next(request)` executes the downstream application and obtains its response.
- The middleware can inspect or modify the response.
- `return response` sends the response back through the middleware stack.

The code before `call_next()` runs before the endpoint.

The code after `call_next()` runs after the downstream application generates its response.

## 4. Measuring Request Processing Time

One common use of middleware is measuring how long an API request takes to process.

Python provides `time.perf_counter()` for measuring elapsed time.

Example:

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next
):

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = str(process_time)

    return response

@app.get("/")
async def home():
    return {"message": "Hello World"}
```

Explanation:

1. Record the start time.
2. Pass the request to the application.
3. Wait for the response.
4. Calculate elapsed time.
5. Add the processing time to the response header.

Example response header:

```text
X-Process-Time: 0.0025
```

The value represents elapsed time in seconds for the measured application processing path.

This is useful for basic API performance monitoring.

**Important:** This measurement does not necessarily represent the complete time experienced by the client. Network latency and other infrastructure delays are not included.

## 5. Adding Custom Response Headers

Middleware can add custom headers to API responses.

Example:

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_custom_header(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-Application"] = "FastAPI"

    return response

@app.get("/")
async def home():
    return {"message": "Welcome"}
```

The response contains:

```text
X-Application: FastAPI
```

Custom headers can be useful for:

- Request tracing.
- Application identification.
- Performance monitoring.
- Debugging.
- Exposing selected metadata to clients.

If a browser frontend needs to read a custom response header, configure that header in CORS using `expose_headers`.

## 6. Logging Requests Using Middleware

Middleware can be used to log incoming requests and their responses.

Example:

```python
import logging

from fastapi import FastAPI, Request

app = FastAPI()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(
        "Request: %s %s",
        request.method,
        request.url.path
    )

    response = await call_next(request)

    logger.info(
        "Response status: %s",
        response.status_code
    )

    return response

@app.get("/")
async def home():
    return {"message": "Hello World"}
```

This middleware logs:

- HTTP method.
- Requested URL path.
- Response status code.

In production, use structured logging and avoid recording passwords, access tokens, API keys, or sensitive request bodies.

## 7. Understanding Middleware Execution Order

FastAPI allows multiple middleware components to be registered.

They form a wrapping stack around the application.

The last middleware added becomes the outermost middleware.

Example:

```python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

Request execution:

```text
MiddlewareB
     |
     v
MiddlewareA
     |
     v
API Endpoint
```

Response execution:

```text
API Endpoint
     |
     v
MiddlewareA
     |
     v
MiddlewareB
```

Therefore:

- The outermost middleware runs first on the request path.
- The outermost middleware runs last on the response path.

Understanding this order is important when multiple middleware components depend on one another.

## 8. Using app.add_middleware()

FastAPI also supports registering middleware using `app.add_middleware()`.

This is commonly used for built-in and third-party middleware classes.

Example:

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)
```

Here:

- `GZipMiddleware` is the middleware class.
- `minimum_size=1000` specifies the minimum response size in bytes before compression is applied.

`app.add_middleware()` is useful when middleware is implemented as a class rather than a function decorated with `@app.middleware("http")`.

## 9. CORS (Cross-Origin Resource Sharing)

CORS stands for Cross-Origin Resource Sharing.

It is a browser security mechanism that controls whether a web application from one origin can access resources from another origin.

An origin consists of:

- Scheme (HTTP or HTTPS).
- Hostname.
- Port.

For example:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
```

These are different origins because their ports are different.

A browser may block frontend JavaScript from reading the backend response unless the backend allows the frontend origin through CORS.

CORS is enforced by browsers. It is not a replacement for API authentication or authorization.

## 10. Configuring CORS in FastAPI

FastAPI provides `CORSMiddleware`.

Example:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)

@app.get("/")
async def home():
    return {"message": "Hello World"}
```

Explanation:

| Parameter | Purpose |
|---|---|
| `allow_origins` | Specifies permitted frontend origins |
| `allow_credentials` | Allows credentials such as cookies |
| `allow_methods` | Specifies permitted HTTP methods |
| `allow_headers` | Specifies permitted request headers |
| `expose_headers` | Specifies response headers browser JavaScript can read |
| `max_age` | Controls how long browsers can cache preflight responses |

For production applications, configure only the origins, methods, and headers that are actually required.

## 11. CORS Wildcards

CORS supports wildcard configuration.

Example:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

This broadly allows origins, methods, and headers for requests without credential support.

However, when `allow_credentials=True`, configure explicit origins, methods, and headers rather than relying on wildcards.

A restrictive CORS configuration is generally preferable for production applications.

CORS does not prevent non-browser clients from sending requests to your API. It controls browser access to cross-origin responses.

## 12. Understanding CORS Preflight Requests

Before certain cross-origin requests, browsers send a preflight request using the HTTP `OPTIONS` method.

The preflight request asks the server whether the actual request is allowed.

For example, a frontend may send:

```text
OPTIONS /items/
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type, authorization
```

The server responds with CORS headers indicating whether the request is permitted.

If allowed, the browser proceeds with the actual request.

`CORSMiddleware` handles these preflight requests automatically.

This is particularly important when a frontend sends JSON data, custom headers, or authorization credentials to a backend hosted on a different origin.

## 13. GZipMiddleware

GZipMiddleware compresses eligible HTTP responses to reduce the amount of data transferred over the network.

Example:

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    compresslevel=5
)

@app.get("/data/")
async def get_data():
    return {
        "message": "This is an example response"
    }
```

Important parameters:

| Parameter | Purpose |
|---|---|
| `minimum_size` | Minimum response size in bytes for compression |
| `compresslevel` | Compression level from 1 to 9 |

Higher compression levels generally use more CPU time but can produce smaller compressed output.

GZip compression is useful for large JSON responses and other compressible content.

## 14. HTTPSRedirectMiddleware

HTTPSRedirectMiddleware redirects insecure HTTP requests to HTTPS.

Example:

```python
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def home():
    return {"message": "Secure connection"}
```

If a client accesses the application through HTTP, the middleware redirects the request to HTTPS.

HTTPS protects data transmitted between clients and servers.

In production, HTTPS must also be configured correctly at the deployment layer, such as a reverse proxy or hosting platform.

When an application runs behind a reverse proxy, configure trusted proxy headers correctly so the application can determine the original request scheme.

## 15. TrustedHostMiddleware

TrustedHostMiddleware protects an application against certain HTTP Host Header attacks.

It validates the hostname supplied in the incoming request.

Example:

```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "example.com",
        "*.example.com"
    ]
)

@app.get("/")
async def home():
    return {"message": "Welcome"}
```

Explanation:

- `allowed_hosts` specifies the permitted hostnames.
- Wildcard subdomains such as `*.example.com` are supported.
- Requests with invalid hostnames receive an HTTP 400 response.

In production, replace the example hostnames with the actual domains used by your application.

## 16. Middleware vs Dependency Injection

Middleware and dependency injection both allow developers to reuse application logic, but they serve different purposes.

| Middleware | Dependency Injection |
|---|---|
| Operates around the request-response cycle | Provides required resources or logic to endpoints |
| Can apply to many or all requests | Can be applied to selected endpoints, routers, or the application |
| Commonly used for logging, timing, CORS, compression | Commonly used for database sessions, authentication, and shared services |
| Works before and after endpoint processing | Resolves dependencies before the endpoint executes |

Example middleware use:

```python
@app.middleware("http")
async def measure_time(request, call_next):
    response = await call_next(request)
    return response
```

Example dependency use:

```python
def get_current_user():
    return {"username": "john"}

@app.get("/profile/")
async def profile(
    user: Annotated[dict, Depends(get_current_user)]
):
    return user
```

Use middleware for application-wide request and response processing.

Use dependencies when an endpoint needs a particular resource, service, or authorization check.

## 17. Advanced ASGI Middleware

FastAPI is built on Starlette and follows the ASGI (Asynchronous Server Gateway Interface) specification.

ASGI defines how asynchronous Python web applications communicate with web servers.

Because FastAPI follows ASGI, it can use compatible third-party ASGI middleware.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

# Example:
# app.add_middleware(
#     SomeASGIMiddleware,
#     some_configuration="value"
# )
```

Third-party middleware must be compatible with the ASGI interface.

FastAPI recommends using `app.add_middleware()` to register middleware classes.

## 18. Middleware and Exception Handling

Middleware operates around request processing, but it should not be treated as a replacement for FastAPI's exception-handling system.

FastAPI provides exception handlers for handling application errors.

For example:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):

    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    return {"user_id": user_id}
```

Use:

- Middleware for cross-cutting request and response behavior.
- Exception handlers for converting application exceptions into appropriate HTTP responses.

The middleware stack and exception-handling order should be considered when designing application-wide error logging and monitoring.

## 19. Relevance to AI and RAG Applications

Middleware is useful when deploying a RAG application through FastAPI.

Consider a RAG backend connected to a frontend application.

The frontend sends a question, and the backend retrieves relevant documents and generates an answer.

Middleware can support:

- Measuring API response time.
- Logging incoming requests.
- Adding request-tracing headers.
- Configuring CORS for the frontend.
- Compressing large JSON responses.
- Enforcing HTTPS.
- Applying trusted-host restrictions.

Example:

```python
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"]
)

@app.middleware("http")
async def measure_request_time(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = str(elapsed_time)

    return response
```

In a real RAG deployment, this middleware could help monitor the API request lifecycle.

However, API processing time and RAG pipeline execution time are not necessarily the same. For detailed monitoring, measure retrieval time, LLM generation time, and total request time separately.

## 20. Best Practices

1. Use middleware for functionality shared across multiple requests.
2. Keep custom middleware lightweight.
3. Avoid blocking operations inside asynchronous middleware.
4. Use `time.perf_counter()` for elapsed-time measurements.
5. Configure CORS with explicit trusted frontend origins.
6. Do not treat CORS as an authentication mechanism.
7. Avoid logging passwords, API keys, access tokens, or sensitive request data.
8. Use HTTPS in production.
9. Configure trusted hosts when appropriate.
10. Understand middleware execution order when registering multiple middleware components.
11. Use dependencies for endpoint-specific resources and services.
12. Monitor middleware overhead because it affects requests passing through the application.

## 21. Official References

- FastAPI — Middleware: https://fastapi.tiangolo.com/tutorial/middleware/
- FastAPI — CORS: https://fastapi.tiangolo.com/tutorial/cors/
- FastAPI — Advanced Middleware: https://fastapi.tiangolo.com/advanced/middleware/
- FastAPI — Middleware Reference: https://fastapi.tiangolo.com/reference/middleware/
- FastAPI — Response Headers: https://fastapi.tiangolo.com/advanced/response-headers/
- Starlette — Middleware: https://www.starlette.io/middleware/
- MDN — Cross-Origin Resource Sharing (CORS): https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS