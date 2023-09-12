class Calculator:
    def __init__(self, param1, param2):
        self.a = param1
        self.b = param2

    def output_result(self):
        print(obj.a + obj.b)


obj = Calculator
Calculator.__init__(obj, 11, 88)
print(obj.a + obj.b)
# Неявный вызов __init__
# obj = Calculator(42,451)
#
# obj.output_result()
