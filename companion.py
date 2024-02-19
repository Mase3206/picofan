import serial, checksum, convert


# initial variables
companionAddr = 'comp0'
UARTport = '/dev/tty.usbmodem143301'

# uart0 = serial.Serial(UARTport, 19200, timeout=1, parity='PARITY_EVEN')
# uart0.open()

class Fan():
	import time

	# Initialize variables
	def __init__(self, picoAddress:str, fanNumber:int, powerCtrlPin:int, pwmPin:int, tachPin:int):
		self.picoAddr = picoAddress
		self.pin_power = powerCtrlPin	# output
		self.pin_pwm = pwmPin			# output
		self.pin_tach = tachPin			# input
		self.fanNumber = fanNumber
		self.state = {		# this is only present for local testing. In real operation, these values would be fetched from the pico via uart0.
			'setSpeed': 0.0,
			'isOn': False,
		}

		# send init command to Pico
		message = ['0xfd', companionAddr, self.picoAddr, '0x01', '0x01', f'0x{self.fanNumber:02x}', f'0x{self.pin_power:02x}', f'0x{self.pin_pwm:02x}', f'0x{self.pin_tach:02x}', '', '0xfe', '0x00', '0x00', '0x00', '0x00', '0x00']
		print(message[1:-8])
		message[-7] = checksum.make(message[1:-8])
		message = bytes(convert.joinHexBytes(message), 'utf-8')
		# uart0.write(message)
		print(message)


	def assembleMessage(self, command:str, value:float):
		value = int(value * 255)

		if command == 'set':
			message = ['0xfd', companionAddr, self.picoAddr, '0x03', '0x01', f'0x{self.fanNumber:02x}', f'0x{value:02x}', '', '0xfe', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00']
			print(message)
		if command == 'get':
			message = ['0xfd', companionAddr, self.picoAddr, '0x04', '0x01', f'0x{self.fanNumber:02x}', f'0x{value:02x}', '', '0xfe', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00']
			print(message)
		message[-9] = (checksum.make(message[1:-10]))
		return message


	# Define speed set method
	def set(self, speed:float):
		if speed >= 0.0 or speed <= 1.0:
			message = convert.joinHexBytes(self.assembleMessage('set', speed))
			message = bytes(message, 'utf-8')
			# uart0.write(message)
			print(message)
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

intake1.set(0.0)