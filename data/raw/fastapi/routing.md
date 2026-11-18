# Routing in FastAPI

## 1. What Is Routing?

Routing is the process of directing an incoming HTTP request to the appropriate function in a web application.

In FastAPI, routing connects a URL path and an HTTP method to a Python function.

For example, when a client sends a GET request to:

```text
http://127.0.0.1:8000/users
```

FastAPI identifies the matching route and executes the associated Python function.

The function processes the request and returns a response.

### Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return {"message": "List of users"}
```

Here:

- `app` is the FastAPI application instance.
- `@app.get("/users")` registers a GET route.
- `get_users()` is the function executed when the matching request arrives.
- The returned dictionary is converted into a JSON response.

## 2. What Is a Path Operation?

In FastAPI, a path operation refers to the combination of an HTTP method and a URL path.

For example:

```python
@app.get("/users")
def get_users():
    return {"message": "Get users"}
```

The path operation consists of:

- HTTP method: GET
- URL path: `/users`
- Function: `get_users()`

FastAPI uses path operation decorators to register endpoints.

Common decorators include:

| Decorator | HTTP Method | Typical Purpose |
|---|---|---|
| `@app.get()` | GET | Retrieve information |
| `@app.post()` | POST | Create a resource |
| `@app.put()` | PUT | Replace or update a resource |
| `@app.patch()` | PATCH | Partially update a resource |
| `@app.delete()` | DELETE | Delete a resource |
| `@app.options()` | OPTIONS | Describe communication options |
| `@app.head()` | HEAD | Retrieve response headers |
| `@app.trace()` | TRACE | Diagnostic HTTP operation |

The most commonly used methods in application development are GET, POST, PUT, PATCH, and DELETE.

## 3. Creating a FastAPI Application

Before defining routes, create a FastAPI application instance.

```python
from fastapi import FastAPI

app = FastAPI()
```

The `FastAPI` class provides the functionality required to build an API application.

A basic application can be created in a file named `main.py`.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}
```

Run the application using:

```powershell
uv run uvicorn main:app --reload
```

Explanation:

- `main`: Python module or filename (`main.py`).
- `app`: FastAPI application instance inside the module.
- `--reload`: Automatically reloads the application when code changes during development.

Open the application at:

```text
http://127.0.0.1:8000/
```

Expected JSON response:

```json
{
    "message": "Welcome to FastAPI"
}
```

## 4. HTTP Methods in FastAPI

HTTP methods define the type of operation a client wants to perform.

### 4.1 GET

GET is used to retrieve information from a server.

Example:

```python
@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Mobile"}
    ]
```

Request:

```text
GET /products
```

Response:

```json
[
    {
        "id": 1,
        "name": "Laptop"
    },
    {
        "id": 2,
        "name": "Mobile"
    }
]
```

GET requests should not be used to perform operations that modify server-side resources.

### 4.2 POST

POST is commonly used to create a new resource.

Example:

```python
@app.post("/products")
def create_product():
    return {
        "message": "Product created successfully"
    }
```

Request:

```text
POST /products
```

In a real application, the client would generally send product information in the request body.

### 4.3 PUT

PUT is commonly used to replace an existing resource or create a resource at a known URI, depending on the API design.

Example:

```python
@app.put("/products/{product_id}")
def update_product(product_id: int):
    return {
        "message": "Product updated",
        "product_id": product_id
    }
```

### 4.4 PATCH

PATCH is commonly used to partially update an existing resource.

Example:

```python
@app.patch("/products/{product_id}")
def partially_update_product(product_id: int):
    return {
        "message": "Product partially updated",
        "product_id": product_id
    }
```

### 4.5 DELETE

DELETE is used to remove a resource.

Example:

```python
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {
        "message": "Product deleted",
        "product_id": product_id
    }
```

## 5. Multiple Routes in a FastAPI Application

A single FastAPI application can contain multiple routes.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Home page"}

@app.get("/users")
def get_users():
    return {"message": "User list"}

@app.get("/products")
def get_products():
    return {"message": "Product list"}

