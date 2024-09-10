import pandas as pd # pip install pandas openpyxl
import sys
import os


                           # separator="|" == separator의 기본값이 "|" 로 할당
                           # { if len(sys.argv) == 3 else "|" }와 같은 말 
def excel_to_sep(excel_file, separator="|"): # == def excel_to_sep(excel_file, separator):
	try:
		# 엑셀 파일 읽기
		df = pd.read_excel(excel_file)

		# 출력 파일명 생성
		base_name = os.path.splitext(os.path.basename(excel_file))[0]
		text_file = f"{base_name}.txt"

		# 파일로 저장
		with open(text_file, "a", encoding="utf8") as f:

			# 컬럼 제목 출력
			f.write(separator.join(df.columns) + "\n")

			# 각 행의 내용 출력
			for index, row in df.iterrows():
				f.write(
					separator.join(
						str(value).replace(separator, f"\\{separator}") for value in row
					)
					+ "\n"
				)
		print(f"{excel_file}의 내용이 {text_file}에 성공적으로 저장되었습니다.")
		print(f"사용된 구분자: {separator}")

	except Exception as e:
		print(f"오류 발생: {str(e)}")


if __name__ == "__main__":
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print("사용법: python x12sep.py <엑셀_파일_경로> [구분자]")
		print("구분자를 지정하지 않으면 '|'가 사용됩니다.")
	else:
		excel_file = sys.argv[1]
		separator = sys.argv[2] # if len(sys.argv) == 3 else "|"
		excel_to_sep(excel_file, separator)