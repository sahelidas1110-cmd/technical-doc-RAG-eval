
---
title: Python Control Flow
domain: Python
source_url: https://docs.python.org/3/tutorial/controlflow.html
document_type: technical_documentation
version: Python 3
---

# Python Control Flow

## 1. Introduction

Control flow statements determine the order in which instructions are executed in a Python program.

Python provides conditional statements, loops, and control flow statements to manage program execution.

## 2. Conditional Statements

Conditional statements execute different blocks of code depending on whether a condition is true or false.

### if Statement

The if statement executes a block of code when its condition is true.

```python
age = 25

if age >= 18:
    print("Adult")
```

### if-else Statement

The if-else statement provides two execution paths.

```python
age = 16

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

### if-elif-else Statement

The elif keyword allows multiple conditions to be checked.

```python
marks = 75

if marks >= 90:
    print("Grade A")
elif marks >= 60:
    print("Grade B")
else:
    print("Grade C")
```

## 3. for Loops

A for loop iterates over the items of a sequence or another iterable object.

```python
fruits = ["apple", "banana", "orange"]

for fruit in fruits:
    print(fruit)
```

### range() Function

The range() function generates a sequence of numbers.

```python
for number in range(5):
    print(number)
```

The output is 0, 1, 2, 3, and 4.

## 4. while Loops

A while loop repeatedly executes a block of code as long as its condition remains true.

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

The loop stops when the condition becomes false.

## 5. break Statement

The break statement terminates the nearest enclosing loop.

```python
for number in range(10):
    if number == 5:
        break

    print(number)
```

The loop terminates when number becomes 5.

## 6. continue Statement

The continue statement skips the remaining statements in the current loop iteration and proceeds to the next iteration.

```python
for number in range(5):
    if number == 2:
        continue

    print(number)
```

The value 2 is skipped.

## 7. pass Statement

The pass statement performs no operation.

It can be used as a placeholder where a statement is syntactically required.

```python
for number in range(5):
    pass
```

## 8. Loop else Clause

Python supports an else clause with loops.

The else block executes when the loop finishes normally, without being terminated by a break statement.

```python
for number in range(3):
    print(number)
else:
    print("Loop completed")
```

## 9. Nested Loops

A nested loop is a loop inside another loop.

```python
for i in range(2):
    for j in range(3):
        print(i, j)
```

The inner loop executes for each iteration of the outer loop.

## 10. List Comprehensions

List comprehensions provide a concise way to create lists from iterables.

```python
squares = [number ** 2 for number in range(5)]
```

The resulting list contains the squares of numbers from 0 to 4.

## 11. Official Reference

Python Official Documentation:

https://docs.python.org/3/tutorial/controlflow.html
