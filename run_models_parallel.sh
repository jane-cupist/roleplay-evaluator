#!/bin/bash

# 첫 번째 배치: ge 모델 3개씩 실행
for i in {1..4}; do
    for j in {1..2}; do
        poetry run python src/main.py --model ge --limit 100 --companion-index $i --repeat $j &
        poetry run python src/main.py --model cl --limit 100 --companion-index $i --repeat $j &
        if [ $(( (i * 2 + j) % 4 )) -eq 0 ]; then
            wait
        fi
    done
done

wait