@app.get("/orders")
def get_orders():
    return {"message": "Order list"}
```

Each route is associated with its own function.

FastAPI identifies the matching route based on the incoming HTTP method and path.

## 6. Path Operation Functions

A path operation function is the Python function associated with a route.

Example:

```python
@app.get("/employees")
def get_employees():
    return {
        "employees": ["Amit", "Riya", "Rahul"]
    }
```

The function executes when a matching request is received.

Path operation functions can be:

- Synchronous functions using `def`.
- Asynchronous functions using `async def`.

### Synchronous Example

```python
@app.get("/sync")
def synchronous_endpoint():
    return {"message": "Synchronous endpoint"}
```

### Asynchronous Example

```python
@app.get("/async")
async def asynchronous_endpoint():
    return {"message": "Asynchronous endpoint"}
```

FastAPI supports both approaches.

For operations involving asynchronous libraries, `async def` allows the application to use asynchronous I/O.

For ordinary blocking I/O libraries, using `def` can allow FastAPI to run the function in a thread pool rather than blocking the event loop.

Choosing between `def` and `async def` depends on the libraries and operations used inside the function.

## 7. Route Order and Path Matching

Route order matters when multiple routes could match similar URL patterns.

Consider:

```python
@app.get("/users/me")
def get_current_user():
    return {"username": "current_user"}

@app.get("/users/{username}")
def get_user(username: str):
    return {"username": username}
```

The static route `/users/me` should be declared before the dynamic route `/users/{username}`.

Otherwise, the dynamic route could match the word `me` as a username.

### Correct Ordering

```python
@app.get("/users/me")
def get_current_user():
    return {"username": "current_user"}

@app.get("/users/{username}")
def get_user(username: str):
    return {"username": username}
```

This is an important consideration when designing applications with both fixed and parameterized routes.

## 8. APIRouter

As an application grows, defining every endpoint in a single Python file becomes difficult to maintain.

FastAPI provides `APIRouter` to organize related path operations into separate modules.

An `APIRouter` can be thought of as a smaller routing unit that can be included in the main FastAPI application.

### Example Project Structure

```text
app/
│
├── main.py
│
├── routers/
│   ├── __init__.py
│   ├── users.py
│   ├── products.py
│   └── orders.py
│
└── schemas/
    └── __init__.py
```

### Step 1: Create a User Router

File: `app/routers/users.py`

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return {"message": "User list"}

@router.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }
```

### Step 2: Create the Main Application

File: `app/main.py`

```python
from fastapi import FastAPI
from app.routers import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome"}
```

`include_router()` registers the routes defined in the user router with the main FastAPI application.

This approach helps organize large applications into manageable modules.

## 9. APIRouter Prefix

A prefix allows a common path segment to be defined once for multiple routes.

Instead of writing `/users` in every route, define the prefix in `APIRouter`.

Example:

File: `app/routers/users.py`

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
def get_users():
    return {"message": "User list"}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

The resulting paths are:

```text
GET /users/
GET /users/{user_id}
```

The prefix should not end with a trailing slash.

## 10. Tags in FastAPI

Tags help organize API endpoints in the automatically generated API documentation.

Example:

```python
@app.get("/users", tags=["Users"])
def get_users():
    return {"message": "Users"}

@app.get("/products", tags=["Products"])
def get_products():
    return {"message": "Products"}
```

When the application is opened at `/docs`, endpoints are grouped according to their tags.

Tags make API documentation easier to navigate, particularly in large applications.

## 11. HTTP Status Codes

HTTP status codes indicate the result of an HTTP request.

Some commonly used status codes include:

| Status Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 202 | Accepted |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Content |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Setting a Status Code in FastAPI

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED
)
def create_product():
    return {
        "message": "Product created successfully"
    }
