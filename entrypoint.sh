#!/bin/bash

RUN_PORT=${PORT:-8000}

/opt/venv/bin/gunicorn -w 6 --threads 4 --worker-tmp-dir /dev/shm -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:${RUN_PORT}" -t 1000 app.main:app