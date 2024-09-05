# 별 출력 테스트

i = 1
while i <= 5:
    j = 1
    while j <= i:
        print("*", end="")
        j += 1
    print()
    i += 1

i = 1
while i <= 5:
    j = 1
    while j <= 5 - i:
        print(" ", end="")
        j += 1
    j = 1
    while j <= i:
        print("*", end="")
        j += 1
    print()
    i += 1

i = 1
while i <= 5:
    j = 1
    if i <= 3:
        while j <= 3 - i:
            print(" ", end="")
            j += 1
        j = 1
        while j <= 2 * i - 1:
            print("*", end="")
            j += 1
    else:
        while j <= i - 3:
            print(" ", end="")
            j += 1
        j = 1
        while j <= 2 * (6 - i) - 1:
            print("*", end="")
            j += 1
    print()
    i += 1