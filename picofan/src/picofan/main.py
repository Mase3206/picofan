# This is your main script.
# This is MicroPython.

# https://stackoverflow.com/questions/20923411/updating-class-variable-within-a-instance-method
# https://micropython-tve.readthedocs.io/en/counter/pyboard/general.html
import sys
print(sys.path)

from machine import Pin
import time
from picofan import things, com
from enum import Enum
from typing import Any
from picofan.things import ThingKind
import micropython


UART0 = com.JsonSerial(0, 19200, tx=Pin(1), rx=Pin(2), parity=0, )




class CommandType(Enum):
    SET = 'set'
    GET = 'get'
    REGISTER = 'register'
    # UPDATE = 'update'


def handle_receive_command(uart: com.JsonSerial) -> None:
    micropython.schedule(
        parse_command,
        uart.read_json()
    )

# set the IRQ handler 
# force it to allow JsonSerial over UART for this
UART0.irq(com.JsonSerial.handle_receive_command, com.JsonSerial.IRQ_RXIDLE) # type: ignore



def parse_command(command: dict[str, Any]) -> None:
    match command['command']:
        case CommandType.REGISTER:
            tm.register(
                kind = command['kind'],
                address = command['addr'],
                thing = ThingKind.get_thing_class(command['kind'])(**command['kwargs'])
            )
        case CommandType.GET:
            details = tm.get(
                kind = command['kind'],
                address = command['addr']
            ).__dict__
            message = {
                'kind': command['kind'],
                'addr': command['addr'],
                'details': details
            }
            UART0.write_json(message)
        case CommandType.SET:
            setattr(
                tm.get(
                    kind = command['kind'],
                    address = command['addr']
                ),
                command['param']['name'], command['param']['value']
            )



tm = things.ThingsManager()
'''Things manager.'''
tm.register(
    ThingKind.THERMISTOR, 
    0,
    things.Thermistor(Pin(26, Pin.IN)),
)
tm.register(
    ThingKind.FAN,
    0,
    things.Fan(tach_pin=Pin(5, Pin.IN), pwm_pin=Pin(4, Pin.OUT))
)
tm.register(
    ThingKind.CURVE,
    0,
    things.FanCurve(
        therm = tm.get(ThingKind.THERMISTOR, 0),
        fans = [tm.get(ThingKind.FAN, 0)]
    )
)


def main():
    while True:
        tm.get(ThingKind.CURVE, 0).update_speed()
        time.sleep(1)
