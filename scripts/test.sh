#!/usr/bin/env bash

set -eo pipefail

cd "$(dirname "$0")/.."

mkdir -p outputs

if [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON=".venv/Scripts/python.exe"
elif [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
fi

echo "Running automated OS module tests..."

"$PYTHON" -m pytest tests/ -v | tee outputs/test_results.txt