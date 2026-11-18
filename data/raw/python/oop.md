---
title: Python Object-Oriented Programming
domain: Python
source_url: https://docs.python.org/3/tutorial/classes.html
document_type: technical_documentation
version: current
---

# Python Object-Oriented Programming (OOP)

## 1. Introduction to Object-Oriented Programming

Object-Oriented Programming (OOP) is a programming paradigm that organizes software around classes and objects.

It combines data (attributes) and behavior (methods) into reusable structures.

Python supports object-oriented programming and provides features such as:

- Classes and objects
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Composition

OOP helps developers build modular, reusable, and maintainable applications.

## 2. Classes and Objects

### What is a Class?

A class is a blueprint or template used to create objects.

It defines the attributes and methods that its objects can have.

### What is an Object?

An object is an instance of a class.

Each object can maintain its own state through instance attributes.

Example:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Salary: {self.salary}")

employee1 = Employee("Alice", 50000)
employee2 = Employee("Bob", 60000)

employee1.display_details()
employee2.display_details()
```

In this example:

- `Employee` is the class.
- `employee1` and `employee2` are objects.
- `name` and `salary` are instance attributes.
- `display_details()` is an instance method.
- Each object maintains its own attribute values.

## 3. The `__init__()` Method

The `__init__()` method is an initializer that Python calls automatically after a new object has been created.

It is commonly used to initialize instance attributes.

Example:

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student1 = Student("John", 22)

print(student1.name)
print(student1.age)
```

Output:

```text
John
22
```

The `__init__()` method is not technically the object creation method. Python uses `__new__()` to create an instance and `__init__()` to initialize it.

## 4. Understanding `self`

`self` refers to the current instance of a class.

It allows instance methods to access and modify the attributes and methods belonging to that object.

Example:

```python
class Employee:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}")

employee = Employee("Alice")
employee.greet()
```

When `employee.greet()` is called, Python automatically passes the employee instance as the first argument to the method.

`self` is a strong Python convention, although it is not a reserved keyword.

## 5. Instance Variables and Class Variables

Python classes can contain both instance variables and class variables.

### 5.1 Instance Variables

Instance variables belong to individual objects.

Different objects can have different values for the same instance variable.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

employee1 = Employee("Alice", 50000)
employee2 = Employee("Bob", 60000)

print(employee1.salary)
print(employee2.salary)
```

### 5.2 Class Variables

Class variables are defined within a class but outside its instance methods.

They are shared through the class unless an instance attribute with the same name overrides access through that instance.

```python
class Employee:
    company = "ABC Technologies"

    def __init__(self, name):
        self.name = name

employee1 = Employee("Alice")
employee2 = Employee("Bob")

print(employee1.company)
print(employee2.company)
```

### Difference Between Instance Variables and Class Variables

| Instance Variables | Class Variables |
|---|---|
| Belong to individual objects | Belong to the class |
| Usually defined using `self` | Defined directly in the class body |
| Each object can have different values | Shared through the class |
| Changes generally affect one instance | Changes to the class attribute can affect all instances that use it |

## 6. Types of Methods in Python

Python classes commonly use three types of methods.

### 6.1 Instance Methods

Instance methods operate on individual object data.

They receive `self` as the first parameter.

```python
class Employee:
    def __init__(self, name):
        self.name = name

    def display_name(self):
        return self.name

employee = Employee("Alice")
print(employee.display_name())
```

### 6.2 Class Methods

Class methods operate on class-level data.

They are defined using the `@classmethod` decorator and receive `cls` as the first parameter.

```python
class Employee:
    company = "ABC Technologies"

    @classmethod
    def change_company(cls, new_company):
        cls.company = new_company

Employee.change_company("XYZ Technologies")

print(Employee.company)
```

### 6.3 Static Methods

Static methods do not automatically receive `self` or `cls`.

They are defined using the `@staticmethod` decorator.

They are useful for utility operations logically related to a class.

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

print(Calculator.add(10, 20))
```

### Comparison of Method Types

| Method Type | First Parameter | Decorator | Typical Purpose |
|---|---|---|---|
| Instance method | `self` | None | Work with object attributes |
| Class method | `cls` | `@classmethod` | Work with class-level data |
| Static method | None automatically | `@staticmethod` | Utility operations |

