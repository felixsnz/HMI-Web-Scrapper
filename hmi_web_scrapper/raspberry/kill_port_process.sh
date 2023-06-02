#!/bin/bash

# Get PID of the process using port 502
PID=$(sudo lsof -i :502)

# If PID exists (i.e., a process is using the port), then kill it
if [ -n "$PID" ]; then
  echo "Killing process $PID on port 502..."
  kill -9 $PID
fi