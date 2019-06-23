#This script randomizes each of the 32 minibosses in the game.
#There four values to set: X/Y, object ID, camera lock data, and difficulty.
#Camera lock data is how close you need to be to the miniboss to start the fight.
#Difficulty is one byte that makes the miniboss slightly faster and have less downtime between attacks/patterns, either a 00 or 01.
import random
import os
import json
from amrShared import *
#==================================================
def checkIfFlying(objectId):
	if objectId == 59 or objectId == 62 or objectId == 63:
		return True
	else:
		return False

def randomizeMinibosses(romFile,minibossDifficulty,minibossesMode):
	print("Randomizing the minibosses...")
	minibosses = json.load(open('JSON\minibosses.json'))
	minibossKeys = list(minibosses.keys())
	minibossList = []

	if minibossesMode == "Shuffle Minibosses":
		for x in minibossKeys:
			minibossList.append(minibosses[x]['object'])
	else:
		for x in range(len(minibossKeys)):
			#minibossList.append(random.randint(56,63))
			minibossList.append(59)
	
	random.shuffle(minibossList)
	
	for x in range(len(minibossKeys)):
		if checkIfFlying(minibossList[x]):
			#X/Y of the object, and how close you need to be to it to start the fight.
			writeValueToRom(romFile,minibosses[minibossKeys[x]]['address'],minibosses[minibossKeys[x]]['airxy'],4)
			writeValueToRom(romFile,minibosses[minibossKeys[x]]['address']+20,minibosses[minibossKeys[x]]['aircam'],3)
		else:
			writeValueToRom(romFile,minibosses[minibossKeys[x]]['address'],minibosses[minibossKeys[x]]['groundxy'],4)
			writeValueToRom(romFile,minibosses[minibossKeys[x]]['address']+20,minibosses[minibossKeys[x]]['groundcam'],3)
		
		#Set the miniboss object.
		writeValueToRom(romFile,minibosses[minibossKeys[x]]['address']+6,minibossList[x],1)
		
		#Make them face the correct direction.
		writeValueToRom(romFile,minibosses[minibossKeys[x]]['address']+8,minibosses[minibossKeys[x]]['facing'],1)
		
		#If this byte is set to 01, the miniboss will be faster and have less downtime between patterns/attacks.
		writeValueToRom(romFile,minibosses[minibossKeys[x]]['address']+10,minibossDifficulty,1)
#==================================================