class QuadraticExuationSolver():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def output_result(self):
        self.d = self.b ** 2 - 4 * self.a * self.c
        if self.d >= 0:
            x1 = (-self.b + self.d ** (1 / 2)) / (2 * self.a)
            x2 = (-self.b - self.d ** (1 / 2)) / (2 * self.a)
        elif self.d < 0:
            x1, x2 = None, None
        print(x1, x2)


solver = QuadraticExuationSolver(3, -20, -1)
solver.output_result()
