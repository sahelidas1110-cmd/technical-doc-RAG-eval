---
title: Python Modules and Packages
domain: Python
source_url: https://docs.python.org/3/tutorial/modules.html
document_type: technical_documentation
version: current
---

# Python Modules and Packages

## 1. Introduction to Modules

A module is a Python file containing Python definitions and statements.

Modules allow developers to organize code into separate files and reuse functions, classes, and variables across different programs.

Every Python file with a `.py` extension can be used as a module.

For example, consider a file named `calculator.py`:

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

This file defines two reusable functions.

Another Python file can import and use these functions.

## 2. Importing Modules

Python provides the `import` statement to load modules.

### 2.1 Import the Entire Module

```python
import math

print(math.sqrt(25))
print(math.pi)
```

The module name is used to access its attributes.

### 2.2 Import Specific Functions

The `from ... import ...` syntax imports specific attributes from a module.

```python
from math import sqrt, pi

print(sqrt(25))
print(pi)
```

### 2.3 Import Using an Alias

The `as` keyword assigns an alternative name to an imported module or attribute.

```python
import numpy as np

array = np.array([10, 20, 30])

print(array)
```

Aliases are commonly used for libraries such as NumPy and pandas.

### 2.4 Import All Names

The `from module import *` syntax imports names that a module makes available for wildcard imports.

```python
from math import *

print(sqrt(25))
```

Wildcard imports are generally discouraged because they can introduce naming conflicts and make code harder to understand.

## 3. Creating a Custom Module

Developers can create their own modules by writing reusable Python code in separate files.

Consider this project structure:

```text
project/
├── main.py
└── calculator.py
```

The `calculator.py` file:

```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

The `main.py` file:

```python
import calculator

print(calculator.add(10, 20))
print(calculator.multiply(5, 4))
```

Output:

```text
30
20
```

The `main.py` file imports and uses functions from `calculator.py`.

## 4. Understanding `__name__`

Every Python module has a special built-in variable called `__name__`.

When a Python file is executed directly, its `__name__` value is set to `"__main__"`.

When it is imported as a module, its `__name__` is generally set to the module's import name.

Example:

```python
def greet():
    print("Hello from Python")

if __name__ == "__main__":
    greet()
```

This condition ensures that `greet()` executes when the file is run directly, but not merely because it is imported.

### Why Use `if __name__ == "__main__"`?

- Separates reusable module code from script execution.
- Prevents test or demonstration code from running automatically during imports.
- Makes Python files easier to reuse.
- Supports clean project organization.

## 5. What is a Python Package?

A package is a way to organize related Python modules into a hierarchical structure.

Packages help divide large applications into logical components.

Example:

```text
project/
├── main.py
└── utilities/
    ├── __init__.py
    ├── calculator.py
    └── string_utils.py
```

Here:
- `utilities` is a package.
- `calculator.py` is a module.
- `string_utils.py` is another module.
- `__init__.py` traditionally marks a regular package and can contain package initialization code.

Modern Python also supports namespace packages, which do not require an `__init__.py` file.

## 6. Importing Modules from Packages

Modules inside packages can be imported using dotted module paths.

Example:

```python
from utilities import calculator

print(calculator.add(10, 20))
```

A specific function can also be imported:

```python
from utilities.calculator import add

print(add(10, 20))
```

## 7. Understanding `__init__.py`

The `__init__.py` file is commonly used to initialize a regular Python package.

It can:
- Mark a directory as a regular package.
- Execute package initialization code.
- Import selected functions or classes for convenient access.
- Define package-level variables.

Example:

```python
# utilities/__init__.py

from .calculator import add
```

Now users can import `add` from the package:

```python
from utilities import add

