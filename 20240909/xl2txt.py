import pandas as pd    # pip install pandas openpyxl
import sys
import os


def excel_to_text(excel_file):
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(excel_file)

        # 출력 파일명 생성
        base_name = os.path.splitext(os.path.basename(excel_file))[0]
        text_file = f"{base_name}.txt"

        # 텍스트 파일로 저장
        with open(text_file, "a", encoding="utf-8") as f:
            for column in df.columns:
                f.write(f"{column} ")
                for item in df[column]:
                    f.write(f"{item}   ")
                f.write("\n")      # 열 사이에 빈 줄 추가

        print(f"{excel_file}의 내용이 {text_file}에 성공적으로 저장되었습니다.")

    except Exception as e:
        print(f"오류 발생: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python xl2txt.py <엑셀_파일_경로>")
    else:
        excel_file = sys.argv[1]
        excel_to_text(excel_file)