import random

num = random.randint(1, 100)
tries = 5
for i in range(tries):
    print(f'У тебя осталось {tries} попыток')
    tries -= 1
    answer = int(input('Какое число я загадал? '))
    if answer > num:
        print('Моё число меньше!')
    elif answer < num:
        print('Моё число больше!')
    else:
        break
if tries == 0:
    print('Ты проиграл')
else:
    print('Ты выиграл!')
