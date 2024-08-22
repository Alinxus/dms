#!/bin/bash

# Find the PID of the gunicorn process
PID=$(ps aux | grep '[g]unicorn' | awk '{print $2}')

if [ -n "$PID" ]; then
    echo "Killing existing process (PID: $PID)"
    kill $PID
    sleep 5  # Wait for the process to die
    
    # If it's still running, force kill
    if ps -p $PID > /dev/null; then
        echo "Force killing process"
        kill -9 $PID
    fi
else
    echo "No existing process found"
fi

echo "Starting new process"
nohup gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 wsgi:app &

echo "Application restarted"