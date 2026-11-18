# Path and Query Parameters in FastAPI

## 1. Introduction

FastAPI supports different ways of receiving input from a client. Two commonly used methods are:

- **Path parameters:** Values included directly in the URL path.
- **Query parameters:** Key-value pairs included after the `?` symbol in a URL.

Both are commonly used in REST APIs to identify resources, filter records, and control how data is retrieved.

## 2. Path Parameters

Path parameters are variables included in the URL path.

Example URL:

```text
/items/101
```

Here, `101` is the path parameter representing the item ID.

In FastAPI, path parameters are declared using curly braces in the route definition.

### Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

In this example:

- `{item_id}` defines a variable part of the URL.
- `item_id: int` tells FastAPI that the value should be an integer.
- FastAPI converts the incoming value into an integer and validates it.

Example request:

```text
http://127.0.0.1:8000/items/101
```

Response:

```json
{
    "item_id": 101
}
```

If a client sends a value that cannot be converted into an integer, FastAPI returns a validation error.

### Multiple Path Parameters

An endpoint can contain multiple path parameters.

```python
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: int):
    return {
        "user_id": user_id,
        "item_id": item_id
    }
```

Example URL:

```text
/users/10/items/25
```

Response:

```json
{
    "user_id": 10,
    "item_id": 25
}
```

## 3. Query Parameters

Query parameters are key-value pairs passed in the URL after the `?` symbol.

Multiple query parameters are separated using `&`.

Example:

```text
/items/?skip=0&limit=10
```

Here:

- `skip=0` specifies the number of records to skip.
- `limit=10` specifies the maximum number of records to return.

### Example

```python
from fastapi import FastAPI

app = FastAPI()

items = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Mobile"},
    {"id": 3, "name": "Keyboard"},
    {"id": 4, "name": "Mouse"}
]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return items[skip : skip + limit]
```

Example request:

```text
http://127.0.0.1:8000/items/?skip=1&limit=2
```

Response:

```json
[
    {"id": 2, "name": "Mobile"},
    {"id": 3, "name": "Keyboard"}
]
```

FastAPI identifies parameters that are not part of the route path as query parameters, unless they are declared differently.

## 4. Required Query Parameters

A query parameter is required when no default value is provided.

```python
@app.get("/items/")
async def read_items(category: str):
    return {"category": category}
```

The following request provides the required parameter:

```text
/items/?category=electronics
```

Response:

```json
{
    "category": "electronics"
}
```

If the client does not provide `category`, FastAPI returns a validation error.

## 5. Optional Query Parameters

A query parameter can be made optional by assigning `None` as its default value.

```python
@app.get("/items/")
async def read_items(q: str | None = None):
    if q:
        return {"search_query": q}

    return {"message": "No search query provided"}
```

Here:

- `str | None` means the parameter can contain a string or `None`.
- `= None` makes the parameter optional.

Example requests:

```text
/items/?q=laptop
```

```text
/items/
```

The first request provides a search query. The second request uses the default value `None`.

**Important:** The type annotation `str | None` alone does not make a parameter optional. The default value determines whether the parameter is required.

## 6. Default Values in Query Parameters

Default values are useful when an API should work even if the client does not provide every parameter.

```python
@app.get("/products/")
async def get_products(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "name"
):
    return {
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by
    }
```

If no query parameters are provided, FastAPI uses:

- `skip = 0`
- `limit = 20`
- `sort_by = "name"`

The client can override these defaults through the URL.

## 7. Type Conversion and Validation

FastAPI uses Python type annotations to convert and validate incoming parameter values.

Common types include:

- `str`
- `int`
- `float`
- `bool`

Example:

```python
@app.get("/products/")
async def get_products(
    product_id: int,
    price: float,
    available: bool
):
    return {
        "product_id": product_id,
        "price": price,
        "available": available
    }
```

Example request:

```text
/products/?product_id=101&price=499.99&available=true
```

FastAPI converts the URL values into the corresponding Python types.

Boolean values can be represented using values such as `true`, `false`, `1`, `0`, `yes`, and `no` (case-insensitive).

If a value cannot be converted or validated, FastAPI returns a structured validation error, typically with HTTP status code `422`.

## 8. Using Query for Additional Validation

FastAPI provides `Query` to define additional validation rules and metadata for query parameters.

The recommended modern approach is to use `Annotated`.

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None
):
    return {"q": q}
