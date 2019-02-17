#!/usr/bin/env bash

echo "Starting up virtual environment..."
source ./venv/bin/activate
echo "...environment started up."

echo "Starting up application..."
python app.py --save=True --num_to_render=150
echo "...finished starting up application."