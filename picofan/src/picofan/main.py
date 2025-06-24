# This is your main script.
# This is MicroPython.

# https://stackoverflow.com/questions/20923411/updating-class-variable-within-a-instance-method
# https://micropython-tve.readthedocs.io/en/counter/pyboard/general.html
import sys
print(sys.path)

from machine import Pin, ADC, PWM
import time, math
from picofan import sensors


fanTach = Pin(5, Pin.IN)
fanPWM = PWM(Pin(4, Pin.OUT), freq=1000, duty_u16=0)

# initialize Thermistor object
temp0 = sensors.Thermistor(Pin(26, Pin.IN))


# fan and temperature limits
min_temp = 30.0
max_temp = 100.0
min_fanSpeed = 0.3
max_fanSpeed = 1.0


def calculateSpeed(temperature:float) -> float:
    return ((max_fanSpeed - min_fanSpeed) / (max_temp - min_temp)) * (temperature - min_temp) + min_fanSpeed


def main():
    while True:
        temperature = temp0.get()
    
        if temperature <= min_temp:
            speed = min_fanSpeed
        elif temperature >= max_temp:
            speed = max_fanSpeed
        else:
            speed = calculateSpeed(temperature)
    
        print(f'Temperature: {temperature:.1f}, Fan speed: {speed * 100:.1f}%')
        fanPWM.duty_u16(int(speed * 65535))
        time.sleep(0.25)
