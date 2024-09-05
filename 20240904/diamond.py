for i in range(1, 6):
  if i <= 3:
    print(' ' * (3-i) + '*' * (2*i-1))
  else:
    print(' ' * (i-3) + '*' * (2*(6-i)-1))