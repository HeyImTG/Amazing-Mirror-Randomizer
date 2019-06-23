#This script randomizes the ability statues found in the switch and pre-boss rooms.
import json
import os
import random
from amrShared import *
#==================================================
def randomizeStands(romFile,randomMode):
	print("Randomizing ability stands...")
	items = json.load(open('JSON\items.json'))
	itemlist = []
	itemadd = []
	for x in items["AbilityStand"]["item"]:
		if randomMode == "Shuffle":
			itemlist.append(x)
		elif x not in itemlist:
			itemlist.append(x)
	for x in items["AbilityStand"]["address"]:
		itemadd.append(x)

	if randomMode == "Shuffle Stands":
		random.shuffle(itemlist)
		for x in range(len(itemadd)):
			writeValueToRom(romFile,itemadd[x],itemlist[x],6)
	else:
		for x in range(len(itemadd)):
			writeValueToRom(romFile,itemadd[x],random.choice(itemlist),6)
#==================================================