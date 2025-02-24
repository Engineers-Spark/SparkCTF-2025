#!/usr/bin/env bash
python3 -m gunicorn --workers 10 --bind 0.0.0.0:1337 app:app
