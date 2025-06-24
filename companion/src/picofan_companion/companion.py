import serial, convert, os


# initial variables
companionAddr = 'comp0'
UARTport = '/dev/ttyAMA0'

uart0 = serial.Serial(UARTport, 19200, timeout=1, parity=serial.PARITY_EVEN)
uart0.open()

class Fan():
	import time

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
			'command': 'initDevice',
			'type': 'fan',
			'addr': '0',
			'pins': {
				'out_power': 4,
				'out_pwm': 6,
				'in_tach': 5
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
			'type': 'fan',
			'addr': '0',
			'speed': speed
		}

		uart0.write(message)
		print(message)
		# self.state['setSpeed'] = speed
		
		return speed



	def getState(self):
		message = {
			'command': 'get',
			'type': 'fan',
			'addr': 0,
			'getInfo': 'state'
		}

		uart0.write(message)

		return self.state
	

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