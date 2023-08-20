import turtle


def target_func():
    print('Работаю по нажатию')


def target_func_with_args(arg):
    print('Работаю по нажатию')
    print(f'Печатаю {arg}')

turtle.onkeypress(target_func, 'a') # Нельзя выполнять 2 разные функции нажатием на одну и ту же кнопку
turtle.onkeypress(lambda: target_func_with_args('Любые слова'), 'b') # Используй `lambda:` чтобы вызвать функцию с аргументами

turtle.listen()
turtle.mainloop()
