# file_object = open('data.txt')
# file_content = file_object.read()
# print(file_content)
# file_object.close()


with open('data.txt') as file_object:
	file_content = file_object.read()

result = int(int(file_content) / 10 ** 15 * 7)

with open('result.txt','w') as file_object:
	file_object.write(str(result))
	print('Смотри не сюда, смотри в список файлов слева')


