class Calculator:
    def compute(self, num1, operator, num2):
        try:
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                result = num1 / num2
            else:
                print("Недопустимый оператор. Допустимые операторы: +, -, *, /")
                return None
            return result
        except ZeroDivisionError:
            print("Ошибка: деление на ноль.")

    def save_result(self, result, filename):
        try:
            with open(filename, 'w') as file:
                file.write(str(result))
            print("Результат сохранен в файл:", filename)
        except IOError:
            print("Ошибка при сохранении результата в файл.")

    def load_result(self, filename):
        try:
            with open(filename, 'r') as file:
                result = float(file.readline().strip())
            print("Результат загружен из файла:", filename)
            return result
        except FileNotFoundError:
            print("Файл не найден.")
        except ValueError:
            print("Ошибка при чтении результата из файла.")

# Пример использования
calculator = Calculator()
result1 = calculator.compute(10, '+', 5)  # 10 + 5 = 15
calculator.save_result(result1, "result.txt")

result2 = calculator.compute(8, '/', 0)   # Генерируется исключение ZeroDivisionError

result3 = calculator.load_result("result.txt")
print("Загруженный результат:", result3)
