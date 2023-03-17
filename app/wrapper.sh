#!/bin/bash

set -e

exec python3 process_video.py &
exec python3 app.py
