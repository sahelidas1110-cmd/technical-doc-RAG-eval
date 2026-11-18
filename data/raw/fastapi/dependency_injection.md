# Dependency Injection in FastAPI

## 1. Introduction

Dependency Injection (DI) is a programming technique in which an object or function receives the resources or services it needs from an external system rather than creating them directly.

FastAPI provides a built-in Dependency Injection system using `Depends()`.

It allows developers to reuse common functionality across multiple API endpoints.

Common use cases include:

- Database connections.
- Authentication and authorization.
- Shared query parameters.
- Configuration management.
- Logging.
- API rate limiting.
- Accessing external services.
- Reusing AI and RAG pipeline components.

For example, suppose multiple API endpoints need to verify whether a user is authenticated.

Instead of implementing authentication separately in every endpoint, we can create one dependency and reuse it.

FastAPI automatically executes the dependency and provides its result to the endpoint.

## 2. Understanding Depends()

FastAPI provides the `Depends()` function to declare dependencies.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_message():
    return "Hello from dependency"

@app.get("/")
async def home(
    message: Annotated[str, Depends(get_message)]
):
    return {"message": message}
```

Explanation:

- `get_message()` is the dependency function.
- `Depends(get_message)` declares that the endpoint depends on this function.
- FastAPI calls the dependency when processing the request.
- The returned value is injected into the `message` parameter.

Response:

```json
{
    "message": "Hello from dependency"
}
```

**Important:** Pass the function itself to `Depends()`, without calling it.

Correct:

```python
Depends(get_message)
```

Incorrect:

```python
Depends(get_message())
```

FastAPI manages the execution of the dependency.

## 3. Creating a Reusable Dependency

Suppose multiple endpoints need common pagination parameters.

Without dependency injection, we might repeat the same parameters in every endpoint.

Using a dependency, we can define the common functionality once.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 10
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit
    }

@app.get("/items/")
async def read_items(
    commons: Annotated[dict, Depends(common_parameters)]
):
    return commons

@app.get("/users/")
async def read_users(
    commons: Annotated[dict, Depends(common_parameters)]
):
    return commons
```

Both endpoints reuse the same dependency.

Example request:

```text
/items/?q=laptop&skip=0&limit=5
```

Response:

```json
{
    "q": "laptop",
    "skip": 0,
    "limit": 5
}
```

The dependency also supports automatic parameter extraction and validation.

## 4. Using Annotated with Depends()

FastAPI recommends using `Annotated` to declare dependencies when possible.

Example:

```python
from typing import Annotated
from fastapi import Depends

def get_current_user():
    return {"username": "john"}

CurrentUser = Annotated[dict, Depends(get_current_user)]
```

Now the reusable dependency can be used in multiple endpoints.

```python
@app.get("/profile/")
async def get_profile(user: CurrentUser):
    return user

@app.get("/dashboard/")
async def get_dashboard(user: CurrentUser):
    return {
        "message": "Welcome to dashboard",
        "user": user
    }
```

Benefits:

- Reduces repeated dependency declarations.
- Improves code readability.
- Preserves type information.
- Provides better editor support.
- Makes large applications easier to maintain.

The alternative syntax is:

```python
@app.get("/profile/")
async def get_profile(
    user: dict = Depends(get_current_user)
):
    return user
```

Both styles are supported, but `Annotated` is generally preferred.

## 5. How Dependency Injection Works

When an API request arrives, FastAPI:

1. Identifies the endpoint that should handle the request.
2. Examines the endpoint's declared dependencies.
3. Executes the required dependency functions.
4. Resolves any sub-dependencies.
5. Passes the dependency results to the endpoint.
6. Executes the endpoint and produces the response.

Conceptual flow:

```text
Client Request
      |
      v
FastAPI Router
      |
      v
Resolve Dependencies
      |
      v
Execute Dependency Functions
      |
      v
Inject Dependency Results
      |
      v
Execute API Endpoint
      |
      v
Return Response
```

This allows developers to separate shared application logic from endpoint-specific logic.

## 6. Synchronous and Asynchronous Dependencies

FastAPI supports both synchronous and asynchronous dependency functions.

### Synchronous Dependency

```python
def get_user():
    return {"username": "john"}

@app.get("/users/")
async def read_user(
    user: Annotated[dict, Depends(get_user)]
):
    return user
```

### Asynchronous Dependency

```python
async def get_user():
    return {"username": "john"}

@app.get("/users/")
async def read_user(
    user: Annotated[dict, Depends(get_user)]
):
    return user
```

FastAPI handles both types.

In general:

- Use `def` for synchronous operations.
- Use `async def` when working with asynchronous libraries and operations.
- Avoid performing blocking operations directly inside asynchronous functions.

For example, an asynchronous database client can be used inside an asynchronous dependency.

