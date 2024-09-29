# Assignment Service

[![codecov](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service/graph/badge.svg?token=88MT80VD78)](https://codecov.io/gh/trabajo-profesional-fiuba/assignment-service)

> _What problem are we trying to solve?_

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

We think that each tutor contains what we call _Periods_, in each period, the tutor has different groups, capacity and topics that the tutor can bring. Also, a tutor can be an evaluator in a specific period.

A tutor can be present in one period but the following be ausent.

# Installation 

For this project is necessary to have  installed ``Python 3.11.*`` and ``Poetry (version 1.8.3)`` for dependency manganment.

You can find how to install python in this [link](https://www.python.org/downloads/release/python-3110/)

## Dependencies

This project uses [Poetry](https://python-poetry.org/) for managing dependencies. Poetry simplifies the process of dependency management by providing a single tool for installing and managing project dependencies. 

To ensure that your environment is properly set up, follow the installation instructions below.

```bash
$ poetry --version

Poetry (version 1.8.3)
```
Poetry creates a virtual enviroment where it handles all the dependencies, this avoid us to install them in our computer and having issues with versions.
Because we are using a virtual enviroment, the python interpreter has to be changed in order to execute poetry commands without invoking poetry.

If you are using vscode as you editor you can add the interpreter doing
![interpreter](docs/image.png)

Then select the one that is from poetry 
![alt text](docs/image-1.png)

Well done! Now you can run commands like `pytest` instead of `poetry run pytest`

## Development

In order to start the development, make sure you are following the [code guidelines](https://github.com/trabajo-profesional-fiuba/.github/blob/main/profile/code_guidelines.md)

Remember to create a `.env.development` following the `.env.example` file. Ask to another dev for shared credentials

## Docker

To run the backend service using [Docker](https://docs.docker.com/), run the following command in the terminal:

```bash
docker compose -f docker-compose.dev.yml up  --build -d

--build is for build the images (not always necessary)

and 

docker compose -f docker-compose.dev.yml down -v
-v remove volumes (not always necessary)
```

## Run Tests Locally

To run tests using Poetry, run the following commands in your terminal:

**Notice:** You need to have `docker installed`

```bash
# if you want to start a postgres db using Docker
.\InitTestDatabase.ps1

# if you want to stop the db
.\InitTestDatabase.ps1 -StopDatabase
```

> **Ensure that the PostgreSQL container is running beforehand, as the integration tests require access to the PostgreSQL database.**

```bash
poetry run pytest or just pytest if env is activated.
```

## Format

For formatting our code, the team chose to use [black](https://black.readthedocs.io/en/stable/index.html)
To format code using Poetry, run the following command in your terminal:

```bash
poetry run black . or just black . if env is activated.
```

## Check format

To check format code using Poetry, run the following command in your terminal:

```bash
poetry run flake8 or just flake8 is env is activated.
```

## Database and migrations

This section can be found at [Migrations](https://github.com/trabajo-profesional-fiuba/assignment-service/blob/main/alembic/README.md)
### Deploy

run before deploying
sed -i -e 's/\r$//'
