shopping_list = {}
print('Оставьте один любой ответ пустым чтобы закончить составление списка')
while True:
    grocery = input('Что купить?\n')
    if not grocery:
        break
    amount = input('Какое количество?\n')
    if not amount:
        break
    shopping_list[grocery] = amount
print(shopping_list)
