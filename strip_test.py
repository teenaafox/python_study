# 빈칸 출력 없애줘
data = "   삼성전자    "
print(data)
print(repr(data))
data1 = data.strip()
print(data1)
print(repr(data1))

data = "039490     "
print(data)
print(repr(data))
data = data.rstrip()
print(repr(data))

# 결과값
"""
   삼성전자    
'   삼성전자    '
삼성전자
'삼성전자'       
039490
'039490     '    
'039490'
"""