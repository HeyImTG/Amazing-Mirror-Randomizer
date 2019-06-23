#Contains a bunch of functions that are used across all the scripts.
#==================================================
def writeValueToRom(romname,address,value,bytes):
	romname.seek(address)
	romname.write(value.to_bytes(bytes,'big'))
#==================================================