---
title: Python Iterators and Generators
domain: Python
source_url: https://docs.python.org/3/tutorial/classes.html#iterators
document_type: technical_documentation
version: current
---

# Python Iterators and Generators

## 1. Introduction to Iteration

Iteration is the process of accessing elements from a collection or sequence one at a time.

Python supports iteration through objects such as:
- Lists
- Tuples
- Strings
- Dictionaries
- Sets
- Files

Example:

```python
numbers = [10, 20, 30, 40]

for number in numbers:
    print(number)
```

The `for` loop retrieves each element from the iterable and executes the loop body.

## 2. What is an Iterable?

An iterable is an object that can return its elements one at a time.

An object is generally iterable if it implements the `__iter__()` method, or the sequence protocol through `__getitem__()`.

Examples of iterables include:
- Lists
- Tuples
- Strings
- Dictionaries
- Sets
- Range objects

Example:

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

A list is an iterable because Python can retrieve its elements one at a time.

## 3. What is an Iterator?

An iterator is an object that represents a stream of data.

It returns elements one at a time and maintains its current iteration state.

An iterator implements two methods:

- `__iter__()`: Returns the iterator object itself.
- `__next__()`: Returns the next element.

When no more elements are available, `__next__()` raises `StopIteration`.

## 4. Difference Between Iterable and Iterator

| Iterable | Iterator |
|---|---|
| Represents a collection or source of elements | Represents a stream of elements |
| Can be passed to `iter()` | Can be passed to `next()` |
| May create a new iterator when iterated over | Maintains iteration state |
| Examples: list, tuple, string | Examples: list iterator, generator |

A list is an iterable, but it is not itself an iterator.

Example:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
10
20
30
```

## 5. The `iter()` Function

The built-in `iter()` function returns an iterator from an iterable.

Syntax:

```python
iterator = iter(iterable)
```

Example:

```python
fruits = ["apple", "banana", "orange"]

fruit_iterator = iter(fruits)

print(type(fruit_iterator))
```

The returned object can be consumed using `next()`.

## 6. The `next()` Function

The built-in `next()` function retrieves the next item from an iterator.

Example:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Calling `next()` after all elements have been consumed raises `StopIteration`.

Example:

```python
numbers = [10, 20]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))

print(next(iterator))
```

The third call raises `StopIteration` because there are no more elements.

### Using a Default Value with `next()`

The `next()` function accepts an optional default value.

If the iterator is exhausted, Python returns the default instead of raising `StopIteration`.

```python
numbers = [10, 20]

iterator = iter(numbers)

print(next(iterator, "No more elements"))
print(next(iterator, "No more elements"))
print(next(iterator, "No more elements"))
```

Output:

```text
10
20
No more elements
```

## 7. How a `for` Loop Uses Iterators

Python's `for` loop internally uses the iterator protocol.

Conceptually, the following code:

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Works similarly to:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

while True:
    try:
        number = next(iterator)
        print(number)

    except StopIteration:
        break
```

The loop stops automatically when the iterator raises `StopIteration`.

## 8. Creating a Custom Iterator

Developers can create their own iterator classes by implementing `__iter__()` and `__next__()`.

Example:

```python
class CountUp:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            value = self.current
            self.current += 1
            return value

        raise StopIteration

counter = CountUp(5)

for number in counter:
    print(number)
```

Output:

```text
1
2
3
4
5
```

The iterator maintains its state using the `current` attribute.

## 9. What is a Generator?

A generator is a special type of iterator that produces values one at a time.

Generators are created using:
- Generator functions with the `yield` keyword.
- Generator expressions.

Generators are useful when working with large data because they do not need to store all generated values in memory simultaneously.

## 10. Generator Functions

A generator function is a function that contains the `yield` keyword.

Unlike a regular function that returns and completes, a generator function produces a generator object and suspends its execution whenever it reaches `yield`.

Example:

```python
def generate_numbers():
    yield 10
    yield 20
    yield 30

numbers = generate_numbers()

print(next(numbers))
print(next(numbers))
print(next(numbers))
```

Output:

```text
10
20
30
```

Each call to `next()` resumes execution until the next `yield` statement.

## 11. Understanding the `yield` Keyword

The `yield` keyword returns a value from a generator while preserving its execution state.

When the generator is resumed, execution continues immediately after the previous `yield`.

Example:

```python
def generate_values():
    print("First execution")
    yield 1

    print("Second execution")
    yield 2

    print("Third execution")
    yield 3

generator = generate_values()

print(next(generator))
print(next(generator))
print(next(generator))
```

The function does not execute all statements at once. It pauses and resumes as values are requested.

### Difference Between `return` and `yield`

| `return` | `yield` |
|---|---|
| Returns a value and exits the function | Produces a value and suspends execution |
| A regular function completes when it returns | A generator can resume after yielding |
| Does not preserve function execution state after returning | Preserves generator execution state |
| A function can return a single result or object | A generator can produce a sequence of values |

## 12. Generator Expressions

A generator expression creates a generator using a compact expression.

Its syntax resembles a list comprehension but uses parentheses instead of square brackets.

Example:

```python
numbers = (x * x for x in range(5))

print(next(numbers))
print(next(numbers))
```

Output:

```text
0
1
```

### List Comprehension vs Generator Expression

List comprehension:

```python
squares = [x * x for x in range(5)]
```

Generator expression:

```python
squares = (x * x for x in range(5))
```

