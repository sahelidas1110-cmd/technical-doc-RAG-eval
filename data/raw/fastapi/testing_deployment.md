# Testing and Deployment in FastAPI

## 1. Introduction

Testing and deployment are important stages in building production-ready APIs.

Testing helps verify that an API behaves as expected, handles invalid inputs correctly, and returns the appropriate responses.

Deployment makes the API available to users through a server or cloud platform.

FastAPI supports testing through:

- Pytest.
- TestClient.
- HTTPX.
- Dependency overrides.
- Asynchronous testing.

For deployment, commonly used tools include:

- Uvicorn.
- Docker.
- Docker Compose.
- Cloud hosting platforms.
- Reverse proxies and load balancers.

## 2. Testing in FastAPI

Testing is the process of verifying that an application works correctly under different conditions.

For a FastAPI application, testing can include:

- Checking whether endpoints return the correct status codes.
- Validating response JSON.
- Testing request-body validation.
- Testing authentication and authorization.
- Checking error handling.
- Testing dependency behavior.
- Testing integration with databases and external services.

Automated testing helps identify problems before an application is deployed.

## 3. Installing Testing Dependencies

FastAPI provides `TestClient` for testing API endpoints.

It is based on Starlette's TestClient and uses HTTPX.

Install the required packages:

```powershell
uv add --dev pytest httpx
```

Here:

- `pytest` is the testing framework.
- `httpx` provides the HTTP client functionality used by TestClient.

## 4. Creating a Simple FastAPI Application for Testing

Consider the following application.

Create a file named `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}
```

This application contains two endpoints:

- `GET /` returns a welcome message.
- `GET /items/{item_id}` returns an item ID.

## 5. Understanding TestClient

FastAPI provides `TestClient` through:

```python
from fastapi.testclient import TestClient
```

It allows developers to send HTTP requests to the application without starting a separate live server.

Example:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.get("/")

print(response.status_code)
print(response.json())
```

Output:

```text
200
{'message': 'Hello World'}
```

Important points:

- `client.get()` sends a GET request.
- `response.status_code` provides the HTTP status code.
- `response.json()` returns the response body as a Python object.

Other supported methods include:

```python
client.get()
client.post()
client.put()
client.patch()
client.delete()
```

## 6. Writing Your First Pytest Test

Pytest automatically discovers test functions whose names start with `test_`.

Create a file named `test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Hello World"
    }
```

Explanation:

- `test_home()` is the test function.
- `client.get("/")` sends a request to the root endpoint.
- `assert` checks whether the actual result matches the expected result.

If all assertions pass, the test succeeds.

## 7. Testing Path Parameters

We can test endpoints that accept path parameters.

Example:

```python
def test_get_item():
    response = client.get("/items/101")

    assert response.status_code == 200

    assert response.json() == {
        "item_id": 101
    }
```

This verifies that the endpoint correctly receives and returns the item ID.

## 8. Testing Invalid Inputs

Testing should also cover invalid requests.

Consider the endpoint:

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}
```

The endpoint expects an integer.

Test an invalid value:

```python
def test_invalid_item_id():
    response = client.get("/items/abc")

    assert response.status_code == 422
```

FastAPI automatically validates the path parameter and returns a validation error when the value cannot be converted into an integer.

Testing invalid input is important because APIs should handle incorrect requests predictably.

## 9. Testing POST Requests

POST endpoints commonly receive JSON request bodies.

Example application:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float

@app.post("/products/")
async def create_product(product: Product):
    return product
```

Test:

```python
def test_create_product():
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "price": 75000
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "name": "Laptop",
        "price": 75000
    }
```

The `json` argument sends the supplied Python dictionary as JSON.

You can also test invalid request bodies:

```python
def test_invalid_product():
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "price": "expensive"
        }
    )

    assert response.status_code == 422
```

## 10. Organizing Test Files

For larger projects, tests should be maintained separately from application code.

Example structure:

```text
fastapi-project/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_products.py
│
├── pyproject.toml
└── README.md
```

This structure separates application logic from test code.

For your portfolio project, you can use a similar structure when adding FastAPI deployment to the RAG application.

## 11. Running Pytest

Run all tests from the project root:

```powershell
uv run pytest
```

Run a particular test file:

```powershell
uv run pytest tests/test_main.py
```

Run a specific test function:

```powershell
uv run pytest tests/test_main.py::test_home
```

Run tests with more detailed output:

```powershell
uv run pytest -v
```

Example output:

```text
============================= test session starts =============================

collected 3 items

tests/test_main.py ...                                      [100%]

