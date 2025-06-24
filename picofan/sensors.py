import math
from machine import Pin, ADC


class Thermistor:
    def __init__(self, pinObj:Pin):
        self.thermistor = ADC(pinObj)
        # Voltage Divider
        self.V_in = 3.3
        self.R_0 = 10000  # Resistor value

        # Steinhart Constants
        self.A = 0.001129148
        self.B = 0.000234125
        self.C = 0.0000000876741
    
    
    def get(self):
        # get voltage value from ADC
        V_read = self.thermistor.read_u16()
        V_out = (3.3 / 65535) * V_read
    
        # Calculate resistance
        R_t = (V_out * self.R_0) / (self.V_in - V_out)
    
        # Steinhart - Hart Equation
        temp_K = 1 / ((self.A + (self.B * math.log(R_t))) + (self.C * math.log(R_t) ** 3))
    
        # Convert from Kelvin to Celsius and return
        return temp_K - 273.15
