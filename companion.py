class Fan():
	import time

	# addr = '0x00'
	# pin_power = 0
	# pin_pwm = 0
	# pin_tach = 0
	# state = {}

	def __init__(self, picoAddress:type('0x00'), fanNumber:int, powerCtrlPin:int, pwmPin:int, tachPin:int):
		self.addr = picoAddress
		self.pin_power = powerCtrlPin
		self.pin_pwm = pwmPin
		self.pin_tach = tachPin
		self.fanNumber = fanNumber
		self.state = {
			'setSpeed': 0.0,
			'isOn': False,
		}


	def set(self, speed:float):
		if speed == 0.0:
			self.state['isOn'] = False
			print(f'Fan {self.fanNumber}: set speed = off')
			
			self.state['setSpeed'] = speed
			print(f'Fan {self.fanNumber}: set power = {speed * 100}%')

			return speed

		elif speed > 0.0:
			if self.state['isOn'] == False:
				self.state['isOn'] = True
				print(f'Fan {self.fanNumber}: set power = on')

			self.state['setSpeed'] = speed
			print(f'Fan {self.fanNumber}: set speed = {speed * 100}%')

			return speed
		
		else:
			raise ValueError(f'Fan {self.fanNumber}: speed must be type(float) from 0.0 to 1.0. Given: speed = {speed}')


	def getState(self):
		# print(f'Fan {self.fanNumber}: get state:')
		# print('\tisOn =', self.state['isOn'])
		# print('\tsetSpeed =', self.state['setSpeed'])
		# print()

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
			'addr': self.addr,
			'pins': {
				'power': self.pin_power,
				'pwm': self.pin_pwm,
				'tach': self.pin_tach
			}
		}
		return info



# Initialize intake fan 1
intake1 = Fan('0x10', 1, 4, 5, 6)

print(intake1.getState())
print(intake1.getInfo())

intake1.set(0.5)