---
title: Python File Handling
domain: Python
source_url: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
document_type: technical_documentation
version: current
---

# Python File Handling

## 1. Introduction to File Handling

File handling is the process of creating, reading, writing, updating, and deleting files using a programming language.

Python provides built-in functions and modules for working with files.

File handling is commonly used for:

- Reading datasets for data analysis.
- Saving model outputs.
- Loading configuration files.
- Processing PDF and text documents.
- Reading and writing CSV and JSON data.
- Maintaining application logs.

## 2. Opening a File

Python provides the built-in `open()` function to open files.

Syntax:

```python
file = open("filename", "mode")
```

The `open()` function accepts:
- File path: The location of the file.
- Mode: Specifies how the file should be opened.
- Encoding: Specifies the text encoding when working with text files.

Example:

```python
file = open("sample.txt", "r", encoding="utf-8")
```

This opens `sample.txt` in read mode.

## 3. File Opening Modes

Python supports different file modes.

| Mode | Description |
|---|---|
| `r` | Opens a file for reading. Raises an error if the file does not exist. |
| `w` | Opens a file for writing. Creates it if necessary and truncates an existing file. |
| `a` | Opens a file for appending. Creates it if necessary. |
| `x` | Creates a new file and raises an error if it already exists. |
| `b` | Opens a file in binary mode. |
| `t` | Opens a file in text mode. |
| `r+` | Opens a file for reading and writing without initially truncating it. |
| `w+` | Opens a file for reading and writing, truncating it first. |
| `a+` | Opens a file for reading and appending. |

Text mode is the default mode.

Binary mode is commonly used for non-text files such as images, audio files, and PDFs.

## 4. Reading a File

Python provides several methods for reading file content.

### 4.1 `read()`

The `read()` method reads the file content and returns it as a string in text mode.

```python
file = open("sample.txt", "r", encoding="utf-8")

content = file.read()

print(content)

file.close()
```

The optional size argument limits how many characters are read in text mode.

```python
content = file.read(10)
```

### 4.2 `readline()`

The `readline()` method reads one line at a time.

```python
file = open("sample.txt", "r", encoding="utf-8")

line = file.readline()

print(line)

file.close()
```

Repeated calls read subsequent lines.

### 4.3 `readlines()`

The `readlines()` method reads all remaining lines and returns them as a list of strings.

```python
file = open("sample.txt", "r", encoding="utf-8")

lines = file.readlines()

print(lines)

file.close()
```

### 4.4 Reading a File Using a Loop

Files can be read efficiently one line at a time using a loop.

```python
with open("sample.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

This approach avoids loading the entire file into memory at once.

## 5. Writing to a File

The `write()` method writes a string to a file.

Opening a file in `w` mode truncates existing content.

```python
with open("sample.txt", "w", encoding="utf-8") as file:
    file.write("Hello Python\n")
    file.write("File handling example")
```

The `write()` method returns the number of characters written.

It does not automatically add a newline.

## 6. Appending to a File

The `a` mode adds new content at the end of an existing file.

It creates the file if it does not exist.

```python
with open("sample.txt", "a", encoding="utf-8") as file:
    file.write("\nThis line is appended.")
