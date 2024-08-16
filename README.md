# Assignment Service

[![codecov](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service/graph/badge.svg?token=88MT80VD78)](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service)

An assignment service designed to solve assignment problems such as:

- Assign people or person to an incomplete group of students.
- Assign topic and tutors to groups of students.
- Assign presentation dates to groups of students.

This service is the most important part of the project. It is responsable for assigning as good as possible 
the members for incomplete groups, topics for groups and the dates which each group will be presenting its
final project to the evaluators.

Also, the interaction through this features are made by an API that has a serie of endpoints related to differents entities that interact inside the model.

**Important Entities**
- Students
- Groups
- Tutors
- Topics
- Categories

## Dependencies

This project uses [Poetry](https://python-poetry.org/) for managing dependencies. Poetry simplifies the process of dependency management by providing a single tool for installing and managing project dependencies. To ensure that your environment is properly set up, follow the installation instructions below.

### Execution

To run the backend service using Docker, run the following command in the terminal:

```bash
docker compose -f docker-compose.dev.yml up  --build -d

--build is for build the images (not always necessary)

and 

docker compose -f docker-compose.dev.yml down -v
-v remove volumes (not always necessary)
```

### Tests

To run tests using Poetry, run the following commands in your terminal:

```bash
# if you want to start a postgres db using Docker
.\InitTestDatabase.ps1

# if you want to stop the db
.\InitTestDatabase.ps1 -StopDatabase
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
