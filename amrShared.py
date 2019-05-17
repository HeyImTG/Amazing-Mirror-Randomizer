#Contains a bunch of functions that are used across all the scripts.
#==================================================
def writeValueToRom(romname,address,value,bytes):
	address = removeBrackets(address)
	romname.seek(address)
	romname.write(value.to_bytes(bytes,'big'))

def removeBrackets(value):
	value = str(value)
	value = value.strip("[")
	value = value.strip("]")
	return int(value)
#==================================================