from machine import Pin, ADC, PWM
import time, math
from picofan import sensors



fanTach = Pin(5, Pin.IN)
fanPWM = PWM(Pin(4, Pin.OUT), freq=1000, duty_u16=0)
temp_probe = Pin(26, Pin.IN)


# Voltage Divider
V_in = 3.3
R_0 = 10000  # Resistor value

# Steinhart Constants
A = 0.001129148
B = 0.000234125
C = 0.0000000876741

# fan and temperature limits
min_temp = 30.0
max_temp = 100.0
min_fanSpeed = 0.3
max_fanSpeed = 1.0


temp0 = sensors.Thermistor(temp_probe)


def calculateSpeed(temperature:float) -> float:
    return ((max_fanSpeed - min_fanSpeed) / (max_temp - min_temp)) * (temperature - min_temp) + min_fanSpeed


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



