
---
title: Python Data Structures
domain: Python
source_url: https://docs.python.org/3/tutorial/datastructures.html
document_type: technical_documentation
version: Python 3
---

# Python Data Structures

## 1. Introduction

Python provides several built-in data structures to store and organize data.

The four commonly used collection types are:

- Lists
- Tuples
- Sets
- Dictionaries

Each data structure has different characteristics and is suitable for different use cases.

## 2. Lists

A list is an ordered and mutable collection of elements.

Lists allow duplicate values and can contain elements of different data types.

### Creating a list

```python
fruits = ["apple", "banana", "orange"]
```

### Important characteristics

- Lists maintain element order.
- Lists are mutable, meaning their elements can be changed.
- Lists allow duplicate elements.
- Lists support indexing and slicing.

### Common list operations

```python
fruits.append("mango")
fruits.remove("banana")
fruits.insert(1, "grapes")
fruits.sort()
```

Other useful methods include:

- `append()` - Adds an element to the end.
- `extend()` - Adds elements from an iterable.
- `insert()` - Inserts an element at a specified position.
- `remove()` - Removes the first matching element.
- `pop()` - Removes and returns an element.
- `reverse()` - Reverses the list in place.
- `copy()` - Creates a shallow copy.

## 3. Tuples

A tuple is an ordered and immutable collection of elements.

Unlike lists, tuples cannot be modified after creation.

### Creating a tuple

```python
coordinates = (10, 20, 30)
```

### Important characteristics

- Tuples maintain element order.
- Tuples are immutable.
- Tuples support indexing and slicing.
- Tuples can contain elements of different data types.
- Tuples support packing and unpacking.

### Tuple unpacking

```python
coordinates = (10, 20, 30)

x, y, z = coordinates
```

The values are assigned to individual variables.

## 4. Sets

A set is an unordered collection of unique elements.

Sets automatically eliminate duplicate values.

### Creating a set

```python
numbers = {10, 20, 30, 20}

print(numbers)
```

The duplicate value is stored only once.

### Important characteristics

- Sets contain unique elements.
- Sets are unordered.
- Sets support membership testing.
- Sets support mathematical set operations.

### Common set operations

```python
A = {1, 2, 3}
B = {3, 4, 5}

print(A.union(B))
print(A.intersection(B))
print(A.difference(B))
```

Important operations include:

- Union
- Intersection
- Difference
- Symmetric difference

An empty set must be created using `set()`, because `{}` creates an empty dictionary.

## 5. Dictionaries

A dictionary stores data in key-value pairs.

Each key is unique within a dictionary.

### Creating a dictionary

```python
student = {
    "name": "Alex",
    "age": 25,
    "course": "Python"
}
```

### Accessing dictionary values

```python
print(student["name"])
```

The `get()` method can also be used to retrieve values.

```python
print(student.get("age"))
```

### Important characteristics

- Dictionaries store key-value pairs.
- Keys must be unique.
- Values can be accessed using their keys.
- Dictionaries are mutable.
- Dictionary keys must be hashable.

### Common dictionary operations

```python
student["city"] = "Kolkata"

student.update({"age": 26})

student.pop("course")
```

Useful methods include:

- `keys()` - Returns dictionary keys.
- `values()` - Returns dictionary values.
- `items()` - Returns key-value pairs.
- `get()` - Retrieves a value using a key.
- `update()` - Updates dictionary entries.
- `pop()` - Removes an entry.

## 6. Comparison of Python Data Structures

| Feature | List | Tuple | Set | Dictionary |
|---|---|---|---|---|
| Ordered | Yes | Yes | No | Yes, insertion order |
| Mutable | Yes | No | Yes | Yes |
| Allows duplicates | Yes | Yes | No | Keys must be unique |
| Data organization | Elements | Elements | Unique elements | Key-value pairs |

## 7. Choosing the Right Data Structure

Use a list when you need an ordered and changeable collection.

Use a tuple when you need an ordered collection that cannot be reassigned element by element.

Use a set when you need unique elements and set operations.

Use a dictionary when you need to associate values with keys.

## 8. Official Reference

Python Official Documentation:

https://docs.python.org/3/tutorial/datastructures.html
