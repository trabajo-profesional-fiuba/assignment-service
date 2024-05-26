# Assignment Service

[![codecov](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service/graph/badge.svg?token=88MT80VD78)](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service)

An assignment service designed to solve assignment problems such as:

- Assign people or person to an incomplete group of students.
- Assign topic and tutors to groups of students.
- Assign presentation dates to groups of students.

## Dependencies

This project uses [Poetry](https://python-poetry.org/) for managing dependencies. Poetry simplifies the process of dependency management by providing a single tool for installing and managing project dependencies. To ensure that your environment is properly set up, follow the installation instructions below.

### Installation

To install the project dependencies using Poetry, run the following command in your terminal:

```bash
poetry install
```

### Execution

To execute the program using Poetry, run the following command in your terminal:

```bash
poetry run python main.py
```

### Tests

To run tests using Poetry, run the following command in your terminal:

```bash
poetry run pytest
```

### Format

To format code using Poetry, run the following command in your terminal:

```bash
poetry run black .
```

### Check format

To check format code using Poetry, run the following command in your terminal:

```bash
poetry run flake8
```
