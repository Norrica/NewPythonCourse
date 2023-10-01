import time
class ElectricDevice():
    def turn_on(self):
        print('Включаюсь')
    def turn_off(self):
        print('Выключаюсь')
class Lamp(ElectricDevice):
    def __init__(self):
        self.brightness = 0
    def turn_on(self):
        self.brightness = 10
        print(f'Свечу с яркостью {self.brightness}')
    def turn_off(self):
        self.brightness = 0
        print(f'Свечу с яркостью {self.brightness}')
class Kettle(ElectricDevice):
    def turn_on(self):
        self.boil_water()
        self.turn_off()
    def boil_water(self):
        for i in range(3):
            time.sleep(1)
            print('Нагреваю воду')