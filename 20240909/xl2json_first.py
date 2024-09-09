import pandas as pd
import json


def excel_to_json(excel_file, json_file):
    # 엑셀 파일 읽기
    df = pd.read_excel(excel_file)

    # DataFrame을 딕셔너리로 변환
    data = df.to_dict(orient="records")

    # JSON 파일로 저장
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 사용 예시
excel_file = "test.xlsx"  # 변환할 엑셀 파일 이름
json_file = "test_output.json"  # 저장할 JSON 파일 이름

excel_to_json(excel_file, json_file)
print(f"{excel_file}이 {json_file}로 성공적으로 변환되었습니다.")