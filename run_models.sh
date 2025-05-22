#!/bin/bash

# 실행 로그 출력
# ./run_models.sh
echo "Running model: cl"
poetry run python src/main.py --model cl --limit 100

echo "Running model: ge"
poetry run python src/main.py --model ge --limit 100
