#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install --upgrade pip
pip install -r requirements.txt

# Apply any outstanding database migrations
python manage.py migrate --run-syncdb

# Collect static files
python manage.py collectstatic --noinput