#!/bin/bash

# Print the environment file being used for confirmation
echo "Aplying database migrations"

alembic upgrade head

# Start the Python application
echo "Starting python server"
python ./main.py
