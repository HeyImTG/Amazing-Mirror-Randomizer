#This script randomizes the ability statues found in the switch and pre-boss rooms.
import json
import os
import sys
import random

from amrShared import writeValueToRom, removeBrackets
#==================================================
def randomizeStands(romFile):
	items = json.load(open('JSON\items.json'))
	itemlist = []
	itemadd = []
	for x in items["AbilityStand"]["item"]:
		itemlist.append(removeBrackets(x))
	for x in items["AbilityStand"]["address"]:
		itemadd.append(removeBrackets(x))

	random.shuffle(itemlist)

	for x in range(len(itemlist)):
		writeValueToRom(romFile,itemadd[x],itemlist[x],6)
#==================================================
if __name__ == '__main__':
	#Make sure we have our arguments and validation and whatever.
	if len(sys.argv) < 3:
		print("Error: invalid number of arguments. Usage: amrMusic.py \"[path to file]\" [seed number]")
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

	if os.path.isfile('JSON\items.json') == False:
		print("Error: Could not find items.json in the JSON folder.")
		sys.exit()

	print("Randomizing ability stands...")

	katamrom = open(romFile,'rb+')
	random.seed(randomSeed)
	randomizeStands(katamrom)
	katamrom.close()