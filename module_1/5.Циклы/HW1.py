# комментарием обозначены части которые нужно переделать/добавить для соответствующего задания
import random

num = random.randint(1, 100)
tries = 5  # 1
for i in range(tries):  # 1
    print(f'У тебя осталось {tries} попыток')  # 1.a*
    tries -= 1  # 1
    answer = int(input('Какое число я загадал? '))
    if answer > num:
        print('Моё число меньше!')
    elif answer < num:
        print('Моё число больше!')
    else:
        # print('Угадал!') # 1.a*
        break
if tries == 0:  # 1.a*
    print('Ты проиграл')  # 1.a*
else:  # 1.a*
    print('Ты выиграл!')  # 1.a*
