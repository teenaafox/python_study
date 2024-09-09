import sys
import os
import pandas as pd 
import csv
import json

from xl2txt import excel_to_text
from xl2sep import excel_to_sep
from xl2csv import excel_to_csv
from xl2json import excel_to_json


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("사용법: python x12sep.py <엑셀_파일_경로> [구분자]")
		print("구분자를 지정하지 않으면 '|'가 사용됩니다.")
	else :
		excel_file = sys.argv[1]
		separator = sys.argv[2] if len(sys.argv) == 3 else "|"
		
		json_file = "test_output.json"  

		excel_to_text(excel_file)
		excel_to_sep(excel_file, separator)
		excel_to_csv(excel_file)
		excel_to_json(excel_file, json_file)

		print(f"{excel_file}이 {json_file}로 성공적으로 저장되었습니다.")