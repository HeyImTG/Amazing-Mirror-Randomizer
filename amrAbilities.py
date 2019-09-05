#This script randomzies the colour palettes of each of the spray paints.
import random
import os
from amrShared import *
#==================================================
#Object properties start at 3366434.
def randomizeAbilities(romFile,shuffleMode):
	print("Randomizing enemy abilities...")
	abilityList = [0,0,0,0,0,0,0,0,0,0,19,0,0,0,7,3,1,13,2,8,6,15,18,14,16,4,11,8,9,0,20,12,24,18,8,13,0,25,0,2,17,10,14,20,21,22,25]
	abilityAddresses = [[3366434,3367754],[3366458],[3366482],[3366506],[3366530],[3366602,3366770],[3366626],[3366650],[3366674],[3366698],[3366722],[3366794],[3366818],[3366842],[3366866],[3366890],[3366914],[3366938],[3366962],[3366986],[3367010],[3367034],[3367058],[3367082],[3367106],[3367130],[3367154],[3367178,3367202,3367226],[3367250,3367538],[3367274],[3367322],[3367346],[3367394],[3367418],[3367442],[3367466],[3367514],[3367562],[3367658],[3367778],[3367802],[3367826],[3367850],[3367874],[3367898],[3367922],[3367946]]

	if shuffleMode == "Randomize Abilities":
		for x in abilityList:
			if x > 0:
				abilityList[x] = random.randint(1,25)
	else:
		random.shuffle(abilityList)
		
	for x in range(len(abilityAddresses)):
		for y in range(len(abilityAddresses[x])):
			writeValueToRom(romFile,abilityAddresses[x][y],abilityList[x],1)
#==================================================