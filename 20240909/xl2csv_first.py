import pandas as pd  # pip install pandas openpyxl
import sys
import os
import csv        # comma seperated values 콤마로 분리된 구분된 데이터


def excel_to_csv(excel_file):
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(excel_file)

        # 출력 파일명 생성
        base_name = os.path.splitext(os.path.basename(excel_file))[0]
        csv_file = f"{base_name}.csv"

        # CSV 파일로 저장
        with open(csv_file, "w", newline="", encoding="euc-kr") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

            # 컬럼 제목 출력
            writer.writerow(df.columns)

            # 각 행의 내용 출력
            for index, row in df.iterrows():
                writer.writerow(row)

        print(f"'{excel_file}'의 내용이 '{csv_file}'에 성공적으로 저장되었습니다.")

    except Exception as e:
        print(f"오류 발생: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python xl2csv.py <엑셀_파일_경로>")
    else:
        excel_file = sys.argv[1]
        excel_to_csv(excel_file)