import random

num = random.randint(1, 100)
for i in range(5):  # !!!
    answer = int(input('Какое число я загадал? '))
    if answer > num:
        print('Моё число меньше!')
    elif answer < num:
        print('Моё число больше!')
    else:
        print('Угадал!')
        break

