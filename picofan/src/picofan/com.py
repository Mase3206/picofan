# This is MicroPython.

# https://stackoverflow.com/questions/20923411/updating-class-variable-within-a-instance-method
# https://micropython-tve.readthedocs.io/en/counter/pyboard/general.html

from __future__ import annotations

from machine import UART, Pin
import json


class JsonSerial(UART):
    '''
    Wrapper around MicroPython's `machine.UART` class, which adds support for reading and writing newline-terminated JSON over UART.
    '''

    def __init__(self, id, *args, **kwargs) -> None:
        super().__init__(id, *args, **kwargs)
    
    def irq(self, *args, **kwargs):
        self._irq = super().irq(*args, **kwargs)

    def write_json(self, data: dict):
        buf = json.dumps(data).encode('utf-8') + b'\n'
        return super().write(buf)
    
    def read_json(self) -> dict:
        ret = super().readline()
        if isinstance(ret, str):
            return json.loads(ret[:-1])
        else:
            return {}
