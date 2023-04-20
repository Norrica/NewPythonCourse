import turtle

t1 = turtle.Turtle()
t2 = turtle.Turtle()
t2.goto(0,50)

turtle.onkey(lambda :t1.forward(10),'z')
turtle.onkey(lambda :t2.forward(10),'x')
def repeat():
    t1.backward(1)# увеличивать скорость когда близко к финишу
    t2.backward(1)# увеличивать скорость когда близко к финишу
    turtle.ontimer(repeat,50)


turtle.ontimer(repeat,50)
turtle.listen()
turtle.mainloop()