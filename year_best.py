# 윤년 최적화 소스 코드

yr = 2024

if yr % 4 == 0 and (yr % 100 != 0 or yr % 400 == 0):
    print(str(yr) + ": 윤년")
else:
    print(str(yr) + ": 평년")