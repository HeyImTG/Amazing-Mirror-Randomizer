#This script randomzies the colour palettes of each of the spray paints.
import random
import os
from amrShared import *
#==================================================
def randomizePalette():
	#Kirby's palette is made up of 11 16-bit colours:
	#	Black outline.
	#	7 colours for the body.
	#	3 colours for the feet.

	colourlist = []
	colourpalettes = []
	colourstring = 0
	
	bodyShadingScale = random.randint(75,90) / 100
	feetShadingScale = random.randint(70,85) / 100
	
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
		randr *= bodyShadingScale
		randg *= bodyShadingScale
		randb *= bodyShadingScale
		colourlist.append((round(randr) << 10) + (round(randg) << 5) + round(randb))
		
	seemsgood = False
	while seemsgood == False:
		randr = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		randg = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		randb = random.choice([random.randint(0,lowColourMax),random.randint(highColourMin,31)])
		if (randr + (randg/2) + randb) > 12:
			seemsgood = True

	colourlist.append((round(randr) << 10) + (round(randg) << 5) + round(randb))
	
	for x in range(4):
		randr *= feetShadingScale
		randg *= feetShadingScale
		randb *= feetShadingScale
		colourlist.append((round(randr) << 10) + (round(randg) << 5) + round(randb))

	for x in range(len(colourlist)):
		colourstring = colourstring << 16
		colourlist[x] = colourlist[x].to_bytes(2,'little')
		colourstring += int.from_bytes(colourlist[x],'big')
	
	colourpalettes.append(colourstring)
	
	#Now we need to make the palette for the 1UP and HP HUD elements. We'll have to frankenstien colours from the previous colourstring.
	colourstring = int.from_bytes(colourlist[1],'big')
	colourstring = colourstring << 16
	colourstring += int.from_bytes(colourlist[3],'big')
	colourstring = colourstring << 16
	colourstring += int.from_bytes(colourlist[5],'big')
	colourstring = colourstring << 16
	colourstring += int.from_bytes(colourlist[8],'big')
	colourstring = colourstring << 16
	colourstring += int.from_bytes(colourlist[4],'big')
	colourstring = colourstring << 16
	colourstring += int.from_bytes(colourlist[6],'big')
	colourpalettes.append(colourstring)
	return colourpalettes

def randomizeSpray(romFile):
	print("Randomizing spray colours...")
	currentPalette = randomizePalette()
	writeValueToRom(romFile,4846172,currentPalette[0]>>32,20) #Normal palette. We don't want to use the last two colours, since that's for UFO only. 
	writeValueToRom(romFile,4849948,currentPalette[0],24) #UFO palette.
	writeValueToRom(romFile,3343094,currentPalette[1],12) #HUD palettes (lives + vitality).
	for x in range(13):
		currentPalette = randomizePalette()
		writeValueToRom(romFile,4846300+(x*32),currentPalette[0]>>32,20)
		writeValueToRom(romFile,4850076+(x*32),currentPalette[0],24)
		writeValueToRom(romFile,3343126+(x*32),currentPalette[1],12)
#==================================================