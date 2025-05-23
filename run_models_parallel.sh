#!/bin/bash

# 첫 번째 배치: ge 모델 50개 프로세스
for i in {0..9}; do
    for j in {1..5}; do
        poetry run python src/main.py --model ge --limit 100 --companion-index $i &
    done
done

# 첫 번째 배치가 완료될 때까지 대기
wait

# 두 번째 배치: cl 모델 50개 프로세스
for i in {0..9}; do
    for j in {1..5}; do
        poetry run python src/main.py --model cl --limit 100 --companion-index $i &
    done
done

# 두 번째 배치가 완료될 때까지 대기
wait