## 7. Encapsulation

Encapsulation is an OOP concept that combines data and the methods that operate on that data within a class.

It also involves controlling how an object's internal state is accessed and modified.

Python uses naming conventions to indicate different levels of attribute accessibility.

### 7.1 Public Attributes

Public attributes can be accessed from inside and outside the class.

```python
class Employee:
    def __init__(self, name):
        self.name = name

employee = Employee("Alice")
print(employee.name)
```

### 7.2 Non-Public Attributes

A single leading underscore indicates that an attribute is intended for internal use.

This is a convention, not strict access enforcement.

```python
class Employee:
    def __init__(self, name):
        self._name = name
```

### 7.3 Name-Mangled Attributes

A double leading underscore triggers name mangling.

Python changes the attribute name internally to reduce accidental name conflicts, particularly in inheritance.

```python
class Employee:
    def __init__(self, salary):
        self.__salary = salary
```

Name mangling does not provide absolute privacy.

### 7.4 Properties

The `property()` mechanism allows methods to be accessed like attributes.

The `@property` decorator is commonly used to control attribute access.

```python
class Employee:
    def __init__(self, salary):
        self._salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value

employee = Employee(50000)
employee.salary = 60000

print(employee.salary)
```

Properties allow validation and controlled updates without changing the external attribute-access syntax.

## 8. Inheritance

Inheritance allows a class to reuse and extend the attributes and methods of another class.

The existing class is called the parent class or base class.

The derived class is called the child class or subclass.

Example:

```python
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

dog = Dog()

dog.speak()
dog.bark()
```

The `Dog` class inherits the `speak()` method from `Animal`.

## 9. Types of Inheritance

Python supports several inheritance patterns.

### 9.1 Single Inheritance

A child class inherits from one parent class.

```python
class Animal:
    pass

class Dog(Animal):
    pass
```

### 9.2 Multiple Inheritance

A child class inherits from more than one parent class.

```python
class Father:
    def skills(self):
        print("Programming")

class Mother:
    def talent(self):
        print("Music")

class Child(Father, Mother):
    pass

child = Child()
child.skills()
child.talent()
```

### 9.3 Multilevel Inheritance

A class inherits from another derived class, creating an inheritance chain.

```python
class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass
```

### 9.4 Hierarchical Inheritance

Multiple child classes inherit from the same parent class.

```python
class Animal:
    def eat(self):
        print("Eating")

class Dog(Animal):
    pass

class Cat(Animal):
    pass
```

### 9.5 Hybrid Inheritance

Hybrid inheritance combines two or more inheritance patterns.

Python supports complex inheritance structures through its method resolution order.

## 10. Method Overriding

Method overriding occurs when a child class provides its own implementation of a method inherited from the parent class.

```python
class Animal:
    def sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def sound(self):
        print("Dog barks")

dog = Dog()
dog.sound()
```

The child class implementation is used when the method is called on a `Dog` instance.

## 11. The `super()` Function

The `super()` function provides a way to call methods from a parent class or the next class in the method resolution order.

It is commonly used in child-class initializers to reuse parent-class initialization logic.

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

dog = Dog("Tommy", "Labrador")

print(dog.name)
print(dog.breed)
```

Using `super()` helps avoid duplicating initialization code.

## 12. Polymorphism

Polymorphism means that different objects can respond to the same operation or interface in different ways.

Python supports polymorphism through inheritance, method overriding, and duck typing.

Example:

```python
class Dog:
    def sound(self):
        return "Bark"

class Cat:
    def sound(self):
        return "Meow"

animals = [Dog(), Cat()]

for animal in animals:
    print(animal.sound())
```

Output:

```text
Bark
Meow
```

Both objects provide a `sound()` method, but their behavior is different.

### Duck Typing

Duck typing is a Python programming principle in which an object's suitability is determined by the operations it supports rather than its explicit class type.

If an object provides the required method or behavior, it can be used in that context.

```python
class PDFDocument:
    def read(self):
        print("Reading PDF")

class TextDocument:
    def read(self):
        print("Reading text file")

def process_document(document):
    document.read()

