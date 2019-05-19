#This script randomzies the colour palettes of each of the spray paints.
import sys
import random
import os

from amrShared import writeValueToRom, removeBrackets
#==================================================
def randomizePalette():
	#Kirby's palette is made up of 11 16-bit colours:
	#	Black outline.
	#	7 colours for the body.
	#	3 colours for the feet.

	colourlist = []
	colourstring = 0
	
	#To create more vibrant colours, lower "lowColourMax" and raise "highColourMin".
	lowColourMax = 10
	highColourMin = 21

	seemsgood = False
	while seemsgood == False:
		randr = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		randg = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		randb = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		if (randr + (randg/2) + randb) > 16:
			seemsgood = True
	
	colourlist.append((round(randr) << 10) + (round(randg) << 5) + round(randb))

	for x in range(6):
		randr *= 0.9
		randg *= 0.9
		randb *= 0.9
		colourlist.append((round(randr) << 10) + (round(randg) << 5) + round(randb))
		
	seemsgood = False
	while seemsgood == False:
		randr = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		randg = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		randb = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		if (randr + (randg/2) + randb) > 12:
			seemsgood = True

	colourlist.append((round(randr) << 10) + (round(randg) << 5) + round(randb))

	for x in range(2):
		randr *= 0.8
		randg *= 0.8
		randb *= 0.8
		colourlist.append((round(randr) << 10) + (round(randg) << 5) + round(randb))

	for x in range(len(colourlist)):
		colourstring = colourstring << 16
		colourlist[x] = colourlist[x].to_bytes(2,'little')
		colourstring += int.from_bytes(colourlist[x],'big')
	
	return colourstring

def randomizeSpray(romFile):
	print("Randomizing spray colours...")
	writeValueToRom(romFile,4846172,randomizePalette(),20)
	for x in range(13):
		writeValueToRom(romFile,4846300+(x*32),randomizePalette(),20)
#==================================================
if __name__ == '__main__':
	#Make sure we have our arguments and validation and whatever.
	if len(sys.argv) < 3:
		print("Error: invalid number of arguments. Usage: amrSpray.py \"[path to file]\" [seed number]")
		sys.exit()

	romFile = sys.argv[1] #The first argument is the path to our randomized rom.
	if os.path.isfile(romFile) == False:
		print("Error: ROM file given does not exist. Did you surround the path in \"\" quotes?")
		sys.exit()
	try:
		randomSeed = int(sys.argv[2]) #The second argument is the seed.
	except ValueError:
		print("Error: Random seed is not a number.")
		sys.exit()

	katamrom = open(romFile,'rb+')
	random.seed(randomSeed)
	randomizeSpray(katamrom)
	katamrom.close()