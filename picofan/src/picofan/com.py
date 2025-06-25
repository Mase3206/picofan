# This is MicroPython.

# https://stackoverflow.com/questions/20923411/updating-class-variable-within-a-instance-method
# https://micropython-tve.readthedocs.io/en/counter/pyboard/general.html


from machine import UART, Pin
import json



class JsonSerial(UART):
    '''
    Wrapper around MicroPython's `machine.UART` class, which adds support for reading and writing newline-terminated JSON over UART.
    '''

    def write_json(self, data: dict):
        buf = json.dumps(data).encode('utf-8') + b'\n'
        return super().write(buf)
    
    def read_json(self) -> dict:
        ret = super().readline()
        if isinstance(ret, str):
            return json.loads(ret[:-1])
        else:
            return {}
        

# uart0 = JsonSerial(0, 19200, tx=Pin(1), rx=Pin(2), parity=0)
