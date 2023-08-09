import turtle

turtle.speed(200)


def move(heading, pixels=100):
    turtle.setheading(heading)
    turtle.forward(pixels)


funcs = {
    'w': lambda: move(90, 100),
    'a': lambda: move(180, 100),
    's': lambda: move(270, 100),
    'd': lambda: move(0, 100)
}

for k, v in funcs.items():
    turtle.onkeypress(v, k)
turtle.listen()
turtle.mainloop()
