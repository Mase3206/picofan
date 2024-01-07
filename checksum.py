import convert

def make(byteList:list):
	'''
	checksum make

	Parameters
	----------
	byteList - list of hex string integers, 1 byte (2 digits) each (i.e. '0xfe', not 0xfe)

	Returns
	-------
	1 byte hex integer
	'''

	# print([hex(byte) for byte in byteList])

	evenPart = []
	oddPart = []
	for i in range(len(byteList)):
		if i % 2 == 0:
			evenPart.append(int(byteList[i], base=16))
		else:
			oddPart.append(int(byteList[i], base=16))

	evenPart = sum(evenPart) * 77
	oddPart = sum(oddPart)

	# print(evenPart, oddPart)
	bothParts = evenPart + oddPart

	return f'0x{255 - (bothParts % 255):02x}'



def verify(fullMessage:str):
	byteList = convert.splitHexBytes(fullMessage)
	message = byteList[1:-2]
	receivedCheck = int(byteList[-2], base=16)
	computedCheck = int(make(message), base=16)

	if receivedCheck == computedCheck:
		return True
	else:
		return False
	


if __name__ == '__main__':
	print()
	print(make(['0x01', '0x0a', '0x01', '0x01', '0x01', '0x01']))
	print()
	print(make(['0xff', '0x00', '0xff', '0x00', '0xff', '0x00']))
	print()
	print(make(['0x00', '0xff', '0x00', '0xff', '0x00', '0xff']))


	# print()
	# print(splitHexBytes('0x010a01010101'))


	print()
	print(convert.joinHexBytes(['0x01', '0x0a', '0x01', '0x01', '0x01', '0x01']))