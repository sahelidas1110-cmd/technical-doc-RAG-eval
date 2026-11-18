# Response Models in FastAPI

## 1. Introduction

A response model defines the structure and format of the data returned by an API endpoint.

In FastAPI, response models are generally defined using Pydantic models.

They help ensure that:

- API responses follow a consistent structure.
- Returned data has the expected types.
- Unwanted or sensitive fields are excluded.
- API documentation describes the expected response.
- Clients receive predictable JSON data.

For example, an API may internally store a user's username, email, and password hash. However, the API should return only the username and email to the client.

A response model helps enforce this separation.

## 2. Creating a Response Model

A response model is a Pydantic model that defines the fields an API should return.

Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProductResponse(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.get("/products/")
async def get_product():
    return {
        "name": "Laptop",
        "price": 75000,
        "description": "Business laptop"
    }
```

The example defines a Pydantic model, but the endpoint has not yet explicitly declared it as its response model.

We can do that using `response_model`.

## 3. Using response_model

FastAPI provides the `response_model` parameter in path operation decorators.

Example:

```python
@app.get("/products/", response_model=ProductResponse)
async def get_product():
    return {
        "name": "Laptop",
        "price": 75000,
        "description": "Business laptop"
    }
```

Here:

- `response_model=ProductResponse` specifies the expected response structure.
- FastAPI validates the returned data against the model.
- FastAPI serializes the data into JSON.
- Fields not declared in the response model are filtered out.

The response model is specified in the decorator, not as a parameter inside the endpoint function.

## 4. Response Validation

FastAPI validates the data returned by the endpoint against the declared response model.

Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProductResponse(BaseModel):
    name: str
    price: float

@app.get("/products/", response_model=ProductResponse)
async def get_product():
    return {
        "name": "Laptop",
        "price": 75000
    }
```

This response is valid because it contains the required fields with compatible values.

Consider an invalid response:

```python
@app.get("/products/", response_model=ProductResponse)
async def get_product():
    return {
        "name": "Laptop",
        "price": "expensive"
    }
```

The returned data does not satisfy the response model.

FastAPI raises a response validation error. This is treated as an application-side error rather than a client request validation error.

By default, the client receives an HTTP 500 Internal Server Error.

This helps developers identify problems in the data their API returns.

## 5. Response Filtering and Data Security

One of the most important benefits of response models is filtering unwanted fields.

Consider an internal user object containing sensitive information.

```python
user_data = {
    "username": "john",
    "email": "john@example.com",
    "password_hash": "hashed_password_value",
    "is_admin": True
}
```

We do not want to expose the password hash to the client.

Create a public response model:

```python
class UserResponse(BaseModel):
    username: str
    email: str
```

Use it in the endpoint:

```python
@app.get("/users/", response_model=UserResponse)
async def get_user():
    return {
        "username": "john",
        "email": "john@example.com",
        "password_hash": "hashed_password_value",
        "is_admin": True
    }
```

The client receives:

```json
{
    "username": "john",
    "email": "john@example.com"
}
```

The `password_hash` and `is_admin` fields are excluded because they are not part of the response model.

This is an important security practice: explicitly define which data is allowed to leave the API.

## 6. Separate Request and Response Models

It is often useful to define separate models for incoming requests and outgoing responses.

For example, a user registration endpoint needs to receive a password, but the API should never return that password.

Example:

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr
```

Endpoint:

```python
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
```

FastAPI filters the returned data according to `UserResponse`.

The response contains only:

```json
{
    "username": "john",
    "email": "john@example.com"
}
```

In a real application, passwords should be securely hashed and stored. They should not be returned to clients.

Note: `EmailStr` requires the optional `email-validator` dependency to be installed.

## 7. Returning a List of Response Models

A response model can also describe a collection of objects.

Example:

```python
class ProductResponse(BaseModel):
    name: str
    price: float

@app.get("/products/", response_model=list[ProductResponse])
async def get_products():
    return [
        {"name": "Laptop", "price": 75000},
        {"name": "Mobile", "price": 25000},
        {"name": "Keyboard", "price": 1500}
    ]
```

FastAPI validates each item in the returned list against `ProductResponse`.

Example response:

```json
[
    {
        "name": "Laptop",
        "price": 75000
    },
    {
        "name": "Mobile",
        "price": 25000
    },
    {
        "name": "Keyboard",
        "price": 1500
    }
]
```

This is useful for endpoints that return search results, product listings, or collections of records.

## 8. Using Different Response Model Options

FastAPI provides several options to control which fields appear in the response.

### 8.1 response_model_exclude_unset

This option excludes fields that were not explicitly set in the returned data.

Example:

```python
class ItemResponse(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float = 10.5

@app.get(
    "/items/",
    response_model=ItemResponse,
    response_model_exclude_unset=True
)
async def get_item():
    return {
        "name": "Laptop",
        "price": 75000
    }
```

Response:

```json
{
    "name": "Laptop",
    "price": 75000
}
```

The `description` and `tax` fields are omitted because they were not explicitly supplied.

### 8.2 response_model_exclude_defaults

This option excludes fields whose values are equal to their model defaults.

Example:

```python
@app.get(
    "/items/",
    response_model=ItemResponse,
    response_model_exclude_defaults=True
)
async def get_item():
    return {
        "name": "Laptop",
        "price": 75000,
        "tax": 10.5
    }
```

The `tax` field has the same value as its default, so it is excluded.

### 8.3 response_model_exclude_none

This option excludes fields whose values are `None`.

Example:

```python
@app.get(
    "/items/",
    response_model=ItemResponse,
    response_model_exclude_none=True
)
async def get_item():
    return {
        "name": "Laptop",
        "price": 75000,
        "description": None
    }
```

The response excludes `description` because its value is `None`.

### Comparison

| Option | What it excludes |
|---|---|
| `response_model_exclude_unset` | Fields not explicitly set |
| `response_model_exclude_defaults` | Fields whose values equal their defaults |
| `response_model_exclude_none` | Fields with `None` values |

These options have different behavior and should not be treated as interchangeable.

## 9. Including and Excluding Specific Fields

FastAPI provides two additional options:

- `response_model_include`
- `response_model_exclude`

Example using `response_model_include`:

```python
class ItemResponse(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

@app.get(
    "/items/",
    response_model=ItemResponse,
    response_model_include={"name", "price"}
)
async def get_item():
    return {
        "name": "Laptop",
        "price": 75000,
        "description": "Business laptop",
        "tax": 5000
    }
```

Only `name` and `price` are returned.

Example using `response_model_exclude`:

```python
@app.get(
    "/items/",
    response_model=ItemResponse,
    response_model_exclude={"tax"}
)
async def get_item():
    return {
        "name": "Laptop",
        "price": 75000,
        "description": "Business laptop",
        "tax": 5000
    }
```

The `tax` field is excluded.

For larger applications, separate Pydantic models are generally preferable to relying heavily on include and exclude options. This keeps the generated OpenAPI schema aligned with the actual response structure.

## 10. Response Models and Python Return Type Annotations

FastAPI supports declaring a response type using the function's return type annotation.

Example:

```python
@app.get("/products/")
async def get_product() -> ProductResponse:
    return ProductResponse(
        name="Laptop",
        price=75000
    )
```

This tells FastAPI and Python development tools that the endpoint returns a `ProductResponse`.

Alternatively, you can use the decorator parameter:

```python
@app.get("/products/", response_model=ProductResponse)
async def get_product():
    return {
        "name": "Laptop",
        "price": 75000
    }
```

Both approaches can be used to define the expected response.

If both are provided, `response_model` takes priority for FastAPI's response validation and serialization.

Use `response_model=None` when you need to disable response model generation for a particular endpoint.

## 11. Nested Response Models

Pydantic supports nested models, allowing APIs to return complex structured responses.

Example:

```python
from pydantic import BaseModel

class AddressResponse(BaseModel):
    city: str
    country: str

class UserResponse(BaseModel):
    username: str
    email: str
    address: AddressResponse
```

Endpoint:

```python
@app.get("/users/", response_model=UserResponse)
async def get_user():
    return {
        "username": "john",
        "email": "john@example.com",
        "address": {
            "city": "Kolkata",
            "country": "India"
        }
    }
```

Response:

```json
{
    "username": "john",
    "email": "john@example.com",
    "address": {
        "city": "Kolkata",
        "country": "India"
    }
}
```

Nested response models are useful when an API returns related objects, such as users with addresses or orders with product details.

## 12. Response Models and Status Codes

FastAPI allows you to specify the HTTP status code returned by an endpoint.

Example:

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class ProductResponse(BaseModel):
    name: str
    price: float

@app.post(
    "/products/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product():
    return {
        "name": "Laptop",
        "price": 75000
    }
```

The endpoint returns HTTP status code `201 Created` when the operation succeeds.

Some commonly used status codes:

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
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

The status code describes the outcome of the HTTP operation, while the response model describes the structure of the returned data.

## 13. Returning a Response Directly

FastAPI normally converts returned data into JSON responses.

However, sometimes an endpoint needs to return a specific response object.

FastAPI provides response classes such as:

- `JSONResponse`
- `HTMLResponse`
- `PlainTextResponse`
- `RedirectResponse`
- `FileResponse`
- `StreamingResponse`

Example using JSONResponse:

```python
from fastapi.responses import JSONResponse

@app.get("/message/")
async def get_message():
    return JSONResponse(
        content={"message": "Operation successful"},
        status_code=200
    )
```

Returning a `Response` object directly gives you more control over the response.

When returning a response directly, FastAPI does not automatically perform the normal response-model validation and filtering on that response object. You are responsible for ensuring its content is correct.

## 14. Automatic API Documentation

Response models are integrated with FastAPI's OpenAPI documentation.

When you declare a response model:

1. FastAPI generates a JSON Schema for the response.
2. The schema is included in the OpenAPI specification.
3. Swagger UI displays the expected response structure.
4. API consumers can understand the data returned by the endpoint.

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The response section displays the expected response model.

## 15. Relevance to AI and RAG Applications

Response models are important when deploying RAG and AI applications.

For example, a RAG application may return:

- The generated answer.
- The retrieved source documents.
- Retrieval metadata.
- Execution information.

Define response models:

```python
from pydantic import BaseModel

class SourceDocument(BaseModel):
    source: str
    page: int | None = None
    content: str

class RAGResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceDocument]
```

Example endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/ask/", response_model=RAGResponse)
async def ask_question():

    return {
        "question": "What is RAG?",
        "answer": "RAG combines retrieval with language generation.",
        "sources": [
            {
                "source": "rag_architecture.md",
                "page": None,
                "content": "RAG retrieves relevant information..."
            }
        ]
    }
```

This creates a predictable JSON response for the frontend.

In a real application, the endpoint would obtain the answer and source documents from the RAG pipeline rather than returning hardcoded data.

Response models also help ensure that internal implementation details, API keys, raw database fields, or other sensitive information are not accidentally exposed.

## 16. Best Practices

1. Define Pydantic response models for important API endpoints.
2. Separate request models from response models.
3. Never expose passwords, API keys, or internal database fields in public responses.
4. Use `response_model` to validate and filter returned data.
5. Use separate models for public and internal representations.
6. Use `response_model_exclude_unset` when omitted fields should remain absent.
7. Use meaningful HTTP status codes.
8. Use nested response models for complex JSON structures.
9. Keep response schemas consistent across related endpoints.
10. Test response structures as part of API testing.

## 17. Official References

- FastAPI — Response Model: https://fastapi.tiangolo.com/tutorial/response-model/
- FastAPI — Custom Response: https://fastapi.tiangolo.com/advanced/custom-response/
- FastAPI — Response Status Code: https://fastapi.tiangolo.com/tutorial/response-status-code/
- Pydantic — Models: https://docs.pydantic.dev/latest/concepts/models/