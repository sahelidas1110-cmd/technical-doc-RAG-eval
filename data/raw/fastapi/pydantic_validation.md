# Pydantic Validation in FastAPI

## 1. Introduction

Pydantic is a Python data validation library used extensively with FastAPI.

It helps ensure that data entering an application follows the expected structure, types, and validation rules.

FastAPI uses Pydantic models to:

- Validate incoming request bodies.
- Convert compatible input values into declared Python types.
- Enforce field-level constraints.
- Generate JSON Schemas for API documentation.
- Return structured validation errors when input is invalid.

For example, an API might expect a product with the following fields:

```json
{
    "name": "Laptop",
    "price": 75000,
    "quantity": 5
}
```

Pydantic can validate that:

- `name` is a string.
- `price` is a positive number.
- `quantity` is a non-negative integer.

## 2. Pydantic BaseModel

Pydantic models are Python classes that inherit from `BaseModel`.

Example:

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    quantity: int
```

Create an instance:

```python
product = Product(
    name="Laptop",
    price=75000,
    quantity=5
)

print(product)
```

Pydantic validates the supplied values and creates a model instance.

### Accessing Model Attributes

```python
print(product.name)
print(product.price)
print(product.quantity)
```

### Converting a Model into a Dictionary

Pydantic v2 provides `model_dump()`:

```python
product_data = product.model_dump()

print(product_data)
```

Output:

```python
{
    "name": "Laptop",
    "price": 75000.0,
    "quantity": 5
}
```

## 3. Field Validation Using Field

Pydantic provides `Field` to define constraints and metadata for individual fields.

Example:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
```

Explanation:

| Constraint | Meaning |
|---|---|
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `gt` | Greater than |
| `ge` | Greater than or equal to |
| `lt` | Less than |
| `le` | Less than or equal to |
| `multiple_of` | Value must be a multiple of a specified number |
| `pattern` | String must match a regular expression |

Example:

```python
product = Product(
    name="Laptop",
    price=75000,
    quantity=5
)
```

Invalid input:

```python
product = Product(
    name="PC",
    price=-100,
    quantity=-5
)
```

Pydantic raises a `ValidationError` because multiple field constraints are violated.

## 4. Required and Optional Fields

A field is required when it has no default value.

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    age: int | None = None
```

Here:

- `username` is required.
- `email` is required.
- `age` is optional and defaults to `None`.

Example:

```python
user = User(
    username="john",
    email="john@example.com"
)
```

Important distinction:

```python
age: int | None
```

This allows `None` as a value but does not make the field optional. Without a default, the field is still required.

```python
age: int | None = None
```

This makes the field optional.

## 5. Custom Field Validation Using field_validator

Sometimes built-in constraints are not sufficient.

For example, an application might require a username to contain only letters and numbers.

Pydantic provides the `@field_validator` decorator for custom field-level validation.

Example:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:

        if not value.isalnum():
            raise ValueError(
                "Username must contain only letters and numbers"
            )

        return value
```

Explanation:

- `@field_validator("username")` specifies the field to validate.
- `@classmethod` defines the validator as a class method.
- The validator receives the field value.
- `ValueError` indicates invalid input.
- The validated value must be returned.

Valid input:

```python
user = User(username="john123")
```

Invalid input:

```python
user = User(username="john@123")
```

The invalid input raises a validation error.

## 6. Field Validator Modes

Pydantic v2 supports four field validator modes.

| Mode | Purpose |
|---|---|
| `after` | Runs after Pydantic's internal validation |
| `before` | Runs before Pydantic's internal validation |
| `plain` | Performs validation itself and terminates the normal validation process |
| `wrap` | Can run logic before and after the normal validation handler |

### 6.1 After Validator

An after validator receives a value after Pydantic has performed its normal type validation.

Example:

```python
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    price: float

    @field_validator("price", mode="after")
    @classmethod
    def validate_price(cls, value: float) -> float:

        if value <= 0:
            raise ValueError("Price must be positive")

        return value
```

After validators are generally easier to implement because the value has already passed Pydantic's normal type validation.

### 6.2 Before Validator

A before validator runs before Pydantic performs its internal type validation.

It receives the raw input, which can be of different Python types.

Example:

```python
from typing import Any
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: Any) -> Any:

        if isinstance(value, str):
            return value.strip().lower()

        return value
```

Input:

```python
user = User(username="  JOHN  ")

print(user.username)
```

Output:

```text
john
```

The validator normalizes the input before Pydantic completes its normal validation.

### 6.3 Plain Validator

