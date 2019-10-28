#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

# flask run --port 3978 --host 0.0.0.0
python /functionaltestbot/app.py --host 0.0.0.0