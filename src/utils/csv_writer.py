import csv
import os
from datetime import datetime
from typing import Any, Dict, List


def save_evaluation_to_csv(
    result: Dict[str, Any],
    output_dir: str,
    filename_prefix: str,
    headers: List[str],
    row_writer: callable,
) -> None:
    """평가 결과를 CSV 파일로 저장합니다.

    Args:
        result (Dict[str, Any]): 평가 결과
        output_dir (str): 출력 디렉토리
        filename_prefix (str): 파일명 접두사
        headers (List[str]): CSV 헤더
        row_writer (callable): 각 행을 작성하는 함수
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{output_dir}/{filename_prefix}_{timestamp}.csv"

    file_exists = os.path.isfile(filename)
    mode = "a" if file_exists else "w"

    with open(filename, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        row_writer(writer, result)


def parse_description_block(text):
    lines = text.split("\n")
    result = {}
    key = None
    buffer = []
    for line in lines:
        if line.startswith("- "):
            if key and buffer:
                result[key] = " ".join(buffer).strip()
                buffer = []
            key_value = line[2:].split(":", 1)
            key = key_value[0].strip()
            buffer.append(key_value[1].strip() if len(key_value) > 1 else "")
        elif key:
            buffer.append(line.strip())
    if key and buffer:
        result[key] = " ".join(buffer).strip()
    return result
