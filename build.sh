#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install all your packages
pip install -r requirements.txt

# 2. Run your static files command
python manage.py collectstatic --no-input

# 3. Run your database migrations
python manage.py migrate