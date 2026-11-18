---
title: Python Decorators
domain: Python
source_url: https://docs.python.org/3/glossary.html#term-decorator
document_type: technical_documentation
version: current
---

# Python Decorators

## 1. Introduction to Decorators

A decorator is a callable that takes another function or class as an argument and returns a modified or wrapped callable.

Decorators allow developers to extend the behavior of existing functions or classes without directly modifying their original implementation.

Decorators are widely used in Python frameworks and libraries.

Common applications include:

- Logging
- Authentication and authorization
- Performance measurement
- Caching
- Input validation
- Access control
- Route registration in web frameworks

## 2. Understanding Functions as First-Class Objects

In Python, functions are first-class objects.

This means functions can be:
- Assigned to variables.
- Passed as arguments to other functions.
- Returned from other functions.
- Stored in data structures.

Example:

```python
def greet():
    return "Hello!"

message_function = greet

print(message_function())
```

Output:

```text
Hello!
```

This feature makes decorators possible.

## 3. Functions as Arguments

A function can accept another function as an argument.

Example:

```python
def greet():
    return "Hello!"

def execute_function(func):
    return func()

print(execute_function(greet))
```

Output:

```text
Hello!
```

Here, `greet` is passed as an argument to `execute_function`.

Notice that `greet` is passed without parentheses because the function itself is being passed rather than its return value.

## 4. Understanding Nested Functions

A nested function is a function defined inside another function.

Example:

```python
def outer_function():

    def inner_function():
        print("Inside inner function")

    inner_function()

outer_function()
```

Output:

```text
Inside inner function
```

Nested functions are commonly used when implementing decorators.

## 5. Creating a Simple Decorator

A decorator can be implemented using a wrapper function.

The wrapper function executes additional logic before or after calling the original function.

Example:

```python
def my_decorator(func):

    def wrapper():
        print("Before function execution")

        func()

        print("After function execution")

    return wrapper


def greet():
    print("Hello!")

decorated_greet = my_decorator(greet)

decorated_greet()
```

Output:

```text
Before function execution
Hello!
After function execution
```

In this example:

- `my_decorator` is the decorator function.
- `func` represents the original function.
- `wrapper` adds additional behavior.
- `return wrapper` returns the modified callable.

## 6. The `@` Decorator Syntax

Python provides a convenient syntax for applying decorators using the `@` symbol.

Example:

```python
def my_decorator(func):

    def wrapper():
        print("Before execution")

        func()

        print("After execution")

    return wrapper


@my_decorator
def greet():
    print("Hello!")

greet()
```

The following syntax:

```python
@my_decorator
def greet():
    print("Hello!")
```

is equivalent to:

```python
def greet():
    print("Hello!")

greet = my_decorator(greet)
```

The `@` syntax makes decorators easier to read and use.

## 7. Decorators with Function Arguments

A decorator should support the arguments accepted by the original function.

A common approach is to use `*args` and `**kwargs` in the wrapper function.

Example:

```python
def my_decorator(func):

    def wrapper(*args, **kwargs):
        print("Function execution started")

        result = func(*args, **kwargs)

        print("Function execution completed")

        return result

    return wrapper


@my_decorator
def add(a, b):
    return a + b

print(add(10, 20))
```

Output:

```text
Function execution started
Function execution completed
30
```

Here:
- `*args` collects positional arguments.
- `**kwargs` collects keyword arguments.
- `func(*args, **kwargs)` forwards them to the original function.
- `return result` preserves the original function's return value.

## 8. Using `functools.wraps`

When a decorator replaces a function with a wrapper, the resulting callable may expose the wrapper's metadata instead of the original function's metadata.

Python provides `functools.wraps` to preserve important metadata such as the original function's name and docstring.

Example:

```python
from functools import wraps

def my_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Executing function")

        return func(*args, **kwargs)

    return wrapper


@my_decorator
def greet():
    """Display a greeting."""
    print("Hello!")

greet()

print(greet.__name__)
print(greet.__doc__)
```

Using `@wraps(func)` is a recommended practice when writing decorators.

## 9. Decorators with Return Values

Decorators should preserve the return value of the original function whenever the decorator is not intended to change it.

Example:

```python
def log_decorator(func):

    def wrapper(*args, **kwargs):
        print("Calling function")

        result = func(*args, **kwargs)

        print("Function completed")

        return result

    return wrapper


@log_decorator
def multiply(a, b):
    return a * b

result = multiply(5, 4)

print(result)
```

Output:

```text
Calling function
Function completed
20
```

## 10. Decorators with Their Own Arguments

A decorator can also accept arguments.

This requires an additional outer function.

Example:

```python
from functools import wraps

def repeat(times):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(3)
def greet():
    print("Hello!")

greet()
```

Output:

```text
Hello!
Hello!
Hello!
```

In this example:

- `repeat()` is the decorator factory.
- `decorator()` receives the original function.
- `wrapper()` controls repeated execution.
- `@repeat(3)` configures the decorator.

## 11. Multiple Decorators

Python allows multiple decorators to be applied to a single function.

Example:

```python
def decorator_one(func):

    def wrapper():
        print("Decorator One - Before")
        func()
        print("Decorator One - After")

    return wrapper


def decorator_two(func):

    def wrapper():
        print("Decorator Two - Before")
        func()
        print("Decorator Two - After")

    return wrapper


@decorator_one
@decorator_two
def greet():
    print("Hello!")

greet()
```