print(add(10, 20))
```

An `__init__.py` file is not mandatory for namespace packages.

## 8. Absolute Imports

An absolute import specifies the complete path from the top-level package.

Example:

```python
from utilities.calculator import add
```

Absolute imports make the module location explicit and are often easier to understand in larger applications.

## 9. Relative Imports

Relative imports specify module locations relative to the current package.

Example:

```python
from .calculator import add
```

A double dot refers to the parent package:

```python
from ..common.logger import setup_logger
```

Relative imports are useful when modules within a package depend on each other.

They must be used within an appropriate package context.

## 10. The Python Module Search Path

When Python imports a module, it searches for that module using its import system.

The search path is exposed through `sys.path`.

It commonly includes:
- The directory containing the input script, depending on how Python was launched.
- Directories specified by `PYTHONPATH`.
- Standard library locations.
- Installed package locations.

Example:

```python
import sys

for path in sys.path:
    print(path)
```

Understanding the module search path helps troubleshoot `ModuleNotFoundError` and import-related issues.

## 11. Common Import Errors

### 11.1 ModuleNotFoundError

This error occurs when Python cannot find the requested module.

Example:

```python
import unknown_module
```

Possible causes:
- The module is not installed.
- The module is not present in the project.
- Python is running from an unexpected working directory.
- The import path is incorrect.
- The wrong Python interpreter or virtual environment is selected.

### 11.2 ImportError

An `ImportError` occurs when Python cannot import a requested name or module.

For example, the module may exist but not contain the requested function or class.

## 12. Modules vs Packages

| Modules | Packages |
|---|---|
| Usually a single Python file | Organize related modules |
| Have a `.py` extension | Usually represented by a directory structure |
| Contain functions, classes, and variables | Contain modules and possibly subpackages |
| Used to organize individual components | Used to organize larger application components |

## 13. Organizing a Real-World Python Project

A larger Python application should be divided into modules based on responsibilities.

Example:

```text
my_project/
├── main.py
├── config.py
├── requirements.txt
├── data/
│   └── input.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── model.py
│   └── evaluation.py
└── tests/
    ├── __init__.py
    └── test_model.py
```

Possible responsibilities:

- `data_loader.py`: Loads data.
- `preprocessing.py`: Cleans and transforms data.
- `model.py`: Defines model-related functionality.
- `evaluation.py`: Evaluates model performance.
- `config.py`: Stores application configuration.
- `tests/`: Contains automated tests.

This modular structure improves readability, testing, and maintainability.

## 14. Modules and Packages in AI Projects

Modules and packages are important when building machine learning and generative AI applications.

For example, a RAG application can separate its functionality into modules:

```text
rag_project/
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── rag_pipeline.py
├── evaluation/
│   └── evaluator.py
└── main.py
```

Each module performs a specific task.

This approach makes it easier to maintain, test, and extend the RAG pipeline.

## 15. Best Practices

- Keep modules focused on a specific responsibility.
- Use meaningful module and package names.
- Avoid circular imports whenever possible.
- Prefer explicit imports over wildcard imports.
- Use `if __name__ == "__main__"` for script-specific execution.
- Use virtual environments to manage project dependencies.
- Organize larger applications into logical packages.
- Keep reusable code separate from application entry points.

## 16. Key Concepts Summary

| Concept | Description |
|---|---|
| Module | A Python file containing reusable code |
| Package | A structure for organizing related modules |
| `import` | Imports a module |
| `from ... import` | Imports selected names |
| `as` | Assigns an alias |
| `__name__` | Special variable identifying a module's execution context |
| `__main__` | Name assigned when a module is executed as the main program |
| `__init__.py` | Common package initialization file |
| Absolute import | Import using a complete package path |
| Relative import | Import relative to the current package |
| `sys.path` | List of locations searched for modules |

## 17. Official References

- Python Tutorial — Modules: https://docs.python.org/3/tutorial/modules.html
- Python Documentation — The Import System: https://docs.python.org/3/reference/import.html
- Python Documentation — `sys.path`: https://docs.python.org/3/library/sys.html#sys.path