mode = input('Записать или вывести логин-пароль от сервиса?\n'
             '1 - записать\n'
             '2 - вывести\n')
if mode == '1':
    with open('db.txt', "a") as f:
        f.write(input("Введите название сервиса/сайта:") + ' ')
        f.write(input("Введите логин:") + ' ')
        f.write(input("Введите пароль:") + '\n')
elif mode == '2':
    service_name = input('Введите имя сервиса/сайта чтобы получить данные\n')
    with open('db.txt', "r") as f:
        for line in f:
            if line.startswith(service_name):
                print(line)
                break
else:
    print('Недопустимая операция')
