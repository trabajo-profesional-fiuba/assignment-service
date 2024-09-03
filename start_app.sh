#!/bin/bash

# Define the environment file
ENV_FILE=".env.production"

# Export the environment file variable so the Python app can use it
export ENV_FILE

# Print the environment file being used for confirmation
echo "Using environment file: $ENV_FILE"

# Start the Python application
python ./main.py
