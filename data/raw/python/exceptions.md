---
title: Python Exception Handling
domain: Python
source_url: https://docs.python.org/3/tutorial/errors.html
document_type: technical_documentation
version: current
---

# Python Exception Handling

## 1. Introduction to Errors and Exceptions

Errors are problems that occur during program execution or prevent a program from running correctly.

Python errors can broadly be classified into two categories:

1. Syntax errors
2. Exceptions

### Syntax Errors

Syntax errors occur when Python code violates the language's syntax rules.

Example:

```python
if x > 10
    print("Greater than 10")
```

The colon is missing after the condition, so Python raises a `SyntaxError`.

### Exceptions

Exceptions are errors detected during program execution.

Example:

```python
number = 10
result = number / 0
```

This raises a `ZeroDivisionError` because division by zero is not allowed.

## 2. Common Built-in Exceptions

Python provides several built-in exception classes.

| Exception | Description |
|---|---|
| `ZeroDivisionError` | Raised when dividing a number by zero |
| `ValueError` | Raised when an argument has the correct type but an inappropriate value |
| `TypeError` | Raised when an operation or function is applied to an inappropriate type |
| `NameError` | Raised when a local or global name is not found |
| `IndexError` | Raised when a sequence index is outside the valid range |
| `KeyError` | Raised when a dictionary key is not found |
| `AttributeError` | Raised when an attribute reference or assignment fails |
| `FileNotFoundError` | Raised when a requested file or directory does not exist |
| `ImportError` | Raised when an import operation fails |
| `ModuleNotFoundError` | Raised when a module cannot be located |
| `RuntimeError` | Raised when an error does not fall into a more specific category |
| `MemoryError` | Raised when an operation runs out of memory |
| `RecursionError` | Raised when the interpreter detects excessive recursion |

## 3. What is Exception Handling?

Exception handling is the process of detecting and managing exceptions during program execution.

It allows an application to respond to errors gracefully rather than terminating unexpectedly.

Python provides the following keywords for exception handling:

- `try`
- `except`
- `else`
- `finally`
- `raise`

## 4. The `try` and `except` Blocks

The `try` block contains code that may raise an exception.

The `except` block contains code that executes when a matching exception occurs.

Example:

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

Output:

```text
Cannot divide by zero
```

Python executes the `except` block because the statement inside `try` raises a `ZeroDivisionError`.

## 5. Handling Multiple Exceptions

A program can handle different exception types using multiple `except` blocks.

Example:

```python
try:
    number = int(input("Enter a number: "))
    result = 100 / number
    print(result)

except ValueError:
    print("Please enter a valid integer")

except ZeroDivisionError:
    print("Number cannot be zero")
```

Each `except` block handles a specific type of exception.

A tuple can also be used to handle multiple exception types in one block.

```python
try:
    result = int("abc")

except (ValueError, TypeError):
    print("Invalid operation")
```

## 6. Using a General Exception Handler

The base class `Exception` can be used to handle most ordinary application exceptions.

Example:

```python
try:
    result = 10 / 0

except Exception as error:
    print("An error occurred:", error)
```

The `as` keyword stores the exception object in the variable `error`.

Catching `Exception` is useful at application boundaries, but catching overly broad exceptions can hide programming mistakes. Prefer specific exception types whenever possible.

## 7. The `else` Block

The `else` block executes only when the `try` block completes without raising an exception.

Example:

```python
try:
    number = int("100")

except ValueError:
    print("Invalid input")

else:
    print("Conversion successful")
```

Output:

```text
Conversion successful
```

The `else` block helps separate successful execution logic from exception-handling logic.

## 8. The `finally` Block

The `finally` block executes whether or not an exception occurs.

It is commonly used for cleanup operations, such as releasing resources.

Example:

```python
try:
    file = open("sample.txt", "r")
    content = file.read()

except FileNotFoundError:
    print("File not found")

finally:
    print("Execution completed")
```

The `finally` block executes even when the file cannot be opened.

For resource management, Python's `with` statement is generally preferred because it automatically manages cleanup.

## 9. Combining `try`, `except`, `else`, and `finally`

All four blocks can be used together.

Example:

```python
try:
    number = int(input("Enter a number: "))
    result = 100 / number

except ValueError:
    print("Invalid input")

except ZeroDivisionError:
    print("Cannot divide by zero")

else:
    print("Result:", result)

finally:
    print("Program execution completed")
```

Execution order:

1. Python executes the `try` block.
2. If an exception occurs, a matching `except` block executes.
3. If no exception occurs, the `else` block executes.
4. The `finally` block executes in either case.

## 10. Raising Exceptions Using `raise`

The `raise` keyword allows developers to explicitly trigger an exception.

Example:

```python
age = -5

if age < 0:
    raise ValueError("Age cannot be negative")
```

This raises a `ValueError` when the age is negative.

The `raise` statement is useful for validating input and enforcing business rules.

## 11. Creating Custom Exceptions

Python allows developers to define their own exception classes.

Custom exceptions are useful when an application needs to represent domain-specific errors.

A custom exception generally inherits from the built-in `Exception` class.

Example:

```python
class InsufficientBalanceError(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(
            "Insufficient account balance"
        )

    return balance - amount

print(withdraw(1000, 200))
```

