# This is MicroPython.

# https://stackoverflow.com/questions/20923411/updating-class-variable-within-a-instance-method
# https://micropython-tve.readthedocs.io/en/counter/pyboard/general.html


picoAddress = '0x02'

from machine import UART, Pin

uart0 = UART(0, 19200, tx=Pin(1), rx=Pin(2), parity=0)