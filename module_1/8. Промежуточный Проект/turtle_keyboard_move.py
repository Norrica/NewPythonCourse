import turtle


def direction(ask_dir):
    match ask_dir:
        case 'W':
            turtle.setheading(90)
        case 'A':
            turtle.setheading(180)
        case 'S':
            turtle.setheading(270)
        case 'D':
            turtle.setheading(0)
        case _:
            return "STOP"


while True:
    ask_dir = input(""" Нажмите, куда двигаться?:
						W - Вверх
						A - Влево
						S - Вниз
						D - Вправо

						""")
    direction(ask_dir)
    how_much = int(input('На сколько пикселей?\n(0 чтобы завершить)\n'))
    if how_much == 0:
        break
    turtle.forward(how_much)