## 7. Sub-Dependencies

A dependency can itself depend on another dependency.

This is called a sub-dependency.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_query():
    return "machine learning"

def get_search_parameters(
    query: Annotated[str, Depends(get_query)]
):
    return {
        "query": query,
        "category": "technology"
    }

@app.get("/search/")
async def search(
    params: Annotated[dict, Depends(get_search_parameters)]
):
    return params
```

Dependency relationship:

```text
get_query()
     |
     v
get_search_parameters()
     |
     v
search() endpoint
```

FastAPI automatically resolves the dependency hierarchy.

This is useful for building more complex applications where one dependency requires another.

## 8. Dependency Caching

FastAPI normally caches dependency results within a single request.

If the same dependency is required multiple times during the same request, FastAPI generally executes it once and reuses its result.

Example:

```python
def get_current_user():
    print("Executing get_current_user")

    return {"username": "john"}

def get_user_permissions(
    user: Annotated[dict, Depends(get_current_user)]
):
    return ["read", "write"]

@app.get("/dashboard/")
async def dashboard(
    user: Annotated[dict, Depends(get_current_user)],
    permissions: Annotated[list, Depends(get_user_permissions)]
):
    return {
        "user": user,
        "permissions": permissions
    }
```

Both the endpoint and `get_user_permissions()` depend on `get_current_user()`.

By default, FastAPI reuses the dependency result within that request rather than executing the same dependency again.

### Disabling Dependency Caching

Use `use_cache=False` when you explicitly need a dependency to execute again.

```python
@app.get("/fresh-data/")
async def get_fresh_data(
    value: Annotated[str, Depends(get_value, use_cache=False)]
):
    return {"value": value}
```

This disables reuse of the cached result for that dependency declaration.

Caching is scoped to an individual request, not shared globally across all requests.

## 9. Dependencies with yield

Some dependencies need to perform cleanup after the endpoint finishes.

For example:

- Opening and closing database sessions.
- Acquiring and releasing resources.
- Opening and closing temporary resources.

FastAPI supports this using `yield`.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_resource():
    print("Opening resource")

    resource = {"connection": "active"}

    try:
        yield resource

    finally:
        print("Closing resource")

@app.get("/data/")
async def read_data(
    resource: Annotated[dict, Depends(get_resource)]
):
    return resource
```

Execution flow:

```text
Request Arrives
      |
      v
Execute code before yield
      |
      v
Provide resource to endpoint
      |
      v
Execute endpoint
      |
      v
Execute cleanup code
```

The `finally` block ensures cleanup is attempted even if an exception occurs during the endpoint's execution.

A dependency using `yield` should use it once.

## 10. Database Dependency Example

A common use case for `yield` is managing database sessions.

The following is a conceptual example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

class DatabaseSession:
    def close(self):
        print("Database session closed")

def create_database_session():
    return DatabaseSession()

def get_db():
    db = create_database_session()

    try:
        yield db

    finally:
        db.close()

@app.get("/users/")
async def get_users(
    db: Annotated[DatabaseSession, Depends(get_db)]
):
    return {"message": "Database operation completed"}
```

Here:

- `get_db()` creates a database session.
- The session is provided to the endpoint.
- The endpoint uses the session.
- The cleanup code closes the session.

In a real application, the database session would be created using a database library such as SQLAlchemy.

## 11. Dependencies at the Endpoint Decorator Level

Sometimes a dependency needs to execute, but the endpoint does not need its returned value.

FastAPI allows dependencies to be declared directly in the path operation decorator.

Example:

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def verify_access():
    print("Access verification completed")

@app.get(
    "/admin/",
    dependencies=[Depends(verify_access)]
)
async def admin_dashboard():
    return {"message": "Welcome to admin dashboard"}
```

Here:

- `verify_access()` is executed before the endpoint.
- The endpoint does not receive its return value.
- The dependency is still useful for executing shared checks.

This is useful for logging, access checks, and other operations that do not need to return a value to the endpoint.

## 12. Dependencies at Router Level

Dependencies can also be applied to an entire router.

Example:

```python
from fastapi import APIRouter, Depends

def verify_access():
    print("Checking access")

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_access)]
)

@router.get("/dashboard/")
async def dashboard():
    return {"message": "Admin dashboard"}

@router.get("/users/")
async def get_users():
    return {"message": "Admin users"}
```

Every endpoint registered with this router uses the declared dependency.

The router must be included in the main application:

```python
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)
```

This is useful when several related endpoints require the same dependency.

## 13. Dependencies at Application Level

FastAPI also supports dependencies at the application level.

Example:

```python
from fastapi import Depends, FastAPI

def verify_request():
    print("Request verification")

app = FastAPI(
    dependencies=[Depends(verify_request)]
)
```