============================== 3 passed ==============================
```

Common pytest outcomes:

| Result | Meaning |
|---|---|
| PASSED | Test completed successfully |
| FAILED | An assertion or test condition failed |
| ERROR | An error occurred while setting up or running the test |
| SKIPPED | Test was intentionally skipped |

## 12. Using Fixtures in Pytest

A fixture provides reusable test setup or resources.

Pytest provides the `@pytest.fixture` decorator.

Example:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
```

Explanation:

- `@pytest.fixture` defines a reusable fixture.
- The `client()` fixture creates a TestClient.
- Pytest automatically supplies the fixture to a test function that requests it.

Fixtures are useful for:

- Creating test clients.
- Setting up test databases.
- Preparing sample data.
- Cleaning up resources.
- Managing authentication tokens.

### Fixture with Setup and Teardown

A fixture can use `yield` to perform cleanup after a test.

```python
import pytest

@pytest.fixture
def sample_resource():

    print("Setting up resource")

    resource = {"status": "active"}

    yield resource

    print("Cleaning up resource")
```

The code before `yield` performs setup.

The code after `yield` performs cleanup.

## 13. Testing Dependencies with Overrides

FastAPI allows developers to replace dependencies during testing.

This is especially useful when an endpoint depends on an external service or database.

Example application:

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_current_user():
    return {"username": "production_user"}

@app.get("/profile/")
async def get_profile(
    user: dict = Depends(get_current_user)
):
    return user
```

Test code:

```python
from fastapi.testclient import TestClient
from main import app, get_current_user

def override_get_current_user():
    return {"username": "test_user"}

app.dependency_overrides[get_current_user] = (
    override_get_current_user
)

client = TestClient(app)

def test_profile():
    response = client.get("/profile/")

    assert response.status_code == 200

    assert response.json() == {
        "username": "test_user"
    }
```

After testing, dependency overrides should be cleared:

```python
app.dependency_overrides = {}
```

For larger test suites, use fixtures to set up and restore overrides automatically.

This technique helps test applications without depending on real authentication systems, paid APIs, or production databases.

## 14. Testing Asynchronous Applications

FastAPI supports asynchronous endpoints using `async def`.

The regular TestClient allows synchronous test functions to call these endpoints.

However, sometimes tests need to interact directly with asynchronous resources, such as:

- Async database clients.
- Async HTTP clients.
- Asynchronous application functions.

For these situations, FastAPI supports asynchronous testing using HTTPX's `AsyncClient` and `ASGITransport`.

Install HTTPX if it is not already installed:

```powershell
uv add --dev httpx
```

Example:

```python
import pytest

from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.anyio
async def test_home():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        response = await client.get("/")

    assert response.status_code == 200
```

This approach allows tests to make asynchronous requests directly to the ASGI application.

For applications that depend on lifespan startup and shutdown behavior, configure lifespan handling explicitly in the test setup. `ASGITransport` alone does not automatically run lifespan events.

## 15. Code Coverage

Code coverage measures how much of an application's code is executed during testing.

It helps identify code paths that have not been tested.

Install pytest-cov:

```powershell
uv add --dev pytest-cov
```

Run:

```powershell
uv run pytest --cov=app tests/
```

Generate an HTML report:

```powershell
uv run pytest --cov=app --cov-report=html tests/
```

Pytest generates an HTML report in:

```text
htmlcov/
```

Open `htmlcov/index.html` in a browser to inspect the coverage report.

Coverage is useful, but a high coverage percentage does not automatically mean that tests are meaningful or comprehensive.

## 16. Running FastAPI with Uvicorn

Uvicorn is an ASGI server used to run FastAPI applications.

Install FastAPI with its standard optional dependencies:

```powershell
uv add "fastapi[standard]"
```

This includes Uvicorn and other recommended dependencies.

Suppose your project contains:

```text
app/
    main.py
```

And `main.py` contains:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "FastAPI is running"}
```

Run the application:

```powershell
uv run uvicorn app.main:app --reload
```

Explanation:

| Command Part | Meaning |
|---|---|
| `uv run` | Executes the command in the project's environment |
| `uvicorn` | Starts the ASGI server |
| `app.main` | Refers to `main.py` inside the `app` package |
| `:app` | Refers to the FastAPI application object |
| `--reload` | Automatically reloads the application during development |

Open:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

## 17. Development vs Production Server Configuration

During development, use:

```powershell
uv run uvicorn app.main:app --reload
```

The `--reload` option restarts the server when code changes.

For production, do not use `--reload`.

A production command can be:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Explanation:

- `--host 0.0.0.0` makes the application listen on all network interfaces.
- `--port 8000` specifies the listening port.
- Omitting `--reload` avoids development reload behavior.