If the withdrawal amount exceeds the balance, the function raises `InsufficientBalanceError`.

### Handling a Custom Exception

```python
class InsufficientBalanceError(Exception):
    pass

try:
    raise InsufficientBalanceError("Insufficient balance")

except InsufficientBalanceError as error:
    print(error)
```

Custom exceptions make application errors easier to identify and manage.

## 12. Exception Propagation

Exception propagation occurs when an exception is not handled in the current function and moves up the call stack.

Python searches for a matching exception handler in the calling functions.

Example:

```python
def divide(a, b):
    return a / b

def calculate():
    return divide(10, 0)

try:
    calculate()

except ZeroDivisionError:
    print("Division by zero detected")
```

The exception raised inside `divide()` propagates through `calculate()` until it is handled by the `try` and `except` block.

## 13. Re-raising Exceptions

An exception can be caught and then raised again using `raise`.

This is useful when a function needs to log an error or perform some action before allowing the caller to handle the exception.

Example:

```python
try:
    result = 10 / 0

except ZeroDivisionError:
    print("Logging division error")
    raise
```

Using `raise` without an argument inside an exception handler re-raises the currently handled exception.

## 14. Exception Chaining

Exception chaining preserves the relationship between an original exception and a new exception.

Python supports explicit exception chaining using `raise ... from ...`.

Example:

```python
def process_data():
    try:
        number = int("abc")

    except ValueError as error:
        raise RuntimeError("Data processing failed") from error

try:
    process_data()

except RuntimeError as error:
    print(error)
```

The original `ValueError` is retained as the cause of the `RuntimeError`.

Exception chaining helps developers understand the underlying cause of an application failure.

## 15. Assertions vs Exceptions

Assertions are used to check assumptions during development.

The `assert` statement raises an `AssertionError` if its condition is false.

Example:

```python
age = 25

assert age >= 0, "Age cannot be negative"
```

### Difference Between Assertions and Exceptions

| Assertions | Exceptions |
|---|---|
| Check assumptions and internal conditions | Handle runtime error conditions |
| Commonly used for debugging and development checks | Used for application error handling |
| Can be disabled when Python runs with optimization | Exception handling remains part of normal execution |
| Should not be used for essential input validation | Appropriate for validating external input |

Assertions should not replace proper validation of user input or other conditions that must always be enforced.

## 16. The `with` Statement and Resource Management

The `with` statement is used with context managers to manage resources.

It helps ensure that resources are cleaned up after their use, even if an exception occurs.

Example:

```python
with open("sample.txt", "r") as file:
    content = file.read()
```

The file is automatically closed when execution leaves the `with` block.

This is generally safer and cleaner than manually opening and closing files using `try` and `finally`.

## 17. Best Practices for Exception Handling

- Catch specific exceptions instead of catching every exception indiscriminately.
- Avoid empty `except` blocks.
- Do not silently ignore errors.
- Use meaningful exception messages.
- Create custom exceptions for application-specific failures.
- Use `finally` or context managers for resource cleanup.
- Use exception chaining when translating one exception into another.
- Avoid using exceptions for ordinary control flow.
- Log errors with useful context when appropriate.
- Do not expose sensitive internal details in user-facing error messages.

## 18. Exception Handling in AI and RAG Applications

Exception handling is especially important in AI applications because they interact with files, APIs, databases, and external services.

Examples include:

### Document Loading

A PDF may be missing, corrupted, or inaccessible.

Possible exceptions include `FileNotFoundError` and errors raised by the PDF processing library.

### API Requests

An external API request may fail because of authentication problems, network issues, rate limits, or server errors.

Applications should handle the relevant exceptions raised by their HTTP or API client libraries.

### Embedding Generation

Embedding generation may fail because of invalid input, API errors, or configuration problems.

### Vector Database Operations

A vector database operation may fail because of connection, configuration, or data-related issues.

### Recommended Approach

- Validate inputs before processing.
- Catch relevant exceptions at appropriate application boundaries.
- Log diagnostic information.
- Return clear error messages to users.
- Avoid exposing API keys, credentials, or sensitive internal details.
- Retry only appropriate transient failures, preferably with controlled backoff.

## 19. Key Concepts Summary

| Concept | Description |
|---|---|
| SyntaxError | Error caused by invalid Python syntax |
| Exception | Error detected during program execution |
| `try` | Contains code that may raise an exception |
| `except` | Handles matching exceptions |
| `else` | Executes when the try block succeeds |
| `finally` | Executes during cleanup regardless of success or failure |
| `raise` | Explicitly raises an exception |
| Custom exception | Application-specific exception class |
| Exception propagation | Movement of an unhandled exception up the call stack |
| Exception chaining | Preserves the relationship between related exceptions |
| Assertion | Checks a development-time assumption |
| Context manager | Manages resource setup and cleanup |

## 20. Official References

- Python Tutorial — Errors and Exceptions: https://docs.python.org/3/tutorial/errors.html
- Python Documentation — Built-in Exceptions: https://docs.python.org/3/library/exceptions.html
- Python Documentation — The `raise` Statement: https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement
- Python Documentation — Context Managers: https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers