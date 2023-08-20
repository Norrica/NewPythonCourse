import turtle

turtle.speed(200)


def move(heading, pixels=100):
    turtle.setheading(heading)
    turtle.forward(pixels)


pixels = 10
funcs = {
    'w': lambda: move(90, pixels),
    'a': lambda: move(180, pixels),
    's': lambda: move(270, pixels),
    'd': lambda: move(0, pixels),
    'e': lambda: turtle.right(pixels),
    'q': lambda: turtle.left(pixels),
    'space': lambda: turtle.forward(pixels),

}

for k, v in funcs.items():
    turtle.onkeypress(v, k)
turtle.listen()
turtle.mainloop()
