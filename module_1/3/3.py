from operator import *

ops = {
    'плюс': add,
    'минус': sub,
    'умножить': mul,
    'разделить': truediv,
    'в степени':pow,
    # 'история':[]
    #TODO в 4м уроке калькулятор с историей операций
}
in1 = int(input())
inop = input()
in2 = int(input())

print(ops[inop](in1, in2)) # показать пример на функции отдельно,
# многие не поймут что здесь происходит
# Если всё равно сложно:
chosen_op = ops[inop]
print(chosen_op(in1, in2))
