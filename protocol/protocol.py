import struct


proDebug = print

def puserRegister(byteArray):
	proDebug(byteArray)
	if len(byteArray) <= 2:
		proDebug('Error: argv!')
		nameLens = 0
		userName = 0
		passWordLens = 0
		passWord = 0
	else:
		nameLens = byteArray[0]
		userName = byteArray[1: nameLens + 1]
		passWordLens = byteArray[nameLens + 1]
		passWordOffs = nameLens + 2
		passWord = byteArray[passWordOffs: passWordOffs + passWordLens]

	proDebug('nameLens: ', nameLens, ', passWordLens: ', passWordLens)
	proDebug('userName: ', userName, ', passWord: ', passWord)

	return (userName, passWord)

def ppacketAnalyze(byteArray):
	packetID = byteArray[0]
	packetSrc =  struct.unpack('>h', byteArray[1: 3])[0]
	packetDest = struct.unpack('>h', byteArray[3: 5])[0]
	packetLens = struct.unpack('>h', byteArray[5: 7])[0]
	packetData = byteArray[7: 7 + packetLens + 1]

	proDebug('packetID: 0x%02x, packetSrc: 0x%04x, packetDest: 0x%04x' % (packetID, packetSrc, packetDest))
	proDebug('packetLens: %02d' % (packetLens))
	proDebug('packetData: ', packetData)
	return (packetID, packetSrc, packetDest, packetLens, packetData)

if __name__ == '__main__':
	packetID1, packetSrc1, packetDest1, packetLens1, packetData1 = \
		ppacketAnalyze(b'\x01\x22\x22\x00\x88\x00\x0A\x04\x72\x6F\x6F\x74\x04\x31\x32\x33\x34')
	puserRegister(packetData1)

	print('packetID1 = %d' % packetID1)