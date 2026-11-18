---
title: Python Functions
domain: Python
source_url: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
document_type: technical_documentation
version: current
---

# Python Functions

## 1. Introduction to Functions

A function is a reusable block of code designed to perform a specific task.

Functions help organize code into smaller, manageable components. They improve code reusability, readability, and maintainability.

Python provides built-in functions such as `print()`, `len()`, `sum()`, and `type()`.

Python also allows developers to define their own functions using the `def` keyword.

## 2. Defining and Calling a Function

A function is defined using the `def` keyword, followed by the function name and parentheses.

Example:

```python
def greet():
    print("Hello, welcome to Python!")

greet()
```

Output:

```text
Hello, welcome to Python!
```

In this example:
- `def` is the keyword used to define a function.
- `greet` is the function name.
- The function body contains the statements to execute.
- `greet()` calls the function.

A function executes its body when it is called.

## 3. Function Parameters and Arguments

Parameters are variables listed in a function definition.

Arguments are the actual values passed to a function when it is called.

Example:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
```

Here:
- `name` is a parameter.
- `"Alice"` is an argument.

Functions can accept multiple parameters.

```python
def add(a, b):
    print(a + b)

add(10, 20)
```

Output:

```text
30
```

## 4. Types of Function Arguments

Python supports several ways of passing arguments to functions.

### 4.1 Positional Arguments

Positional arguments are assigned to parameters based on their position in the function call.

```python
def employee(name, age):
    print(name, age)

employee("Alice", 25)
```

The first argument is assigned to `name`, and the second is assigned to `age`.

### 4.2 Keyword Arguments

Keyword arguments are passed using parameter names.

```python
def employee(name, age):
    print(name, age)

employee(age=25, name="Alice")
```

Keyword arguments allow arguments to be passed in a different order from the function definition.

### 4.3 Default Arguments

Default arguments allow parameters to have predefined values.

If an argument is not supplied, the default value is used.

```python
def greet(name, message="Welcome"):
    print(message, name)

greet("Alice")
greet("Bob", "Good morning")
```

Output:

```text
Welcome Alice
Good morning Bob
```

Default parameters must follow non-default parameters in a function definition.

### 4.4 Variable-Length Positional Arguments: `*args`

`*args` allows a function to accept a variable number of positional arguments.

The arguments are collected into a tuple.

```python
def calculate_sum(*args):
    return sum(args)

print(calculate_sum(10, 20))
print(calculate_sum(10, 20, 30, 40))
```

Output:

```text
30
100
```

### 4.5 Variable-Length Keyword Arguments: `**kwargs`

`**kwargs` allows a function to accept a variable number of keyword arguments.

The arguments are collected into a dictionary.

```python
def display_details(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

display_details(name="Alice", age=25, city="Kolkata")
```

Output:

```text
name Alice
age 25
city Kolkata
```

### 4.6 Combining Different Argument Types

A function can combine regular parameters, default parameters, `*args`, and `**kwargs`.

```python
def example(a, b=10, *args, **kwargs):
    print(a)
    print(b)
    print(args)
    print(kwargs)

example(5, 20, 30, 40, city="Kolkata")
```

Output:

```text
5
20
(30, 40)
{'city': 'Kolkata'}
```

## 5. Return Statement

The `return` statement sends a result back from a function to the caller.

A function can return a value that can be stored in a variable or used in another expression.

```python
def add(a, b):
    return a + b

result = add(10, 20)
print(result)
```

Output:

```text
30
```

### Difference Between `print()` and `return`

- `print()` displays information on the screen.
- `return` sends a value back to the calling code.
- A returned value can be reused in calculations or passed to another function.

Example:

```python
def square(number):
    return number * number

result = square(5)
print(result + 10)
```

Output:

```text
35
```

If a function does not explicitly return a value, Python returns `None` by default.

## 6. Returning Multiple Values

Python allows a function to return multiple values.

These values are returned together as a tuple and can be unpacked into separate variables.

```python
def calculate(a, b):
    total = a + b
    difference = a - b
    return total, difference

sum_result, difference_result = calculate(20, 10)

print(sum_result)
print(difference_result)
```

Output:

```text
30
10
```

## 7. Lambda Functions

A lambda function is a small anonymous function defined using the `lambda` keyword.

Lambda functions can contain only a single expression.

Syntax:

```python
lambda arguments: expression
```

Example:

```python
square = lambda x: x * x

print(square(5))
```

Output:

```text
25
```

Lambda functions are commonly used when a short function is needed temporarily.

### Lambda with Multiple Arguments

```python
add = lambda a, b: a + b

print(add(10, 20))
```

Output:

```text
30
```

### Lambda with `map()`

The `map()` function applies a function to every item in an iterable.

```python
numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x ** 2, numbers))

