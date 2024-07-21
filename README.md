# Assignment Service

[![codecov](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service/graph/badge.svg?token=88MT80VD78)](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service)

An assignment service designed to solve assignment problems such as:

- Assign people or person to an incomplete group of students.
- Assign topic and tutors to groups of students.
- Assign presentation dates to groups of students.

## Dependencies

This project uses [Poetry](https://python-poetry.org/) for managing dependencies. Poetry simplifies the process of dependency management by providing a single tool for installing and managing project dependencies. To ensure that your environment is properly set up, follow the installation instructions below.

### Execution

To run the backend service using Docker, run the following command in the terminal:

```bash
docker-compose up --build
```

### Tests

To run tests using Poetry, run the following commands in your terminal:

```bash
.\InitTestDatabase.ps1
```

```bash
poetry run pytest
```

### Important Note

> **Ensure that the PostgreSQL container is running beforehand, as the integration tests require access to the PostgreSQL database.**

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
