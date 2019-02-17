#!/usr/bin/env bash

echo "Starting up virtual environment..."
source ./venv/bin/activate
echo "...environment started up."

echo "Starting up application..."
python app.py --save=True
echo "...finished starting up application."