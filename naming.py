name1 = "김민수"
age1 = 10
name2 = "이철희"
age2 = 13

print("이름: " + name1 + " 나이: " + str(age1))
print("이름: " + name2 + " 나이: " + str(age2))

print("이름: %s 나이: %d " % (name1, age1))
print("이름: %s 나이: %d " % (name2, age2))

print("이름: {} 나이: {}".format(name1, age1))
print("이름: {} 나이: {}".format(name2, age2))

print(f"이름: {name1} 나이: {age1}")
print(f"이름: {name2} 나이: {age2}")