The dependency applies to the application's path operations.

This can be useful for shared application-wide checks.

Choose the narrowest appropriate level:

- Endpoint-level dependency: one endpoint.
- Router-level dependency: a group of endpoints.
- Application-level dependency: application-wide behavior.

## 14. Class-Based Dependencies

A Python class can also be used as a dependency.

FastAPI calls the class to create an instance and resolves its constructor parameters.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

class CommonQueryParams:

    def __init__(
        self,
        q: str | None = None,
        skip: int = 0,
        limit: int = 10
    ):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(
    params: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
):
    return {
        "q": params.q,
        "skip": params.skip,
        "limit": params.limit
    }
```

FastAPI creates the class instance and injects it into the endpoint.

Class-based dependencies are useful when reusable logic requires multiple related parameters or methods.

## 15. Dependency Overrides for Testing

FastAPI allows developers to replace a dependency with another implementation during testing.

This is particularly useful when an endpoint depends on:

- A database.
- An external API.
- Authentication services.
- A paid AI model API.
- A remote vector database.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_current_user():
    return {"username": "production_user"}

@app.get("/profile/")
async def get_profile(
    user: Annotated[dict, Depends(get_current_user)]
):
    return user
```

During testing, we can override the dependency:

```python
def override_get_current_user():
    return {"username": "test_user"}

app.dependency_overrides[get_current_user] = (
    override_get_current_user
)
```

Now requests to the endpoint use the test dependency instead of the original dependency.

After testing, clear the override:

```python
app.dependency_overrides = {}
```

Dependency overrides help isolate tests from external systems and make them more predictable.

## 16. Depends() vs Security()

FastAPI provides both `Depends()` and `Security()`.

Both participate in the dependency injection system.

`Security()` is especially useful when working with OAuth2 scopes and permission requirements.

Example:

```python
from typing import Annotated
from fastapi import FastAPI, Security
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    return {"username": "john"}

@app.get("/users/me/")
async def read_current_user(
    user: Annotated[dict, Security(get_current_user)]
):
    return user
```

This illustrates the use of `Security()` to declare a security-related dependency.

For actual authentication, the token must be validated and the user's identity and permissions must be verified. Merely receiving a token does not authenticate a user.

| Depends() | Security() |
|---|---|
| General dependency injection | Security-related dependency injection |
| Used for shared logic, resources, and services | Useful for authentication and authorization requirements |
| Does not itself define OAuth2 scopes | Supports OAuth2 scopes through the `scopes` parameter |

## 17. Relevance to AI and RAG Applications

Dependency injection is particularly useful when deploying a RAG application through FastAPI.

Consider a RAG application that needs:

- A retriever.
- An LLM.
- A RAG pipeline.
- Configuration settings.

Instead of initializing these components inside every endpoint, we can expose them through reusable dependencies.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

class RAGService:

    def ask(self, question: str):
        return {
            "answer": f"Generated answer for: {question}",
            "sources": []
        }

def get_rag_service():
    return RAGService()

RAGServiceDependency = Annotated[
    RAGService,
    Depends(get_rag_service)
]

@app.post("/ask/")
async def ask_question(
    question: str,
    rag_service: RAGServiceDependency
):
    result = rag_service.ask(question)

    return result
```

This is a simplified illustration. The `RAGService` would be replaced by the actual retrieval and generation implementation.

A more production-oriented design would consider how expensive components such as embedding clients, vector-store connections, and LLM clients are initialized and shared.

Dependency injection helps keep the API layer separate from the AI application logic.

## 18. Best Practices

1. Use `Depends()` to share reusable application logic.
2. Prefer `Annotated` for modern dependency declarations.
3. Keep dependencies focused on one responsibility.
4. Use `yield` for resources that require cleanup.
5. Use dependency caching appropriately.
6. Use sub-dependencies to organize complex dependency relationships.
7. Apply dependencies at endpoint, router, or application level depending on their scope.
8. Use dependency overrides to isolate tests from external services.
9. Avoid initializing expensive resources repeatedly for every request when they can safely be reused.
10. Keep authentication and authorization logic separate from business logic.
11. Use asynchronous dependencies when working with asynchronous libraries.
12. Never assume that a dependency returning a user object automatically makes authentication secure; validate credentials and permissions.

## 19. Official References

- FastAPI — Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
- FastAPI — Sub-dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
- FastAPI — Dependencies with yield: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- FastAPI — Advanced Dependencies: https://fastapi.tiangolo.com/advanced/advanced-dependencies/
- FastAPI — Classes as Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
- FastAPI — Testing Dependencies with Overrides: https://fastapi.tiangolo.com/advanced/testing-dependencies/
- FastAPI — Depends Reference: https://fastapi.tiangolo.com/reference/dependencies/