```

Here, `201 Created` indicates that the resource was successfully created.

Using named constants from `fastapi.status` makes the code more readable.

## 12. Path Operation Configuration

FastAPI allows additional information to be defined in path operation decorators.

Example:

```python
@app.get(
    "/products",
    tags=["Products"],
    summary="Retrieve products",
    description="Retrieve the available products.",
    response_description="List of products",
    deprecated=False
)
def get_products():
    return []
```

Important configuration parameters include:

| Parameter | Purpose |
|---|---|
| `tags` | Groups endpoints in API documentation |
| `summary` | Short description of the endpoint |
| `description` | Detailed endpoint description |
| `response_description` | Describes the response |
| `status_code` | Defines the default response status code |
| `deprecated` | Marks an endpoint as deprecated |
| `name` | Assigns a name to the path operation |
| `operation_id` | Sets the OpenAPI operation ID |

These settings improve the quality of automatically generated API documentation.

## 13. Automatic API Documentation

One of FastAPI's important features is automatic API documentation.

FastAPI generates an OpenAPI schema based on the application routes, parameters, request bodies, and response definitions.

Two commonly used documentation interfaces are available by default.

### 13.1 Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides an interactive interface where developers can:

- View available endpoints.
- Inspect HTTP methods.
- Review request parameters.
- Execute API requests.
- Inspect responses.
- Review validation errors.

### 13.2 ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

ReDoc provides another interface for browsing the generated API documentation.

### 13.3 OpenAPI Schema

The OpenAPI schema is generally available at:

```text
http://127.0.0.1:8000/openapi.json
```

It provides a machine-readable description of the API.

This schema can be used by documentation tools, API clients, and other development systems.

## 14. API Versioning Through Routing

As an API evolves, new versions may introduce changes to endpoints or response structures.

Versioning helps maintain compatibility with existing clients.

A common approach is URL-based versioning.

Example:

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["API V1"]
)

v2_router = APIRouter(
    prefix="/api/v2",
    tags=["API V2"]
)

@v1_router.get("/users")
def get_users_v1():
    return {
        "version": "v1",
        "users": ["Amit", "Riya"]
    }

@v2_router.get("/users")
def get_users_v2():
    return {
        "version": "v2",
        "users": [
            {"id": 1, "name": "Amit"},
            {"id": 2, "name": "Riya"}
        ]
    }

app.include_router(v1_router)
app.include_router(v2_router)
```

The resulting endpoints are:

```text
GET /api/v1/users
GET /api/v2/users
```

Versioning allows different API versions to coexist while clients migrate gradually.

## 15. Routing Best Practices

1. Use meaningful and consistent endpoint names.
2. Follow REST conventions where appropriate.
3. Use the correct HTTP methods.
4. Organize large applications using `APIRouter`.
5. Use prefixes to avoid repeated path segments.
6. Group related endpoints using tags.
7. Declare static routes before conflicting dynamic routes.
8. Use appropriate HTTP status codes.
9. Document endpoints using summaries and descriptions.
10. Use API versioning when backward compatibility is required.
11. Keep business logic separate from routing functions.
12. Avoid placing all endpoints in one large Python file.
13. Use meaningful response models as the application grows.
14. Test routes with valid and invalid requests.

## 16. Summary

Routing is the foundation of a FastAPI application.

It connects incoming HTTP requests to Python functions through path operations.

Important concepts include:

- FastAPI application instance.
- Path operations.
- HTTP methods.
- Synchronous and asynchronous endpoints.
- Route order.
- APIRouter.
- Router prefixes.
- Tags.
- HTTP status codes.
- Path operation configuration.
- Automatic API documentation.
- API versioning.

For larger applications, `APIRouter` helps organize endpoints into separate modules and makes the application easier to maintain.

## References

- FastAPI First Steps: https://fastapi.tiangolo.com/tutorial/first-steps/
- FastAPI Bigger Applications: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- FastAPI Path Operation Configuration: https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
- FastAPI Metadata and Docs URLs: https://fastapi.tiangolo.com/tutorial/metadata/
- FastAPI Status Codes: https://fastapi.tiangolo.com/tutorial/response-status-code/
- FastAPI Documentation: https://fastapi.tiangolo.com/