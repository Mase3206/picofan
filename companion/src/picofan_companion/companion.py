import serial
import os
import json
from typing import Any


class JsonSerial(serial.Serial):
	'''
	Wrapper around PySerial's `serial.Serial` class which adds support for reading and writing newline-terminated JSON over UART.
	'''

	def write_json(self, data: dict):
		buf = json.dumps(data).encode('utf-8') + b'\n'
		return super().write(buf)

	def read_json(self) -> dict:
		ret = super().read_until(
			expected = b'\n', 
			size = None
		)
		return json.loads(str(ret, encoding='utf-8')[:-1])



# initial variables
companionAddr = 'comp0'
UARTport = '/dev/ttyAMA0'

uart0 = JsonSerial(UARTport, 19200, timeout=1, parity=serial.PARITY_EVEN)
uart0.open()


class Fan:
	# Initialize variables
	def __init__(self, picoAddress:str, fanNumber:int, powerCtrlPin:int, pwmPin:int, tachPin:int):
		self.picoAddr = picoAddress
		self.pin_power = powerCtrlPin	# output
		self.pin_pwm = pwmPin			# output
		self.pin_tach = tachPin			# input
		self.fanNumber = fanNumber
		# self.state = {		# this is only present for local testing. In real operation, these values would be fetched from the pico via uart0.
		# 	'setSpeed': 0.0,
		# 	'isOn': False,
		# }

		# send init command to Pico
		message = {
			'command': 'register',
			'kind': 'fan',
			'addr': '0',
			'kwargs': {
				'pwm_pin': 6,
				'tach_pin': 5
			}
		}
		# uart0.write(message)
		print(message)


	# Define speed set method
	def setSpeed(self, speed:float):
		if speed < 0.0 or speed > 1.0:
			raise ValueError(f'Given speed {speed} out of accepted range')
		
		message = {
			'command': 'set',
			'kind': 'fan',
			'addr': '0',
			'param': {
				'name': 'speed',
				'value': speed
			}
		}

		uart0.write_json(message)
		print(message)
		# self.state['setSpeed'] = speed
		
		return speed



	def getState(self):
		message = {
			'command': 'get',
			'kind': 'fan',
			'addr': 0,
		}

		uart0.write_json(message)
		return uart0.read_json()
	

	def getInfo(self):
		# print(f'Fan {self.fanNumber}: get info:')
		# print('\tpico address =', self.addr)
		# print('\tpins:')
		# print('\t\tpower =', self.pin_power)
		# print('\t\tPWM =', self.pin_pwm)
		# print('\t\ttach =', self.pin_tach)
		# print()

		info = {
			'addr': self.picoAddr,
			'pins': {
				'power': self.pin_power,
				'pwm': self.pin_pwm,
				'tach': self.pin_tach
			}
		}
		return info



# Initialize intake fan 1
intake1 = Fan('0x02', 1, 4, 5, 6)

# print(intake1.getState())
# print(intake1.getInfo())

# intake1.set(0.0)
# os.