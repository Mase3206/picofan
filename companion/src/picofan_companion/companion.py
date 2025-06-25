import json

import serial


class JsonSerial(serial.Serial):
    """
    Wrapper around PySerial's `serial.Serial` class which adds support for reading and writing newline-terminated JSON over UART.
    """

    def write_json(self, data: dict):
        buf = json.dumps(data).encode("utf-8") + b"\n"
        return super().write(buf)

    def read_json(self) -> dict:
        ret = super().read_until(expected=b"\n", size=None)
        return json.loads(str(ret, encoding="utf-8")[:-1])


# initial variables
uart_port = "/dev/ttyAMA0"

uart0 = JsonSerial(uart_port, 19200, timeout=1, parity=serial.PARITY_EVEN)
uart0.open()


class Fan:
    def __init__(
        self,
        number: int,
        pin_power_control: int,
        pin_pwm: int,
        pin_tach: int,
    ):
        """
        Companion to the picofan.things.Fan class.

        Arguments
        ---------
            number (int) : the number of this fan
            pin_power (int) : pin used to control the fan's power through a transistor or MOSFET
            pin_tach (int) : pin used to read tachometer data
            pin_pwm (int) : pin used to control the fan's PWM duty-cycle
        """
        self.pin_power = pin_power_control  # output
        self.pin_pwm = pin_pwm  # output
        self.pin_tach = pin_tach  # input
        self.number = number

        # send init command to pico
        message = {
            "command": "register",
            "kind": "fan",
            "addr": self.number,
            "kwargs": {"pwm_pin": self.pin_pwm, "tach_pin": self.pin_tach},
        }
        uart0.write_json(message)
        print(message)

    def set_speed(self, speed: float):
        if speed < 0.0 or speed > 1.0:
            raise ValueError(f"Given speed {speed} out of accepted range")

        message = {
            "command": "set",
            "kind": "fan",
            "addr": self.number,
            "param": {"name": "speed", "value": speed},
        }

        uart0.write_json(message)
        print(message)

        return speed

    def get_state(self):
        message = {
            "command": "get",
            "kind": "fan",
            "addr": self.number,
        }

        uart0.write_json(message)
        return uart0.read_json()


# Initialize intake fan 1
intake1 = Fan(1, 4, 5, 6)


# print(intake1.getState())
# print(intake1.getInfo())

# intake1.set(0.0)
# os.