| List Comprehension | Generator Expression |
|---|---|
| Creates a list | Creates a generator object |
| Generates all values immediately | Generates values when requested |
| Stores generated elements in memory | Does not store the entire generated sequence |
| Useful when all results are needed | Useful for lazy processing |

## 13. Lazy Evaluation

Lazy evaluation means that values are computed only when they are requested.

Generators support lazy evaluation.

Example:

```python
def generate_squares(limit):
    for number in range(limit):
        yield number * number

squares = generate_squares(1000000)

print(next(squares))
print(next(squares))
print(next(squares))
```

Only the requested values are generated.

Lazy evaluation can reduce memory usage when processing large sequences.

## 14. Memory Efficiency of Generators

Generators are useful for processing large datasets because they generate values on demand.

Example using a list:

```python
numbers = [number * number for number in range(1000000)]
```

This creates and stores a list containing one million values.

Example using a generator:

```python
numbers = (number * number for number in range(1000000))
```

This creates a generator that produces values when requested.

Generators can reduce memory consumption when the entire sequence does not need to be stored.

Actual memory and performance benefits depend on the workload and how the generated values are consumed.

## 15. Generator with File Processing

Generators are useful when reading large files line by line.

Example:

```python
def read_large_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()

for line in read_large_file("large_file.txt"):
    print(line)
```

This approach avoids loading the entire file into memory.

The file remains open while the generator is being iterated and is closed when the loop completes normally or the generator is closed.

## 16. Generator Pipelines

Multiple generators can be combined to build processing pipelines.

Example:

```python
def generate_numbers():
    for number in range(1, 11):
        yield number

def filter_even(numbers):
    for number in numbers:
        if number % 2 == 0:
            yield number

def square_numbers(numbers):
    for number in numbers:
        yield number * number

numbers = generate_numbers()
even_numbers = filter_even(numbers)
squared_numbers = square_numbers(even_numbers)

for value in squared_numbers:
    print(value)
```

Output:

```text
4
16
36
64
100
```

Each generator performs one processing step and passes its output to the next generator.

## 17. The `yield from` Statement

The `yield from` statement delegates iteration to another iterable or generator.

It is useful for combining values from multiple iterables.

Example:

```python
def generate_values():
    yield from [10, 20, 30]
    yield from [40, 50]

for value in generate_values():
    print(value)
```

Output:

```text
10
20
30
40
50
```

`yield from` can also delegate to another generator.

## 18. Generator State

Generators maintain their execution state between successive calls.

Their state includes:
- Local variables.
- Current execution position.
- Values needed to resume execution.

Example:

```python
def counter():
    count = 1

    while count <= 3:
        yield count
        count += 1

generator = counter()

print(next(generator))
print(next(generator))
print(next(generator))
```

The local variable `count` retains its value between calls to `next()`.

## 19. Closing a Generator

The `close()` method requests that a generator terminate.

It raises `GeneratorExit` inside the generator at its current suspension point.

Example:

```python
def generate_numbers():
    try:
        yield 10
        yield 20
        yield 30

    finally:
        print("Generator closed")

generator = generate_numbers()

print(next(generator))

generator.close()
```

The `finally` block executes when the generator is closed.

## 20. Iterators and Generators in AI Applications

Iterators and generators are useful in data-intensive applications.

Examples include:

### Large Dataset Processing

Generators can process records one at a time without loading an entire dataset into memory.

### Document Processing

A document-processing pipeline can generate chunks incrementally.

### RAG Applications

Generators can help process:
- Large collections of documents.
- Document chunks.
- Streaming retrieval results.
- Batch processing tasks.

### Streaming LLM Responses

Generator-based interfaces can produce response chunks incrementally.

Actual LLM streaming APIs may use provider-specific streaming interfaces rather than ordinary Python generators.

## 21. Best Practices

- Use iterators when processing elements sequentially.
- Use generators when values can be produced on demand.
- Prefer generator expressions for simple lazy transformations.
- Use generator functions for more complex generation logic.
- Avoid converting a large generator into a list unless all values need to be stored.
- Remember that iterators are generally consumed as they are traversed.
- Handle `StopIteration` appropriately when manually using `next()`.
- Close generators when early termination requires cleanup.
- Keep generator functions focused on a specific processing task.

## 22. Key Concepts Summary

| Concept | Description |
|---|---|
| Iterable | Object that can provide an iterator |
| Iterator | Object that returns elements one at a time |
| `iter()` | Creates or retrieves an iterator |
| `next()` | Retrieves the next iterator element |
| `StopIteration` | Indicates that an iterator is exhausted |
| `__iter__()` | Returns an iterator |
| `__next__()` | Returns the next element |
| Generator | Special iterator that produces values lazily |
| `yield` | Produces a value and suspends generator execution |
| Generator expression | Compact syntax for creating a generator |
| Lazy evaluation | Computes values only when requested |
| `yield from` | Delegates iteration to another iterable |
| `close()` | Requests generator termination |

## 23. Official References

- Python Tutorial — Iterators: https://docs.python.org/3/tutorial/classes.html#iterators
- Python Documentation — Iterator Types: https://docs.python.org/3/library/stdtypes.html#iterator-types
- Python Documentation — Generator Expressions: https://docs.python.org/3/reference/expressions.html#generator-expressions
- Python Documentation — Yield Expressions: https://docs.python.org/3/reference/expressions.html#yield-expressions