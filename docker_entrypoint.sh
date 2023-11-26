#!/bin/sh
set -e

python /app/src/manage.py migrate

exec "$@"
