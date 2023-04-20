integer = 10
string = '10'
boolean = True

veryLongincorrectName = None
very_long_correct_name = None

implicit_conversion1 = string * integer
implicit_conversion2 = integer + boolean

try:
    incompatible_types = string + integer
    print(incompatible_types)
except:
    print('Типы несовместимы')

explicit_conversion1 = string + str(integer)
explicit_conversion2 = int(string) + integer

# Детям самим добавить принты чтобы посмотреть содержание переменных
# Добавить ещё примеров, тоже самим.