print(squares)
```

Output:

```text
[1, 4, 9, 16, 25]
```

### Lambda with `filter()`

The `filter()` function selects elements from an iterable based on a condition.

```python
numbers = [1, 2, 3, 4, 5, 6]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print(even_numbers)
```

Output:

```text
[2, 4, 6]
```

### Lambda with `sorted()`

Lambda functions can be used as sorting keys.

```python
employees = [
    {"name": "Alice", "salary": 50000},
    {"name": "Bob", "salary": 70000},
    {"name": "Charlie", "salary": 60000}
]

sorted_employees = sorted(
    employees,
    key=lambda employee: employee["salary"]
)

print(sorted_employees)
```

This sorts employees by salary in ascending order.

## 8. Variable Scope

Variable scope determines where a variable can be accessed in a program.

Python follows the LEGB rule when resolving variable names.

LEGB stands for:

- Local
- Enclosing
- Global
- Built-in

### 8.1 Local Scope

A variable created inside a function belongs to the local scope.

It can generally be accessed only within that function.

```python
def display():
    message = "Hello"
    print(message)

display()
```

### 8.2 Global Scope

A variable defined outside all functions belongs to the global scope.

It can be accessed from functions unless a local variable with the same name takes precedence.

```python
message = "Hello from global scope"

def display():
    print(message)

display()
```

### 8.3 The `global` Keyword

The `global` keyword allows a function to reassign a variable defined in the global scope.

```python
count = 10

def update_count():
    global count
    count = 20

update_count()

print(count)
```

Output:

```text
20
```

### 8.4 The `nonlocal` Keyword

The `nonlocal` keyword allows a nested function to reassign a variable from its nearest enclosing function scope, excluding the global scope.

```python
def outer():
    count = 10

    def inner():
        nonlocal count
        count = 20

    inner()
    print(count)

outer()
```

Output:

```text
20
```

## 9. Recursive Functions

A recursive function is a function that calls itself.

Every recursive function should have a base case that stops further recursive calls.

Example: Factorial

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1

    return n * factorial(n - 1)

print(factorial(5))
```

Output:

```text
120
```

The base case prevents infinite recursion.

Python has a recursion depth limit. Excessive recursive calls can raise a `RecursionError`.

## 10. Docstrings

A docstring is a string literal used to document a function, class, or module.

It is generally placed immediately after the function definition.

```python
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.

    Parameters:
        length: Length of the rectangle.
        width: Width of the rectangle.

    Returns:
        Area of the rectangle.
    """
    return length * width

print(calculate_area(10, 5))
```

Docstrings can be accessed using the `__doc__` attribute.

```python
print(calculate_area.__doc__)
```

## 11. First-Class Functions

In Python, functions are first-class objects.

This means functions can be:
- Assigned to variables.
- Passed as arguments to other functions.
- Returned from other functions.
- Stored in data structures.

Example:

```python
def greet():
    return "Hello"

message_function = greet

print(message_function())
```

Output:

```text
Hello
```

## 12. Higher-Order Functions

A higher-order function is a function that accepts another function as an argument or returns a function.

Example:

```python
def apply_operation(func, a, b):
    return func(a, b)

def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

print(apply_operation(add, 10, 20))
print(apply_operation(multiply, 10, 20))
```

Output:

```text
30
200
```

Functions such as `map()`, `filter()`, and `sorted()` can work with other functions.

## 13. Function Annotations

Function annotations allow developers to attach metadata to parameters and return values.

Type hints are commonly used to indicate expected data types.

```python
def add(a: int, b: int) -> int:
    return a + b
```

Here:
- `a: int` indicates the expected type of `a`.
- `b: int` indicates the expected type of `b`.
- `-> int` indicates the expected return type.

Python does not automatically enforce these annotations at runtime.

## 14. Best Practices for Writing Functions

- Use descriptive function names.
- Keep functions focused on a single responsibility.
- Avoid unnecessarily long functions.
- Use parameters instead of relying excessively on global variables.
- Return values when results need to be reused.
- Add docstrings to explain important functions.
- Avoid mutable default argument values such as lists and dictionaries unless their shared behavior is intentional.
- Write functions that are easy to test and maintain.

## 15. Functions: Key Concepts Summary

| Concept | Description |
|---|---|
| `def` | Keyword used to define a function |
| Parameter | Variable in a function definition |
| Argument | Value passed during a function call |
| `return` | Sends a value back to the caller |
| `*args` | Collects variable positional arguments into a tuple |
| `**kwargs` | Collects variable keyword arguments into a dictionary |
| Lambda | Small anonymous function |
| Recursion | A function calling itself |
| Docstring | Documentation string for a function |
| Scope | Determines where variables can be accessed |
| Higher-order function | Accepts or returns another function |
| Annotation | Metadata attached to parameters or return values |

## 16. Official References

- Python Tutorial — Defining Functions: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Python Documentation — Function Definitions: https://docs.python.org/3/reference/compound_stmts.html#function-definitions
- Python Documentation — Expressions and Lambda: https://docs.python.org/3/reference/expressions.html#lambda