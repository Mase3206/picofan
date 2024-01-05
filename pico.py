# This is MicroPython.

# https://stackoverflow.com/questions/20923411/updating-class-variable-within-a-instance-method
# https://micropython-tve.readthedocs.io/en/counter/pyboard/general.html


class Fan():
	import time
#	from machine import Counter, Pin

	# addr = '0x00'
	# pin_power = 0
	# pin_pwm = 0
	# pin_tach = 0
	# state = {}

	def __init__(self, pico_address:type('0x00'), power_ctrl_pin:int, pwm_pin:int, tach_pin:int):
		self.addr = pico_address
		self.pin_power = power_ctrl_pin
		self.pin_pwm = pwm_pin
		self.pin_tach = tach_pin
		self.state = {
			'setSpeed': 0.0,
			'isOn': False,
		}


	def set(self, speed:float):
		if speed == 0.0:
			# Pin.set(self.pin_power, 0)
			self.state['isOn'] = False
			print(f'Fan {self.__name__}: power set = off.')
			
			self.state['setSpeed'] = speed
			print(f'Fan {self.__name__}: speed set = {speed * 100}%')

			return speed

		elif speed > 0.0:
			if self.state['isOn'] == False:
				# Pin.set(self.pin_power, 1)
				self.state['isOn'] = True
				print(f'Fan {self.__name__}: power set = on.')

			self.PWM(speed=speed)
			self.state['setSpeed'] = speed
			print(f'Fan {self.__name__}: speed set = {speed * 100}%')

			return speed
		
		else:
			print(f'Fan {self.__name__}: speed must be type(float) from 0.0 to 1.0. Given: speed = {speed}, type({type(speed)})')


	def getState(self):
		print(f'Fan {self.__name__}: get state:')
		print('\tisOn =', self.state['isOn'])
		print('\tsetSpeed =', self.state['setSpeed'])

		return self.state
	

	def getInfo(self):
		print(f'Fan {self.__name__}: get info:')
		print('\tpico address =', self.addr)
		print('\tpins:')
		print('\t\tpower =', self.pin_power)
		print('\t\tPWM =', self.pin_pwm)
		print('\t\ttach =', self.pin_tach)

		info = {
			'addr': self.addr,
			'pins': {
				'power': self.pin_power,
				'pwm': self.pin_pwm,
				'tach': self.pin_tach
			}
		}
		return info