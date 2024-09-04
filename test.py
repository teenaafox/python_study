for n in range(1,6):
  print("*" * n)

for n in range(1,6):
  print(" "*(5-n) + "*"*n)
 

for n in range(1,6):
  if n <= 3:
    print(" "*(3-n) + "*"*(2*n-1))
  else:
    print(" "*(n-3)+"*"*(2*(6-n)-1))