FastAPI also provides a CLI:

```powershell
uv run fastapi dev app/main.py
```

For development, and:

```powershell
uv run fastapi run app/main.py
```

For production-oriented execution.

The FastAPI CLI uses Uvicorn underneath.

## 18. Understanding Workers

Workers are separate server processes that can handle requests concurrently.

Uvicorn supports multiple worker processes.

Example:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

This starts four worker processes.

Benefits include:

- Better use of multiple CPU cores.
- Handling requests across multiple processes.
- Increased application capacity for suitable workloads.

However, each worker generally has its own memory space.

This is important for AI applications because loading a large machine learning model or embedding model separately in each worker can consume substantial memory.

For container-based deployments with an orchestrator such as Kubernetes, a common approach is one server process per container and replication at the container level.

Choose the number of workers based on CPU, memory, workload, and deployment architecture.

## 19. Environment Variables and Configuration

Production applications should not hardcode sensitive configuration values.

Examples include:

- Database connection strings.
- OpenAI API keys.
- JWT signing secrets.
- External service credentials.
- Application environment settings.

These values should be provided through environment variables or a secure secret-management system.

Example `.env` file:

```text
OPENAI_API_KEY=your_api_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ENVIRONMENT=development
```

Do not commit `.env` files containing real secrets to GitHub.

### Reading Environment Variables

Python provides `os.getenv()`:

```python
import os

secret_key = os.getenv("SECRET_KEY")

environment = os.getenv(
    "ENVIRONMENT",
    "development"
)
```

### Using python-dotenv

Install:

```powershell
uv add python-dotenv
```

Example:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

For production, inject environment variables through the hosting platform or secret manager rather than relying on a local `.env` file.

### Using Pydantic Settings

Pydantic Settings provides structured application configuration.

Install:

```powershell
uv add pydantic-settings
```

Example:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    openai_api_key: str
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
```

This provides typed configuration and centralizes application settings.

## 20. Docker Basics

Docker is a platform used to package applications and their dependencies into containers.

A container provides a consistent runtime environment across different systems.

Docker is useful because it helps:

- Package an application with its dependencies.
- Maintain consistent environments.
- Simplify deployment.
- Isolate application processes.
- Support scaling through container orchestration.

### Important Docker Concepts

| Concept | Meaning |
|---|---|
| Dockerfile | Instructions for building an image |
| Docker Image | Packaged application environment |
| Docker Container | Running instance of an image |
| Docker Volume | Persistent storage mechanism |
| Docker Network | Communication between containers |
| Docker Compose | Tool for defining and running multiple services |

## 21. Creating a Dockerfile

Suppose your FastAPI application has this structure:

```text
fastapi-project/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── requirements.txt
└── Dockerfile
```

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

Explanation:

**FROM**

Selects the base Python image.

**WORKDIR**

Sets the working directory inside the container.

**COPY**

Copies the dependency file and application code into the container.

**RUN**

Installs the required Python packages.

**CMD**

Defines the command executed when the container starts.

The exec form of `CMD` is recommended so the server process can receive operating-system signals correctly.

This is a basic example. A production Dockerfile should also consider dependency pinning, non-root execution, image size, secret handling, and security updates.

## 22. Building a Docker Image

Run this command from the directory containing the Dockerfile:

```powershell
docker build -t fastapi-app .
```

Explanation:

- `docker build` builds a Docker image.
- `-t fastapi-app` assigns a name to the image.
- `.` specifies the current directory as the build context.

## 23. Running a Docker Container

Start the container:

```powershell
docker run -d --name fastapi-container -p 8000:80 fastapi-app
```

Explanation:

| Option | Meaning |
|---|---|
| `-d` | Runs the container in the background |
| `--name` | Assigns a container name |
| `-p 8000:80` | Maps host port 8000 to container port 80 |
| `fastapi-app` | Specifies the image |

Access the API:

```text
http://localhost:8000
```

Check running containers:

```powershell
docker ps
```

View container logs:

```powershell
docker logs fastapi-container
```

Stop the container:

```powershell
docker stop fastapi-container
```

Remove the container:

```powershell
docker rm fastapi-container
```

## 24. Using Docker with uv

If a project uses `uv` for dependency management, the dependency versions are recorded in:

```text
pyproject.toml
uv.lock
```

The Docker build can use these files to maintain consistent dependencies.

One approach is to export a requirements file:

```powershell
uv export --format requirements-txt --no-dev --no-emit-project --output-file requirements.txt
```

The generated requirements file can then be used by the Dockerfile.

An alternative is to install and use `uv` directly inside the container.

For a project already managed with `uv`, retain `uv` as the primary dependency manager and regenerate the exported requirements file whenever dependencies change.

## 25. Deployment Concepts

Deployment means making an application available to users through an appropriate hosting environment.

A production deployment requires more than simply starting Uvicorn.

Important considerations include:

### 25.1 HTTPS

HTTPS encrypts communication between clients and servers.

It protects sensitive information such as:

- Login credentials.
- Access tokens.
- API keys sent by clients.
- Other private request data.

HTTPS is commonly configured through a reverse proxy, load balancer, or cloud platform.

### 25.2 Automatic Startup

The application should start automatically when the hosting environment starts.

Tools such as Docker, Docker Compose, Kubernetes, and process managers can help manage application startup.

### 25.3 Restart Management

Production systems should be able to restart an application after an unexpected failure.

Container platforms and process managers commonly provide restart policies.

### 25.4 Replication and Scaling

Replication means running multiple instances of an application to handle more requests.

Scaling can be achieved using:

- Multiple Uvicorn worker processes.
- Multiple containers.
- Multiple machines.
- Container orchestration systems.

The correct approach depends on the application's resource requirements.

### 25.5 Monitoring

Production systems should monitor:

- API response time.
- Request volume.
- Error rates.
- CPU usage.
- Memory consumption.
- Application logs.
- External service failures.

Monitoring helps identify performance problems and operational failures.

## 26. Relevance to AI and RAG Applications

Testing and deployment are particularly important when exposing an AI or RAG pipeline through FastAPI.

Consider a RAG application that accepts questions and returns answers supported by retrieved documents.

A production-oriented structure might look like:

```text
technical-doc-RAG-eval/
│
├── src/
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── embeddings.py
│   └── config.py
│
├── tests/
│   ├── test_api.py
│   ├── test_retriever.py
│   └── test_rag_pipeline.py
│
├── evaluation/
├── data/
├── Dockerfile
├── pyproject.toml
└── README.md
```

### Example RAG API Endpoint

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)

class QuestionResponse(BaseModel):
    question: str
    answer: str

@app.post("/ask/", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):

    # In a real application, call the RAG pipeline here.
    answer = "Example answer generated from retrieved context."

    return QuestionResponse(
        question=request.question,
        answer=answer
    )
```

