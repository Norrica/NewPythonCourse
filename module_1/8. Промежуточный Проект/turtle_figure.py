import turtle

turtle.speed(2000)
rainbow = ['red', 'orange', 'yellow' , 'green', 'cyan', 'blue', 'violet']
i = 0
turtle.pensize(10)
while True:
	turtle.forward(i)
	turtle.color(rainbow[i % len(rainbow)])
	turtle.left(360 / len(rainbow) - 1)
	i += 1

turtle.mainloop()
