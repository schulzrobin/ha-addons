#!/usr/bin/env bash
set -e
exec gunicorn -b 0.0.0.0:5000 app:app --workers 4 --threads 2