```

In this example:

- `min_length=3` requires at least three characters.
- `max_length=50` limits the value to 50 characters.
- `None` makes the parameter optional.

Other useful Query validation options include:

| Parameter | Purpose |
|---|---|
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `pattern` | Regular expression pattern |
| `gt` | Greater than |
| `ge` | Greater than or equal to |
| `lt` | Less than |
| `le` | Less than or equal to |
| `description` | Parameter description |
| `alias` | Alternative external parameter name |

### Numeric Query Validation

```python
@app.get("/products/")
async def get_products(
    price: Annotated[float, Query(gt=0, le=100000)]
):
    return {"price": price}
```

The price must be greater than zero and less than or equal to 100,000.

## 9. Using Path for Additional Validation

FastAPI provides `Path` to add validation and metadata to path parameters.

```python
from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(gt=0, le=1000)]
):
    return {"item_id": item_id}
```

Here:

- `gt=0` means the ID must be greater than zero.
- `le=1000` means the ID cannot exceed 1000.

Path parameters are always required because they are part of the URL path.

Unlike query parameters, a path parameter cannot be made optional simply by assigning `None` as its default.

## 10. Using Aliases for Query Parameters

Sometimes an API needs to expose a parameter name that differs from the Python variable name.

The `alias` option allows this.

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    item_query: Annotated[str | None, Query(alias="item-query")] = None
):
    return {"search": item_query}
```

Example request:

```text
/items/?item-query=laptop
```

The client uses `item-query`, while the Python function uses `item_query`.

## 11. Multiple Values for a Query Parameter

A query parameter can accept multiple values using a list.

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    tags: Annotated[list[str] | None, Query()] = None
):
    return {"tags": tags}
```

Example request:

```text
/items/?tags=electronics&tags=computers
```

Response:

```json
{
    "tags": ["electronics", "computers"]
}
```

This is useful when clients need to filter records using multiple categories or tags.

## 12. Combining Path and Query Parameters

FastAPI can handle path and query parameters in the same endpoint.

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users/{user_id}/orders/")
async def get_user_orders(
    user_id: int,
    status: Annotated[str | None, Query()] = None,
    limit: int = 10
):
    return {
        "user_id": user_id,
        "status": status,
        "limit": limit
    }
```

Example request:

```text
/users/101/orders/?status=completed&limit=5
```

Here:

- `user_id` is a path parameter.
- `status` is an optional query parameter.
- `limit` is a query parameter with a default value.

FastAPI identifies each parameter based on its declaration and type.

## 13. Path Parameters vs Query Parameters

| Feature | Path Parameters | Query Parameters |
|---|---|---|
| Location | Inside the URL path | After `?` in the URL |
| Syntax | `/items/{item_id}` | `/items/?limit=10` |
| Typical use | Identify a specific resource | Filter, sort, search, or paginate |
| Required | Always required | Can be required or optional |
| FastAPI helpers | `Path` | `Query` |

### Example

Path parameter:

```text
/users/101
```

This identifies a particular user.

Query parameter:

```text
/users/?active=true
```

This filters users based on their active status.

## 14. Best Practices

1. Use path parameters to identify specific resources.
2. Use query parameters for filtering, searching, sorting, and pagination.
3. Add Python type annotations to enable automatic conversion and validation.
4. Use `Query` and `Path` when additional validation or metadata is required.
5. Prefer `Annotated` for modern FastAPI parameter declarations.
6. Provide sensible defaults for optional query parameters.
7. Validate user input instead of assuming that incoming values are correct.
8. Use meaningful parameter names and descriptions.

## 15. Relevance to AI and RAG Applications

Path and query parameters are important when deploying AI applications through FastAPI.

For example, a RAG application might expose an endpoint like:

```text
/documents/123
```

Here, `123` identifies a document.

A search endpoint might look like:

```text
/search/?query=machine-learning&top_k=5
```

Here:

- `query` contains the user's search text.
- `top_k` controls how many relevant document chunks are retrieved.

Example endpoint:

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/search/")
async def search_documents(
    query: Annotated[str, Query(min_length=3)],
    top_k: Annotated[int, Query(ge=1, le=20)] = 5
):
    return {
        "query": query,
        "top_k": top_k
    }
```

This demonstrates how FastAPI can validate inputs before passing them to a RAG retrieval pipeline.

## 16. Official References

- FastAPI — Path Parameters: https://fastapi.tiangolo.com/tutorial/path-params/
- FastAPI — Query Parameters: https://fastapi.tiangolo.com/tutorial/query-params/
- FastAPI — Path Parameters and Numeric Validations: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
- FastAPI — Query Parameters and String Validations: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
- FastAPI — Request Parameters Reference: https://fastapi.tiangolo.com/reference/parameters/