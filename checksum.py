def make(message:list):
	'''
	checksum make

	Parameters
	----------
	message - list of hex values, 1 byte (2 digits) each

	Returns
	-------
	checkByte - 1 byte hex
	'''

	# byteList = []
	# print(len(hex(message)))

	# while message >= 0:
	# 	byte = message % 0x100
	# 	print(hex(byte))
	# 	if byte != None: 
	# 		byteList.append(byte)
	# 	message = message // 0x100


	# print([hex(byte) for byte in byteList])
	# byteList = list(reversed(byteList))

	byteList = message

	checkByte = 0
	print([hex(byte) for byte in byteList])

	evenPart = sum([byte for byte in byteList if byte % 2 == 0]) * 6
	oddPart = sum([byte for byte in byteList if byte % 2 == 1])

	print(evenPart, oddPart)
	bothParts = evenPart + oddPart

	return hex(255 - (bothParts % 255)), len(byteList)




	return hex(abs(checkByte)), len(byteList)


print()
print(make([0x01, 0x0a, 0x01, 0x01, 0x01, 0x01]))
print()
print(make([0xff, 0x00, 0xff, 0x00, 0xff, 0x00]))
print()
print(make([0x00, 0xff, 0x00, 0xff, 0x00, 0xff]))
