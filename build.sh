#!/usr/bin/env bash
set -e  # Exit on any failure

# Update and install system deps (optional, if needed)
# apt-get update && apt-get install -y build-essential libpq-dev

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate --noinput

# (Optional) Collect static files
python manage.py collectstatic --noinput
