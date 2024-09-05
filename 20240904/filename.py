# 확장자가 xlsx 인지 확인하고 싶다
# return 값이 뭐냐

file_name = "보고서.xlsx"
print(file_name.split(".")[1] == "xlsx")
print(file_name.endswith("xlsx"))
print(file_name.endswith(("xlsx", "xls")))

file_name = "보고서.xls"
print(file_name.split(".")[1] == "xlsx")
print(file_name.endswith("xlsx"))
print(file_name.endswith(("xlsx", "xls")))