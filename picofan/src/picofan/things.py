'''
Contains classes for thermistors, switches, knobs, fans, etc. Any "thing" that this uses for input or output. Also some software things which link two or more hardware things.
'''

import math
from machine import Pin, ADC, PWM


class Thermistor:
    # Voltage Divider
    V_in = 3.3
    R_0 = 10000  # Resistor value

    # Steinhart Constants
    A = 0.001129148
    B = 0.000234125
    C = 0.0000000876741

    def __init__(self, pinObj:Pin):
        self.thermistor = ADC(pinObj)
    
    @property
    def temperature(self):
        # get voltage value from ADC
        V_read = self.thermistor.read_u16()
        V_out = (3.3 / 65535) * V_read
    
        # Calculate resistance
        R_t = (V_out * self.R_0) / (self.V_in - V_out)
    
        # Steinhart - Hart Equation
        temp_K = 1 / ((self.A + (self.B * math.log(R_t))) + (self.C * math.log(R_t) ** 3))
    
        # Convert from Kelvin to Celsius and return
        return temp_K - 273.15



class Fan:
    tach: Pin
    pwm: PWM

    def __init__(self, tach_pin: Pin, pwm_pin: Pin):
        self.tach = tach_pin
        self.pwm = PWM(pwm_pin, freq=1000, duty_u16=0)


    @property
    def speed(self):
        return self.pwm.duty_u16() / 65535

    @speed.setter
    def speed(self, percentage: float | Thermistor):
        self.pwm.duty_u16(percentage)



class FanCurve:
    '''Very simple linear fan curve.'''

    # fan and temperature limits
    min_temp = 30.0
    max_temp = 100.0
    min_speed = 0.3
    max_speed = 1.0

    def __init__(self, therm: Thermistor, fans: list[Fan]):
        self.therm = therm
        self.fans = fans


    @classmethod
    def calculate_speed(cls, temperature: float):
        slope = ((cls.max_speed - cls.min_speed) / (cls.max_temp - cls.min_temp))
        unbound_speed = slope * temperature
        return max(cls.min_speed, min(unbound_speed, cls.max_speed))

    def update_speed(self):
        temperature = self.therm.temperature
        speed = self.calculate_speed(self.therm.temperature)
        print(f'Temperature: {temperature:.1f}, Fan speed: {speed * 100:.1f}%')
        for fan in self.fans:
            fan.speed = speed
        return speed