process_document(PDFDocument())
process_document(TextDocument())
```

The function works with both objects because both implement the required `read()` method.

## 13. Abstraction

Abstraction exposes essential functionality while hiding implementation details.

Python supports abstract base classes through the `abc` module.

The `ABC` class and `@abstractmethod` decorator are commonly used to define abstract interfaces.

Example:

```python
from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

rectangle = Rectangle(10, 5)

print(rectangle.area())
```

A concrete subclass must implement the inherited abstract methods before it can be instantiated.

## 14. Composition

Composition is a design approach in which one class contains an instance of another class.

It represents a "has-a" relationship.

Example:

```python
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        self.engine.start()

car = Car()
car.start()
```

Here, a `Car` has an `Engine`.

Composition helps build complex objects by combining smaller, reusable components.

## 15. Inheritance vs Composition

| Inheritance | Composition |
|---|---|
| Represents an "is-a" relationship | Represents a "has-a" relationship |
| A class derives behavior from another class | A class contains objects of other classes |
| Creates a parent-child relationship | Creates a relationship between components |
| Can be useful for shared interfaces and behavior | Can be useful for flexible component-based design |

For example:

- A `Dog` is an `Animal`: inheritance.
- A `Car` has an `Engine`: composition.

## 16. Special Methods (Dunder Methods)

Special methods are methods with double underscores at the beginning and end of their names.

They are also called magic methods or dunder methods.

They allow classes to define behavior for built-in Python operations.

Common examples include:

| Special Method | Purpose |
|---|---|
| `__init__()` | Initializes a newly created object |
| `__str__()` | Defines the informal string representation |
| `__repr__()` | Defines the developer-oriented representation |
| `__len__()` | Defines behavior for `len()` |
| `__add__()` | Defines behavior for the `+` operator |
| `__eq__()` | Defines behavior for equality comparison |
| `__iter__()` | Returns an iterator |
| `__next__()` | Returns the next iterator item |

Example:

```python
class Book:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f"Book: {self.title}"

book = Book("Python Programming")

print(book)
```

Output:

```text
Book: Python Programming
```

## 17. Multiple Inheritance and Method Resolution Order (MRO)

When a class inherits from multiple parent classes, Python needs a defined order for searching methods and attributes.

This order is called the Method Resolution Order (MRO).

Python uses the C3 linearization algorithm to determine the MRO.

Example:

```python
class A:
    def show(self):
        print("Class A")

class B(A):
    def show(self):
        print("Class B")

class C(A):
    def show(self):
        print("Class C")

class D(B, C):
    pass

d = D()
d.show()

print(D.mro())
```

The method lookup follows the order returned by `D.mro()`.

The `super()` function also follows this method resolution order.

## 18. Advantages of OOP

- Code reusability through inheritance and composition.
- Modularity through classes and objects.
- Encapsulation of data and behavior.
- Easier maintenance of large applications.
- Flexibility through polymorphism.
- Improved organization of complex software systems.

## 19. When to Use OOP

OOP is useful when an application contains entities with related data and behavior.

Examples include:

- Employee management systems.
- Banking applications.
- E-commerce platforms.
- Inventory management systems.
- Machine learning application components.
- API service layers and business logic.

Not every problem requires OOP. Small scripts and simple data transformations may be clearer with functions and built-in data structures.

## 20. OOP Concepts Summary

| Concept | Description |
|---|---|
| Class | Blueprint for creating objects |
| Object | Instance of a class |
| Constructor / Initializer | `__init__()` initializes an object |
| `self` | Refers to the current instance |
| Encapsulation | Combines data and methods and controls access |
| Inheritance | Reuses and extends another class |
| Polymorphism | Allows different objects to support common operations |
| Abstraction | Exposes essential behavior while hiding implementation details |
| Composition | Builds a class using other objects |
| Method overriding | Redefines an inherited method |
| `super()` | Accesses the next implementation in the MRO |
| MRO | Defines the method lookup order |
| Dunder methods | Special methods that customize Python operations |

## 21. Official References

- Python Tutorial — Classes: https://docs.python.org/3/tutorial/classes.html
- Python Documentation — Data Model: https://docs.python.org/3/reference/datamodel.html
- Python Documentation — `abc` Module: https://docs.python.org/3/library/abc.html