```

Appending preserves existing file content.

## 7. The `with` Statement

The `with` statement is used to work with context managers.

When opening files, it ensures that the file is properly closed when the block exits, including when an exception occurs.

Example:

```python
with open("sample.txt", "r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

Using `with` is generally preferred over manually calling `close()`.

## 8. Closing a File

When a file is opened manually, it should be closed after use.

```python
file = open("sample.txt", "r", encoding="utf-8")

content = file.read()

file.close()
```

Closing a file releases the associated resources.

The `with` statement is generally safer because it handles closing automatically.

## 9. File Pointer and File Position

A file object maintains a current position that determines where the next read or write operation occurs.

Python provides two useful methods:

### 9.1 `tell()`

The `tell()` method returns the current stream position.

```python
with open("sample.txt", "r", encoding="utf-8") as file:
    print(file.tell())

    file.read(5)

    print(file.tell())
```

### 9.2 `seek()`

The `seek()` method changes the stream position.

```python
with open("sample.txt", "r", encoding="utf-8") as file:
    file.seek(0)
    print(file.read())
```

For text streams, seeking is subject to specific restrictions. Position values returned by `tell()` can be used to restore previously recorded positions.

## 10. Checking Whether a File Exists

Python provides the `pathlib` module for working with file system paths.

Example:

```python
from pathlib import Path

file_path = Path("sample.txt")

if file_path.exists():
    print("File exists")
else:
    print("File does not exist")
```

The `is_file()` method checks whether a path refers to a file.

```python
if file_path.is_file():
    print("This is a file")
```

## 11. Deleting a File

The `unlink()` method from `pathlib.Path` deletes a file.

```python
from pathlib import Path

file_path = Path("sample.txt")

if file_path.exists():
    file_path.unlink()
    print("File deleted")
```

Use file deletion carefully because it can permanently remove data.

## 12. Working with File Paths Using `pathlib`

The `pathlib` module provides an object-oriented approach to working with filesystem paths.

Example:

```python
from pathlib import Path

project_dir = Path("my_project")

data_dir = project_dir / "data"

file_path = data_dir / "input.csv"

print(file_path)
```

Useful `Path` methods and properties include:

| Method or Property | Purpose |
|---|---|
| `exists()` | Checks whether the path exists |
| `is_file()` | Checks whether the path is a file |
| `is_dir()` | Checks whether the path is a directory |
| `mkdir()` | Creates a directory |
| `glob()` | Finds paths matching a pattern |
| `rglob()` | Recursively finds paths matching a pattern |
| `name` | Returns the final path component |
| `suffix` | Returns the file extension |
| `parent` | Returns the parent directory |

Example of creating directories:

```python
from pathlib import Path

data_dir = Path("data/raw")

data_dir.mkdir(parents=True, exist_ok=True)
```

The `parents=True` argument creates missing parent directories.

The `exist_ok=True` argument prevents an error if the directory already exists.

## 13. Working with Binary Files

Binary files contain data that is not necessarily represented as readable text.

Common examples include:
- Images
- Audio files
- Video files
- PDF files
- Serialized data

Binary mode uses `rb`, `wb`, and `ab`.

Example:

```python
with open("image.jpg", "rb") as source:
    content = source.read()

with open("image_copy.jpg", "wb") as destination:
    destination.write(content)
```

Binary mode reads and writes bytes rather than text strings.

## 14. Reading and Writing CSV Files

CSV stands for Comma-Separated Values.

Python provides the built-in `csv` module for reading and writing CSV files.

### 14.1 Reading CSV Files

```python
import csv

with open("employees.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

The `csv.reader()` function reads rows as lists.

### 14.2 Reading CSV Files as Dictionaries

```python
import csv

with open("employees.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["name"])
```

`DictReader` maps each row to a dictionary using the column headers as keys.

### 14.3 Writing CSV Files

```python
import csv

data = [
    ["name", "age"],
    ["Alice", 25],
    ["Bob", 30]
]

with open("employees.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

### 14.4 Writing CSV Using Dictionaries

```python
import csv

employees = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30}
]

with open("employees.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["name", "age"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(employees)
```

## 15. Reading and Writing JSON Files

JSON stands for JavaScript Object Notation.

It is a commonly used format for exchanging structured data between applications and APIs.

Python provides the built-in `json` module.

### 15.1 Reading JSON Files

The `json.load()` function reads JSON data from a file and converts it into corresponding Python objects.

```python
import json

with open("employee.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data)
```

### 15.2 Writing JSON Files

The `json.dump()` function writes Python objects into a JSON file.

```python
import json

employee = {
    "name": "Alice",
    "age": 25,
    "department": "IT"
}

with open("employee.json", "w", encoding="utf-8") as file:
    json.dump(employee, file, indent=4)
```

The `indent` parameter makes the JSON output easier to read.

### 15.3 `json.load()` vs `json.loads()`

| Function | Purpose |
|---|---|
| `json.load()` | Reads JSON data from a file-like object |
| `json.loads()` | Parses a JSON-formatted string |

Example:

```python
import json

json_string = '{"name": "Alice", "age": 25}'

data = json.loads(json_string)

print(data["name"])
```

### 15.4 `json.dump()` vs `json.dumps()`

| Function | Purpose |
|---|---|
| `json.dump()` | Writes JSON data to a file-like object |
| `json.dumps()` | Converts a Python object into a JSON string |

Example:

```python
import json

employee = {"name": "Alice", "age": 25}

json_string = json.dumps(employee)

print(json_string)
```

## 16. Handling File-Related Exceptions

File operations can raise exceptions.

Common file-related exceptions include:

| Exception | Description |
|---|---|
| `FileNotFoundError` | Requested file does not exist |
| `PermissionError` | Operation is not permitted |
| `IsADirectoryError` | A file operation was attempted on a directory |
| `NotADirectoryError` | A path component is not a directory |
| `UnicodeDecodeError` | Bytes cannot be decoded using the specified encoding |
| `OSError` | General operating-system-related error |

Example:

```python
try:
    with open("missing.txt", "r", encoding="utf-8") as file:
        content = file.read()

except FileNotFoundError:
    print("Requested file was not found")

except PermissionError:
    print("Permission denied")
```

Handling file-related exceptions helps applications respond gracefully to filesystem problems.

## 17. File Handling in Data Science and AI Projects

File handling is important throughout data science and AI workflows.

Examples include:

### Data Science

- Reading CSV datasets.
- Saving processed datasets.
- Exporting analysis results.
- Loading JSON configuration files.

### Machine Learning

- Loading training and testing datasets.
- Saving model artifacts.
- Reading preprocessing configurations.
- Exporting prediction results.

### Generative AI and RAG

- Reading PDF and Markdown documents.
- Loading text files for document ingestion.
- Reading API configuration from JSON files.
- Saving evaluation datasets.
- Loading golden question-answer datasets.
- Managing application logs.

For example, a RAG ingestion pipeline may use `pathlib` to discover Markdown and PDF files, then use specialized document loaders to extract their content.

## 18. Best Practices

- Prefer the `with` statement when opening files.
- Specify the encoding explicitly when working with text files.
- Use `pathlib` for filesystem path management.
- Choose the correct file mode.
- Avoid using `w` mode when existing file contents must be preserved.
- Handle file-related exceptions appropriately.
- Use CSV and JSON libraries instead of manually parsing their formats.
- Process large files incrementally when appropriate.
- Validate file paths and input data before processing.

## 19. Key Concepts Summary

| Concept | Description |
|---|---|
| `open()` | Opens a file |
| `read()` | Reads file content |
| `readline()` | Reads one line |
| `readlines()` | Reads remaining lines into a list |
| `write()` | Writes a string to a file |
| `close()` | Closes an opened file |
| `with` | Manages resources using a context manager |
| `seek()` | Changes the current stream position |
| `tell()` | Returns the current stream position |
| `pathlib` | Provides object-oriented filesystem path handling |
| `csv` | Built-in module for CSV operations |
| `json` | Built-in module for JSON operations |
| `rb` / `wb` | Binary read and write modes |

## 20. Official References

- Python Tutorial — Reading and Writing Files: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
- Python Documentation — Built-in `open()`: https://docs.python.org/3/library/functions.html#open
- Python Documentation — `pathlib`: https://docs.python.org/3/library/pathlib.html
- Python Documentation — `csv`: https://docs.python.org/3/library/csv.html
- Python Documentation — `json`: https://docs.python.org/3/library/json.html