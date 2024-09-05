t1 = "python"
t2 = "java"
t3 = t1 + ' ' + t2 + ' '
print(t3 * 4)
print((t1 + ' ' + t2 + ' ') * 4)
print(repr(t3 * 4))
print((t3 * 4).strip())
print(repr((t3 * 4).strip()))

#결과
"""
python java python java python java python java   
python java python java python java python java   
'python java python java python java python java '
python java python java python java python java   
'python java python java python java python java' 
"""