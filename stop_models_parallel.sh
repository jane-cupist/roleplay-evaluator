#!/bin/sh

# 스크립트 설명: 지정된 Python 프로세스를 종료합니다.
echo "Stopping roleplay-evaluator..."
pkill -f '/Users/jane/Dev/roleplay-evaluator/.venv/bin/python src/main.py'

# 성공 메시지
if [ $? -eq 0 ]; then
  echo "Process stopped successfully."
else
  echo "No matching process found or error occurred."
fi