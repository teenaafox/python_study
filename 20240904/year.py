# 윤년 초기 버전

year = 2024
print("year = " + str(year))
if year%4 == 0 and year%100 == 0 and year%400 == 0 :
  print(str(year) + "년은 윤년입니다.")
elif year%4 == 0 and year%100 == 0:
  print(str(year) + "년은 평년입니다.")
elif year%4 == 0:
  print(str(year) + "년은 윤년입니다.")
else:
  print(str(year) + "년은 평년입니다.")