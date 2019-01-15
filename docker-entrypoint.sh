#!/bin/sh
set -e
python3 manage.py collectstatic --noinput

echo "Waiting for Database to start...."
sleep 10

echo "Migrating Database"
python3 manage.py migrate --noinput

exec "$@"
