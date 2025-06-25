# This is your main script.
# This is MicroPython.

# https://stackoverflow.com/questions/20923411/updating-class-variable-within-a-instance-method
# https://micropython-tve.readthedocs.io/en/counter/pyboard/general.html
import sys
print(sys.path)

from machine import Pin
import time
from picofan import things, com


UART0 = com.JsonSerial(0, 19200, tx=Pin(1), rx=Pin(2), parity=0, )



# initialize Thermistor and Fan objects
temp0 = things.Thermistor(Pin(26, Pin.IN))
fan0 = things.Fan(
    tach_pin=Pin(5, Pin.IN),
    pwm_pin=Pin(4, Pin.OUT)
)
# add them to a fan curve
curve = things.FanCurve(temp0, [fan0])


def main():
    while True:
        curve.update_speed()
        time.sleep(1)