A plain validator takes responsibility for validation and terminates the normal validation process for that field.

Pydantic does not continue its usual internal validation against the declared field type after the plain validator returns.

Example:

```python
from typing import Any
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    price: int

    @field_validator("price", mode="plain")
    @classmethod
    def validate_price(cls, value: Any) -> Any:

        if isinstance(value, int) and value > 0:
            return value

        raise ValueError("Price must be a positive integer")
```

Plain validators should be used carefully because they take responsibility for type and value validation.

### 6.4 Wrap Validator

A wrap validator provides control over the normal validation process.

It receives a handler that can execute Pydantic's standard validation.

Example:

```python
from typing import Any
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidatorFunctionWrapHandler,
    field_validator
)

class Product(BaseModel):
    name: str = Field(max_length=10)

    @field_validator("name", mode="wrap")
    @classmethod
    def validate_name(
        cls,
        value: Any,
        handler: ValidatorFunctionWrapHandler
    ) -> str:

        try:
            return handler(value)

        except ValidationError:
            return handler(str(value)[:10])
```

This example attempts normal validation first. If validation fails because the string is too long, it retries with a truncated value.

Wrap validators are useful when custom logic needs to surround or control the normal validation process.

## 7. Applying One Validator to Multiple Fields

A single field validator can be applied to multiple fields.

Example:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    first_name: str
    last_name: str

    @field_validator("first_name", "last_name")
    @classmethod
    def capitalize_names(cls, value: str) -> str:
        return value.capitalize()
```

Input:

```python
user = User(
    first_name="john",
    last_name="doe"
)
```

Output:

```python
first_name="John" last_name="Doe"
```

This avoids writing separate validation functions for fields that share the same rule.

## 8. Model-Level Validation Using model_validator

Field validators work on individual fields.

Sometimes validation requires comparing multiple fields.

For example, a registration API may require the password and password confirmation to match.

Pydantic provides `@model_validator` for validating the entire model.

Example:

```python
from typing_extensions import Self
from pydantic import BaseModel, model_validator

class UserRegistration(BaseModel):
    username: str
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self) -> Self:

        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self
```

Input:

```python
user = UserRegistration(
    username="john",
    password="password123",
    confirm_password="password123"
)
```

The validation succeeds because both passwords match.

If they differ, Pydantic raises a validation error.

### Model Validator Modes

Pydantic supports three model validator modes:

| Mode | Purpose |
|---|---|
| `before` | Validates or modifies raw input before model creation |
| `after` | Validates the fully validated model instance |
| `wrap` | Controls the complete model validation process |

An after model validator receives the validated model instance and should return that instance.

## 9. Before Model Validation

A before model validator receives raw input before the model is constructed.

Example:

```python
from typing import Any
from pydantic import BaseModel, model_validator

class User(BaseModel):
    username: str

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Any) -> Any:

        if isinstance(data, dict):
            if "password" in data:
                raise ValueError(
                    "Password should not be included in this model"
                )

        return data
```

Before model validators are useful when you need to inspect, reject, or normalize the incoming object before individual fields are validated.

## 10. Pydantic Validation Errors

When data does not satisfy a model's validation rules, Pydantic raises a `ValidationError`.

Example:

```python
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float

try:
    product = Product(
        name="Laptop",
        price="expensive"
    )

except ValidationError as error:
    print(error)
```

The error describes:

- Which field failed validation.
- What type of validation failed.
- The invalid input value.
- The expected input type or constraint.

### Extracting Error Details

The `errors()` method returns structured error details.

```python
try:
    Product(name="Laptop", price="expensive")

except ValidationError as error:
    print(error.errors())
```

Other useful methods include:

```python
error.json()
error.error_count()
```

These are useful when logging, inspecting, or formatting validation failures.

## 11. Handling Validation Errors in FastAPI

FastAPI automatically handles request validation errors raised when incoming data does not match the declared request model.

Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)

@app.post("/products/")
async def create_product(product: Product):
    return product
```

Valid request:

```json
{
    "name": "Laptop",
    "price": 75000
}
```

Invalid request:

```json
{
    "name": "PC",
    "price": -100
}
```

FastAPI returns HTTP status code `422` for request validation errors by default.

The response contains structured details identifying the invalid fields.

For custom error responses, FastAPI provides exception handlers. These are covered in more detail in the API error-handling and application design context.

## 12. Strict Mode

By default, Pydantic may convert compatible input values into the declared type.

For example, some input values can be converted from strings into numbers.

Strict mode can be used when an application should reject inputs that do not already have the expected type.

