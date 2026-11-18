# Request Bodies in FastAPI

## 1. Introduction

A request body is data sent by a client to an API.

For example, when a user registers an account, creates a product, or submits a document, the client sends information to the API. This information is commonly sent in the request body as JSON.

A response body is the data returned by the API to the client.

Example:

A client sends product information:

```json
{
    "name": "Laptop",
    "price": 75000,
    "description": "A high-performance laptop"
}
```

The API receives this information, validates it, processes it, and returns a response.

In FastAPI, Pydantic models are commonly used to declare and validate request bodies.

## 2. HTTP Methods That Commonly Use Request Bodies

Request bodies are commonly used with:

| HTTP Method | Typical Purpose |
|---|---|
| POST | Create a new resource |
| PUT | Replace or update a resource |
| PATCH | Partially update a resource |
| DELETE | Delete a resource; a body is occasionally used but is not typical |

POST is frequently used when submitting new data to an API.

GET requests generally should not use request bodies. Their behavior is not well-defined by HTTP specifications, and some intermediaries may not support them reliably.

## 3. Creating a Pydantic Model

To define a request body, create a Pydantic model by inheriting from `BaseModel`.

Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

Explanation:

- `BaseModel` is imported from Pydantic.
- `Item` is a Pydantic model.
- `name` is a required string.
- `description` is an optional string.
- `price` is a required floating-point number.
- `tax` is an optional floating-point number.

A field without a default value is required. A field with a default value is not required.

## 4. Declaring a Request Body in a FastAPI Endpoint

After creating the Pydantic model, declare it as a parameter in the path operation function.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

Here:

- `@app.post("/items/")` defines a POST endpoint.
- `item: Item` tells FastAPI to expect a request body matching the `Item` model.
- FastAPI reads the JSON request body, converts compatible values, and validates the data.
- The validated data is provided to the function as an `Item` object.

Example request body:

```json
{
    "name": "Laptop",
    "description": "A business laptop",
    "price": 75000,
    "tax": 5000
}
```

Example response:

```json
{
    "name": "Laptop",
    "description": "A business laptop",
    "price": 75000,
    "tax": 5000
}
```

## 5. Accessing Request Body Attributes

Once FastAPI validates the request body, you can access individual attributes using dot notation.

```python
@app.post("/items/")
async def create_item(item: Item):
    item_name = item.name
    item_price = item.price

    return {
        "name": item_name,
        "price": item_price
    }
```

Pydantic models provide structured access to data and editor support through type annotations.

## 6. Converting a Pydantic Model into a Dictionary

Pydantic v2 provides the `model_dump()` method to convert a model instance into a Python dictionary.

```python
@app.post("/items/")
async def create_item(item: Item):
    item_data = item.model_dump()

    return item_data
```

Example output:

```json
{
    "name": "Laptop",
    "description": "A business laptop",
    "price": 75000,
    "tax": 5000
}
```

This is useful when passing validated data to database operations or other application functions.

For example, `model_dump(exclude_unset=True)` can be useful when you want only fields explicitly supplied by the client.

## 7. Request Body Validation

FastAPI automatically validates request body data using the declared Pydantic model.

Consider this model:

```python
class Product(BaseModel):
    name: str
    price: float
    quantity: int
```

A valid request:

```json
{
    "name": "Keyboard",
    "price": 1500,
    "quantity": 10
}
```

An invalid request:

```json
{
    "name": "Keyboard",
    "price": "expensive",
    "quantity": "many"
}
```

The invalid request contains values that cannot be converted into the required numeric types.

FastAPI returns a validation error instead of passing invalid data to the endpoint function.

By default, request validation errors use HTTP status code `422 Unprocessable Entity`.

## 8. Using Field for Additional Validation

Pydantic's `Field` allows you to define validation rules and metadata for individual model attributes.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
```

Explanation:

- `min_length=3`: Product name must contain at least three characters.
- `max_length=50`: Product name cannot exceed 50 characters.
- `gt=0`: Price must be greater than zero.
- `ge=0`: Quantity must be greater than or equal to zero.

These constraints help prevent invalid data from entering the application.

## 9. Combining Request Bodies with Path Parameters

FastAPI allows an endpoint to receive a request body and path parameters together.

Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "name": item.name,
        "price": item.price
    }
```

Example URL:

```text
/items/101
```

Request body:

```json
{
    "name": "Laptop",
    "price": 75000
}
```

FastAPI recognizes:

- `item_id` as a path parameter because it appears in the URL.
- `item` as a request body because it is declared as a Pydantic model.

## 10. Combining Request Bodies with Path and Query Parameters

An endpoint can receive all three types of input.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    q: str | None = None
):
    result = {
        "item_id": item_id,
        "name": item.name,
        "price": item.price
    }

    if q:
        result["query"] = q

    return result
