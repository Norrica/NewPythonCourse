try:
	var = 1/0
except:
	print('Нельзя делить на 0')

try:
	f = open('file')
	a = 10
except:
	print('Файла не существует')
print(a)