Example:

```python
from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str
    price: float
```

With strict validation enabled, values that would otherwise be coerced may be rejected.

Strict behavior can vary by type and validation context, so test the exact input formats your API accepts.

## 13. Controlling Extra Fields

By default, Pydantic models ignore extra input fields that are not declared in the model.

You can change this behavior using `ConfigDict`.

### Ignore Extra Fields

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")

    username: str
    email: str
```

### Forbid Extra Fields

```python
class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    email: str
```

With `extra="forbid"`, an incoming field that is not declared in the model causes a validation error.

### Allow Extra Fields

```python
class User(BaseModel):
    model_config = ConfigDict(extra="allow")

    username: str
    email: str
```

With `extra="allow"`, additional input fields are accepted and retained.

| Configuration | Behavior |
|---|---|
| `ignore` | Ignore extra fields |
| `forbid` | Reject extra fields |
| `allow` | Accept and retain extra fields |

For APIs with strict request contracts, `extra="forbid"` can help detect unexpected input.

## 14. Nested Model Validation

Pydantic supports nested models, allowing complex JSON structures to be validated.

Example:

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class User(BaseModel):
    username: str
    email: str
    address: Address
```

Request data:

```python
user = User(
    username="john",
    email="john@example.com",
    address={
        "city": "Kolkata",
        "country": "India"
    }
)
```

Pydantic validates the nested `address` object using the `Address` model.

This is useful for APIs that accept structured information containing multiple related objects.

## 15. Reusable Validation with Annotated

Pydantic supports reusable validators using `Annotated` and validator functions such as `AfterValidator`.

Example:

```python
from typing import Annotated
from pydantic import AfterValidator, BaseModel

def validate_even_number(value: int) -> int:

    if value % 2 != 0:
        raise ValueError("Number must be even")

    return value

EvenNumber = Annotated[int, AfterValidator(validate_even_number)]

class Product(BaseModel):
    quantity: EvenNumber
```

The `EvenNumber` type can be reused in multiple models.

```python
class Order(BaseModel):
    quantity: EvenNumber
```

This helps avoid repeating the same validation logic.

## 16. Pydantic v1 vs Pydantic v2

Pydantic v2 introduced important changes to validation APIs.

| Pydantic v1 | Pydantic v2 |
|---|---|
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `class Config` | `model_config = ConfigDict(...)` |
| `parse_obj()` | `model_validate()` |

For new projects, use Pydantic v2 syntax unless you are maintaining an older application.

## 17. Relevance to AI and RAG Applications

Pydantic validation is especially useful when deploying AI and RAG applications through FastAPI.

Consider a RAG API that accepts a question and retrieval configuration.

```python
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)
```

This model ensures:

- The question is not empty or too short.
- The question does not exceed the configured length.
- The number of retrieved chunks is between 1 and 20.
- A default retrieval count is used when the client does not supply one.

The FastAPI endpoint can use this model:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/search/")
async def search_documents(request: SearchRequest):

    return {
        "question": request.question,
        "top_k": request.top_k
    }
```

In a production RAG application, the validated input would be passed to the retrieval pipeline.

This prevents malformed input from reaching the retrieval and generation components.

Pydantic can also validate structured LLM outputs when an application expects the model to return data in a defined schema.

## 18. Best Practices

1. Use Pydantic models for structured input validation.
2. Prefer `Field` for straightforward field constraints.
3. Use `field_validator` for custom field-level validation.
4. Use `model_validator` when validation depends on multiple fields.
5. Prefer after validators when possible because they operate on values that have passed normal type validation.
6. Use before validators when raw input needs normalization or preprocessing.
7. Use strict mode when implicit type conversion is not acceptable.
8. Consider `extra="forbid"` for APIs with strict request contracts.
9. Reuse common validation logic through `Annotated` types.
10. Avoid exposing internal exception details or sensitive information in production error responses.

## 19. Official References

- Pydantic — Models: https://docs.pydantic.dev/latest/concepts/models/
- Pydantic — Fields: https://docs.pydantic.dev/latest/concepts/fields/
- Pydantic — Validators: https://docs.pydantic.dev/latest/concepts/validators/
- Pydantic — Configuration: https://docs.pydantic.dev/latest/concepts/config/
- Pydantic — Strict Mode: https://docs.pydantic.dev/latest/concepts/strict_mode/
- Pydantic — Validation Errors: https://docs.pydantic.dev/latest/errors/errors/
- FastAPI — Handling Errors: https://fastapi.tiangolo.com/tutorial/handling-errors/