FROM python:3.11-slim


RUN pip install poetry

# Set a workdir
WORKDIR /app


COPY pyproject.toml poetry.lock ./

# As we are in a container, is not necessary for poetry to work
# inside a virtual enviroment.
RUN poetry config virtualenvs.create false

# We want to use Poetry only for dependency management but not for packaging
RUN poetry install --no-root

# Copy the src of the project, test and other files are not necessary
COPY src .

# Open port 5000 for be available
EXPOSE 5000

# Define cmd to be executed.
CMD ["python", "./main.py"]
