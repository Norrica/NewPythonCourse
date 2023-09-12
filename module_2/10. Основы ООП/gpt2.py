class MyClass:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


# Неявный вызов __init__
obj = MyClass(42)

# Явный вызов __init__
obj.__init__(42)  # Такой вызов не рекомендуется