Decorators are applied from the bottom upward.

The example is equivalent to:

```python
greet = decorator_one(decorator_two(greet))
```

The order of decorators matters because each decorator wraps the result of the decorator below it.

## 12. Common Built-in Decorators

Python provides several commonly used decorators.

### 12.1 `@staticmethod`

Defines a method that does not automatically receive `self` or `cls`.

```python
class Calculator:

    @staticmethod
    def add(a, b):
        return a + b

print(Calculator.add(10, 20))
```

### 12.2 `@classmethod`

Defines a method that receives the class as its first argument.

```python
class Employee:
    company = "ABC Ltd"

    @classmethod
    def change_company(cls, name):
        cls.company = name

Employee.change_company("XYZ Ltd")

print(Employee.company)
```

### 12.3 `@property`

Allows a method to be accessed like an attribute.

```python
class Employee:

    def __init__(self, salary):
        self._salary = salary

    @property
    def salary(self):
        return self._salary

employee = Employee(50000)

print(employee.salary)
```

## 13. Class Decorators

Decorators can also be applied to classes.

A class decorator receives a class as an argument and returns a class or another callable.

Example:

```python
def add_class_attribute(cls):
    cls.category = "Employee"
    return cls


@add_class_attribute
class Employee:
    pass


print(Employee.category)
```

Output:

```text
Employee
```

Class decorators are useful for modifying or registering classes.

## 14. Decorators for Logging

Decorators can be used to log function execution.

Example:

```python
from functools import wraps

def logging_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print(f"Calling {func.__name__}")

        result = func(*args, **kwargs)

        print(f"Completed {func.__name__}")

        return result

    return wrapper


@logging_decorator
def calculate_sum(a, b):
    return a + b


print(calculate_sum(10, 20))
```

This decorator adds logging behavior without modifying the original function.

## 15. Decorators for Execution Time Measurement

Decorators can measure how long a function takes to execute.

Example:

```python
import time
from functools import wraps

def execution_time(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()

        print(
            f"Execution time: {end_time - start_time:.6f} seconds"
        )

        return result

    return wrapper


@execution_time
def calculate():
    time.sleep(1)
    return "Completed"


print(calculate())
```

The decorator measures the execution duration without changing the original function's implementation.

## 16. Decorators for Caching

Caching stores previously computed results so that repeated calls can avoid performing the same computation again.

Python provides `functools.lru_cache` for caching function results.

Example:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):

    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(10))
```

The `lru_cache` decorator caches results and can improve performance for functions with repeated inputs.

## 17. Decorators in FastAPI

FastAPI uses decorators to register functions as API endpoints.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}
```

The `@app.get("/")` decorator registers the `home()` function as a handler for HTTP GET requests to the root endpoint.

Other commonly used FastAPI route decorators include:

- `@app.post()`
- `@app.put()`
- `@app.patch()`
- `@app.delete()`

Decorators allow framework functionality to be attached to ordinary Python functions.

## 18. Decorators in Machine Learning and AI Applications

Decorators can be useful in AI and machine learning applications.

Examples include:

### Logging

Record function execution details in data preprocessing and model inference pipelines.

### Performance Monitoring

Measure the execution time of model prediction and data-processing functions.

### Caching

Cache expensive or repeated computations where caching is appropriate.

### Authentication

Protect application functions by checking whether a user has the required permissions.

### API Endpoint Registration

Frameworks such as FastAPI use decorators to register endpoint functions.

### Retry Logic

A decorator can implement controlled retries for operations that may experience temporary failures, such as network requests.

## 19. Best Practices

- Use decorators when behavior needs to be reused across multiple functions.
- Keep decorators focused on a single responsibility.
- Use `functools.wraps` to preserve function metadata.
- Forward arguments using `*args` and `**kwargs` when appropriate.
- Preserve the original return value unless intentionally changing it.
- Be careful when stacking multiple decorators because order affects behavior.
- Avoid unnecessary layers of decorators that make code difficult to debug.
- Document decorators that significantly change function behavior.

## 20. Key Concepts Summary

| Concept | Description |
|---|---|
| Decorator | Callable that modifies or wraps another callable |
| Wrapper function | Function that adds behavior around another function |
| `@` syntax | Convenient way to apply a decorator |
| `*args` | Collects positional arguments |
| `**kwargs` | Collects keyword arguments |
| `functools.wraps` | Preserves important function metadata |
| Decorator factory | Function that creates a configured decorator |
| Class decorator | Decorator applied to a class |
| `@staticmethod` | Defines a static method |
| `@classmethod` | Defines a class method |
| `@property` | Provides attribute-style access to a method |
| `lru_cache` | Decorator for caching function results |

## 21. Official References

- Python Glossary — Decorator: https://docs.python.org/3/glossary.html#term-decorator
- Python Documentation — Function Definitions: https://docs.python.org/3/reference/compound_stmts.html#function-definitions
- Python Documentation — `functools`: https://docs.python.org/3/library/functools.html
- Python Documentation — `time`: https://docs.python.org/3/library/time.html
- FastAPI Documentation — First Steps: https://fastapi.tiangolo.com/tutorial/first-steps/