```

Example request:

```text
PUT /items/101?q=electronics
```

Request body:

```json
{
    "name": "Laptop",
    "price": 75000
}
```

FastAPI identifies the inputs as follows:

- `item_id`: Path parameter.
- `item`: Request body.
- `q`: Optional query parameter.

## 11. Multiple Request Body Parameters

FastAPI supports multiple Pydantic model parameters in one endpoint. It combines them into a single JSON request body.

Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str
    email: str

@app.post("/orders/")
async def create_order(item: Item, user: User):
    return {
        "item": item,
        "user": user
    }
```

The request body should contain both objects:

```json
{
    "item": {
        "name": "Laptop",
        "price": 75000
    },
    "user": {
        "username": "john",
        "email": "john@example.com"
    }
}
```

FastAPI validates each object against its corresponding Pydantic model.

## 12. Embedding a Single Request Body Parameter

By default, when an endpoint has one Pydantic model parameter, FastAPI expects the JSON body to contain the model's fields directly.

For example:

```python
@app.post("/items/")
async def create_item(item: Item):
    return item
```

Expected body:

```json
{
    "name": "Laptop",
    "price": 75000
}
```

If you want the request body to contain an additional key around the model, use `Body(embed=True)`.

```python
from typing import Annotated
from fastapi import Body

@app.post("/items/")
async def create_item(
    item: Annotated[Item, Body(embed=True)]
):
    return item
```

Expected body:

```json
{
    "item": {
        "name": "Laptop",
        "price": 75000
    }
}
```

This is useful when the API contract requires a named wrapper around the request object.

## 13. Using Body for Singular Values

A Pydantic model is usually the preferred way to receive structured data. However, FastAPI also provides `Body` when you need to receive a simple value directly in the request body.

Example:

```python
from typing import Annotated
from fastapi import Body

@app.post("/items/price/")
async def update_price(
    price: Annotated[float, Body()]
):
    return {"price": price}
```

The request body can contain:

```json
4999.99
```

This is different from sending a query parameter such as `?price=4999.99`.

## 14. Request Body vs Query Parameters

| Feature | Request Body | Query Parameters |
|---|---|---|
| Location | HTTP request body | URL after `?` |
| Typical format | JSON | Key-value pairs |
| Common purpose | Submit structured data | Filter, search, sort, paginate |
| Common methods | POST, PUT, PATCH | GET |
| FastAPI declaration | Pydantic model or Body | Function parameter or Query |

Example request body:

```json
{
    "name": "Laptop",
    "price": 75000
}
```

Example query parameter:

```text
/items/?category=electronics
```

## 15. Automatic API Documentation

FastAPI uses Pydantic models and their JSON Schemas to generate OpenAPI documentation.

When you declare a request body using a Pydantic model:

1. FastAPI generates the corresponding JSON Schema.
2. The schema becomes part of the application's OpenAPI specification.
3. Swagger UI displays the expected request body.
4. Developers can try the endpoint directly through the interactive documentation.

Open the following URL while the application is running:

```text
http://127.0.0.1:8000/docs
```

The endpoint will show the expected request body structure.

## 16. Relevance to AI and RAG Applications

Request bodies are particularly important when building AI applications and deploying machine learning or RAG pipelines.

For example, a RAG application may receive a user's question as JSON.

Request body:

```json
{
    "question": "What is retrieval augmented generation?",
    "top_k": 5
}
```

A FastAPI endpoint can receive this data using a Pydantic model.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class SearchRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)

@app.post("/search/")
async def search_documents(request: SearchRequest):
    return {
        "question": request.question,
        "top_k": request.top_k
    }
```

In a real RAG application, the endpoint would pass the validated question and retrieval configuration to the retrieval pipeline.

The pipeline would retrieve relevant document chunks, construct context, invoke the language model, and return the generated answer.

This demonstrates how FastAPI can act as the API layer between a client application and an AI backend.

## 17. Best Practices

1. Use Pydantic models to define structured request bodies.
2. Use meaningful field names and appropriate Python types.
3. Add validation constraints using Pydantic's `Field`.
4. Use `model_dump()` when a dictionary representation is required.
5. Separate request schemas from response schemas when their responsibilities differ.
6. Avoid accepting arbitrary unvalidated dictionaries for important application inputs.
7. Use POST, PUT, and PATCH appropriately for operations that submit data.
8. Do not use GET request bodies for ordinary API operations.
9. Keep request models focused on the data an endpoint actually needs.

## 18. Official References

- FastAPI — Request Body: https://fastapi.tiangolo.com/tutorial/body/
- FastAPI — Body Fields: https://fastapi.tiangolo.com/tutorial/body-fields/
- FastAPI — Body: Multiple Parameters: https://fastapi.tiangolo.com/tutorial/body-multiple-params/
- FastAPI — Request Parameters Reference: https://fastapi.tiangolo.com/reference/parameters/
- Pydantic — Models: https://docs.pydantic.dev/latest/concepts/models/
- Pydantic — Fields: https://docs.pydantic.dev/latest/concepts/fields/