def splitHexBytes(hexstream:str):
	byteList = []
	streamLen = (len(hexstream) - 2) // 2	# remove the '0x', divide by 2 to count each 2-digit chunk
	# print(streamLen)

	hexstream = int(hexstream, base=16)

	for i in range(streamLen):
		byte = hexstream % 0x100
		print(hex(byte))
		byteList.append(byte)
		hexstream = hexstream // 0x100


	# print([hex(byte) for byte in byteList])
	return list(reversed(byteList))



def joinHexBytes(byteList:list):
	# strip hex byte strings of the '0x' prefix
	strippedBytes = [byte[2:4] for byte in byteList]

	strippedBytes = ''.join(strippedBytes)
	return '0x' + strippedBytes