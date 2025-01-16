#!/bin/bash

# Check if the `.venv` directory exists
if [ ! -d ".venv"]; then
  echo "Error: Virtual environment (.venv) not found." >&2
  exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

# Check if db file exists
if [ ! -f "db.sqlite" ]; then
  echo "Database 'db.sqlite' not found. Setting up the database..."
  alembic upgrade head
  if [ $? -ne 0 ]; then
        echo "Error: Alembic migration failed. Please check your setup." >&2
        deactivate
        exit 1
    fi
fi

# Run the app
echo "Starting the app..."
python3 -m src.GUI.brain_boost_app
if [ $? -ne 0 ]; then
    echo "Error: Application failed to start." >&2
fi

deactivate