This demonstrates how FastAPI can expose a RAG pipeline through an HTTP endpoint.

### What Should Be Tested in a RAG API?

**API-level tests**

- Does the endpoint accept a valid question?
- Does it reject an invalid request?
- Does it return the expected JSON structure?
- Does it handle missing or invalid parameters?

**Retrieval-level tests**

- Does the retriever return relevant documents?
- Are the expected source documents included?
- Does the retrieval pipeline respect `top_k`?

**Generation-level tests**

- Does the LLM answer using the retrieved context?
- Does it abstain when information is insufficient?
- Does it provide valid source references?

**Performance tests**

- How long does retrieval take?
- How long does LLM generation take?
- What is the total API response time?
- How does the application behave under concurrent requests?

For AI applications, API tests and RAG quality evaluations serve different purposes. A successful HTTP response does not necessarily mean that the generated answer is factually correct.

## 27. Best Practices

1. Write automated tests for important API endpoints.
2. Use pytest and TestClient for API testing.
3. Test both valid and invalid inputs.
4. Use fixtures for reusable test setup.
5. Override external dependencies during testing.
6. Keep application code and tests organized separately.
7. Use code coverage to identify untested areas.
8. Do not use the development reload option in production.
9. Store secrets in environment variables or secure secret managers.
10. Use Docker when consistent application packaging is required.
11. Configure HTTPS and appropriate restart policies.
12. Monitor CPU, memory, latency, and error rates.
13. Consider the memory impact of multiple workers when serving machine learning models.
14. Test API behavior separately from AI output quality.
15. Include deployment instructions in your project's README.

## 28. Official References

- FastAPI — Testing: https://fastapi.tiangolo.com/tutorial/testing/
- FastAPI — Async Tests: https://fastapi.tiangolo.com/advanced/async-tests/
- FastAPI — Testing Dependencies with Overrides: https://fastapi.tiangolo.com/advanced/testing-dependencies/
- FastAPI — Run a Server Manually: https://fastapi.tiangolo.com/deployment/manually/
- FastAPI — Deployment Concepts: https://fastapi.tiangolo.com/deployment/concepts/
- FastAPI — Docker Deployment: https://fastapi.tiangolo.com/deployment/docker/
- Pytest Documentation: https://docs.pytest.org/
- HTTPX Documentation: https://www.python-httpx.org/
- Uvicorn Documentation: https://www.uvicorn.org/
- Docker Documentation: https://docs.docker.com/