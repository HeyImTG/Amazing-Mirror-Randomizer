#This script ranadomizes the mirrors, cannons, and warp starts.
import random
import os
import json
import sys

from amrShared import writeValueToRom, removeBrackets
#==================================================
def findLinkedMirror(string):
	underscore = string.find("_")
	return string[underscore+1:len(string)] + "_" + string[0:underscore]

def removeBrackets(value):
	value = str(value)
	value = value.strip("[")
	value = value.strip("]")
	return int(value)

def randomizeMirrors(romFile,hubMirrors,totalRandom):
	mirrors = json.load(open('JSON\mirrors.json'))
	mirrorlist = list(mirrors.keys())

	mirrorlist.remove("Int1_Int2")
	mirrorlist.remove("Int2_Int3")
	mirrorlist.remove("Int3_Int2")
	mirrorlist.remove("Car19_Reset") #Cause it's fucking aggrivating
	 
	#Don't randomize the hub mirrors?
	if hubMirrors == 0:
		mirrorlist.remove("Rbr1_Rbr27")
		mirrorlist.remove("Rbr27_Rbr1")
		mirrorlist.remove("Rbr1_Can10")
		mirrorlist.remove("Can10_Rbr1")
		mirrorlist.remove("Rbr1_Cab8")
		mirrorlist.remove("Cab8_Rbr1")
		mirrorlist.remove("Rbr1_Pep5")
		mirrorlist.remove("Pep5_Rbr1")
		mirrorlist.remove("Rbr1_Mnl4")
		mirrorlist.remove("Mnl4_Rbr1")
		mirrorlist.remove("Rbr1_Rbr21")
		mirrorlist.remove("Rbr21_Rbr1")
		mirrorlist.remove("Rbr1_Rbr8")
		mirrorlist.remove("Rbr8_Rbr1")
		mirrorlist.remove("Rbr1_Cab19")
		mirrorlist.remove("Cab19_Rbr1")
		mirrorlist.remove("Rbr1_Rbr15")
		mirrorlist.remove("Rbr15_Rbr1")
		mirrorlist.remove("Rbr1_AbilityRoom")
		mirrorlist.remove("AbilityRoom_Rbr1")
		mirrorlist.remove("Rbr27_Mus12")
		mirrorlist.remove("Mus12_Rbr27")
		mirrorlist.remove("Rbr15_Cab17")
		mirrorlist.remove("Cab17_Rbr15")
		mirrorlist.remove("Rbr21_Car5")
		mirrorlist.remove("Car5_Rbr21")
		mirrorlist.remove("Cab19_Oli11")
		mirrorlist.remove("Oli11_Cab19")
		mirrorlist.remove("Cab8_Rad12")
		mirrorlist.remove("Rad12_Cab8")
		mirrorlist.remove("Pep5_Pep24")
		mirrorlist.remove("Pep24_Pep5")

	#Randomize warp stars.
	print("Randomizing warp stars...")
	warpstaradds = [ [ 8944554, 8944566 ], [ 8964698, 8964710 ], [ 8981034, 8981046 ], [ 8998010, 8998022 ], [ 9006434, 9006446 ], [ 9065234, 9065246 ] ]
	warpstarvalues = [ [ 0, 277076896629504, [ "Mnl1_Mnl2" ] ], [ 4, 69269484247297, [ "Can1_Can9", "Can1_Can2" ] ], [ 1, 12094879601665, [ "Can4_Can6", "Can4_Can2", "Can4_Can5Carbon" ] ], [ 2, 281471017324801, [ "Can7_Can9", "Can7_Can6", "Can7_Can8" ] ], [ 3, 5497809837825, [ "Can21_Can22" ] ], [ 5, 281470681800192, [ "Pep23_Pep24", "Pep23_Car4" ] ] ]

	random.shuffle(warpstarvalues)
	for x in range(len(warpstaradds)):
		writeValueToRom(romFile,warpstaradds[x][0],warpstarvalues[x][0],1)
		writeValueToRom(romFile,warpstaradds[x][1],warpstarvalues[x][1],6)
	
	#Randomize fused cannons.
	print("Randomizing canons stars...")
	cannonadds = [ 8951430, 8999618, 9033722, 9050022 ]
	cannonvalues = [ [ 4179903404153243910, [ "Rbr26_Rbr27", "Rbr26_Rbr25" ] ], [ 3170817811668802562, [ "Mus24L_Kracko" ] ], [ 9583663305579299867, [ "Oli5Bottom_Oli6" ] ], [ 937313871469740802, [ "Rad28_Rad29" ] ] ]

	random.shuffle(cannonvalues)
	for x in range(len(cannonadds)):
		writeValueToRom(romFile,cannonadds[x],cannonvalues[x][0],8)

	#We need to filter our mirror list into two other lists: a dead end list and a...not...dead end list.
	#We're gonna check if the one-way mirror entry (Type 1) is labeled as 'DEADEND'.
	#Then we're gonna check (if total random mode is off) if there's only one possible exit out of a two-way mirror.
	mirrorListRandomized = []
		
	for x in range(len(mirrorlist)):
		mirrorListRandomized.append('NULL')
		
	#Please note that these are the "Pre" random lists.
	if totalRandom == 0:
		twoWayPreRandomList = []
		oneWayPreRandomList = []
		deadEndTwoWayPreRandomList = []
		deadEndOneWayPreRandomList = []
	else:
		mirrorPreRandomList = []
		deadEndPreRandomList = []

	print("Determining dead ends...")
	for x in mirrorlist:
		if mirrors[x]['type'][0] == 0:
			if 'DEADEND' in mirrors[x]['exits']:
				if totalRandom == 0:
					deadEndOneWayPreRandomList.append(x)
				else:
					deadEndPreRandomList.append(x)
			else:
				if totalRandom == 0:
					oneWayPreRandomList.append(x)
				else:
					mirrorPreRandomList.append(x)
		else:
			if totalRandom == 0:
				if mirrors[x]['type'][0] == 1 and len(mirrors[x]['exits']) == 1:
					deadEndTwoWayPreRandomList.append(x)
				else:
					twoWayPreRandomList.append(x)
			else:
				mirrorPreRandomList.append(x)

	print("Randomizing mirrors...")
	if totalRandom == 0:
		random.shuffle(twoWayPreRandomList)
		random.shuffle(oneWayPreRandomList)
		random.shuffle(deadEndTwoWayPreRandomList)
		random.shuffle(deadEndOneWayPreRandomList)
	else:
		random.shuffle(mirrorPreRandomList)
		random.shuffle(deadEndPreRandomList)
		
	#The queue list. Once this runs out, the rest of the mirrors that aren't randomized get filled with dead ends.
	#Once an entrance is randomized, its exits are added to the queue.
	queueList = [ "Rbr1_Rbr2" ] #Start with the first mirror.
	alreadyRandomized = []
	spoilerLogLists = []
	mirrorlistRandomized = []
	for x in range(len(mirrorlist)):
		mirrorlistRandomized.append('NULL')

	if totalRandom == 1:
		while len(queueList) > 0:
			currentPick = random.choice(queueList)

			#If the exit is a CANON or a WARPSTAR, add the exits for that warpstar or canon to the list and move on.
			if currentPick.startswith("WARPSTAR") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in warpstarvalues[int(currentPick[8])-1][2]:
					if not x in alreadyRandomized:
						queueList.append(x)
			elif currentPick.startswith("CANON") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in cannonvalues[int(currentPick[5])-1][1]:
					if not x in alreadyRandomized:
						queueList.append(x)

			#If it's not a CANON or a WARPSTAR, then it's probably something we can work with?
			elif currentPick in mirrorlist:
				currentPickId = mirrorlist.index(currentPick)
				#Dead-end test. If a mirror's exits are all already randomized, add it to the dead-end list and re-random.
				isGoodCheck = False
				while isGoodCheck == False:
					alreadyCheck = 0
					if len(mirrorPreRandomList) == 0:
						isGoodCheck = True
					else:
						for x in mirrors[mirrorPreRandomList[0]]['exits']:
							if x in alreadyRandomized:
								alreadyCheck += 1
							elif x in queueList:
								alreadyCheck += 1
						if alreadyCheck == len(mirrors[mirrorPreRandomList[0]]['exits']):
							deadEndPreRandomList.append(mirrorPreRandomList[0])
							random.shuffle(deadEndPreRandomList)
							del mirrorPreRandomList[0]
						else:
							isGoodCheck = True
				
				if not currentPick in alreadyRandomized:
					alreadyRandomized.append(currentPick)
					if len(mirrorPreRandomList) > 0:
						for x in mirrors[mirrorPreRandomList[0]]['exits']:
							if not x in alreadyRandomized:
								queueList.append(x)
						mirrorlistRandomized[currentPickId] = mirrorPreRandomList[0]
						del mirrorPreRandomList[0]
					else:
						mirrorlistRandomized[currentPickId] = deadEndPreRandomList[0]
						del deadEndPreRandomList[0]

			#This means the exit isn't scheduled to be randomized. Mark it as already randomized, but don't do anything with mirrorlistRandomized.
			else:
				if not currentPick in alreadyRandomized:
					alreadyRandomized.append(currentPick)
					for x in mirrors[currentPick]['exits']:
						if not x in alreadyRandomized:
							queueList.append(x)

			queueList.remove(currentPick)
	#Non-total random.
	else:
		while len(queueList) > 0:
			currentPick = random.choice(queueList)
		
			#If the exit is a CANON or a WARPSTAR, add the exits for that warpstar or canon to the list and move on.
			if currentPick.startswith("WARPSTAR") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in warpstarvalues[int(currentPick[8])-1][2]:
					if not x in alreadyRandomized:
						queueList.append(x)
			elif currentPick.startswith("CANON") and not ( currentPick in alreadyRandomized ):
				alreadyRandomized.append(currentPick)
				for x in cannonvalues[int(currentPick[5])-1][1]:
					if not x in alreadyRandomized:
						queueList.append(x)

			#If it's not a CANON or a WARPSTAR, then it's probably something we can work with?
			elif currentPick in mirrorlist:
				currentPickId = mirrorlist.index(currentPick)
				#Dead-end test. If a mirror's exits are all already randomized, add it to the dead-end list and re-random.
				isGoodCheck = False
				while isGoodCheck == False:
					alreadyCheck = 0
					if mirrors[currentPick]['type'][0] == 0:
						if len(oneWayPreRandomList) == 0:
							isGoodCheck = True
						else:
							#If all a mirror's exits are already randomized, move it to the dead end list.
							for x in mirrors[oneWayPreRandomList[0]]['exits']:
								if x in alreadyRandomized:
									alreadyCheck += 1
								elif x in queueList:
									alreadyCheck += 1
							if alreadyCheck == len(mirrors[oneWayPreRandomList[0]]['exits']):
								deadEndOneWayPreRandomList.append(oneWayPreRandomList[0])
								random.shuffle(deadEndOneWayPreRandomList)
								del oneWayPreRandomList[0]
							else:
								isGoodCheck = True
					else:
						if len(twoWayPreRandomList) == 0:
							isGoodCheck = True
						else:
							#If all a mirror's exits are already randomized, move it to the dead end list.
							for x in mirrors[twoWayPreRandomList[0]]['exits']:
								if x in alreadyRandomized:
									alreadyCheck += 1
								elif x in queueList:
									alreadyCheck += 1
							if alreadyCheck == len(mirrors[twoWayPreRandomList[0]]['exits']):
								deadEndTwoWayPreRandomList.append(twoWayPreRandomList[0])
								random.shuffle(deadEndTwoWayPreRandomList)
								del twoWayPreRandomList[0]
							else:
								isGoodCheck = True
				
				if not currentPick in alreadyRandomized:
					alreadyRandomized.append(currentPick)
					if mirrors[currentPick]['type'][0] == 0:
						if len(oneWayPreRandomList) > 0:
							for x in mirrors[oneWayPreRandomList[0]]['exits']:
								if not x in alreadyRandomized:
									queueList.append(x)
							mirrorlistRandomized[currentPickId] = oneWayPreRandomList[0]
							del oneWayPreRandomList[0]
						else:
							mirrorlistRandomized[currentPickId] = deadEndOneWayPreRandomList[0]
							del deadEndOneWayPreRandomList[0]
					else:
						#Do some more tests as to whether or not the possible pair is a dead end or not.
						deadendTest = False
						while deadendTest == False:
							if len(twoWayPreRandomList) == 0:
								deadendTest = True
							else:
								deadEndCount = 0
								for x in mirrors[twoWayPreRandomList[0]]['exits']:
									if x in alreadyRandomized:
										deadEndCount += 1
								if deadEndCount == len(mirrors[twoWayPreRandomList[0]]['exits']):
									deadEndTwoWayPreRandomList.append(twoWayPreRandomList[0])
									del twoWayPreRandomList[0]
								else:
									deadendTest = True
							
						if len(twoWayPreRandomList) > 0:
							while twoWayPreRandomList[0] == findLinkedMirror(currentPick):
								random.shuffle(twoWayPreRandomList)
							for x in mirrors[twoWayPreRandomList[0]]['exits']:
								if not x in alreadyRandomized:
									queueList.append(x)
							mirrorlistRandomized[currentPickId] = twoWayPreRandomList[0]
							mirrorlistRandomized[mirrorlist.index(findLinkedMirror(twoWayPreRandomList[0]))] = findLinkedMirror(currentPick)
							alreadyRandomized.append(mirrorlist[mirrorlist.index(findLinkedMirror(twoWayPreRandomList[0]))])
							if findLinkedMirror(currentPick) in twoWayPreRandomList:
								twoWayPreRandomList.remove(findLinkedMirror(currentPick))
							else:
								deadEndTwoWayPreRandomList.remove(findLinkedMirror(currentPick))
							del twoWayPreRandomList[0]
						else:
							while deadEndTwoWayPreRandomList[0] == findLinkedMirror(currentPick):
								random.shuffle(deadEndTwoWayPreRandomList)
							mirrorlistRandomized[currentPickId] = deadEndTwoWayPreRandomList[0]
							mirrorlistRandomized[mirrorlist.index(findLinkedMirror(deadEndTwoWayPreRandomList[0]))] = findLinkedMirror(currentPick)
							alreadyRandomized.append(mirrorlist[mirrorlist.index(findLinkedMirror(deadEndTwoWayPreRandomList[0]))])
							
							deadEndTwoWayPreRandomList.remove(findLinkedMirror(currentPick))
							del deadEndTwoWayPreRandomList[0]
			#This means the exit isn't scheduled to be randomized. Mark it as already randomized, but don't do anything with mirrorlistRandomized.
			else:
				if not currentPick in alreadyRandomized:
					alreadyRandomized.append(currentPick)
					for x in mirrors[currentPick]['exits']:
						if not x in alreadyRandomized:
							queueList.append(x)

			queueList.remove(currentPick)
			
			if len(queueList) == 0:
				for x in range(len(mirrorlistRandomized)):
					if mirrorlistRandomized[x] == "NULL":
						if mirrorlist[x] in alreadyRandomized:
							alreadyRandomized.remove(mirrorlist[x])
							print("ERROR: FOUND NULL")
						queueList.append(mirrorlist[x])

	print("Writing mirrors to ROM...")
	for x in range(len(mirrorlist)):
		#Location warps in Amazing Mirror have two places in the ROM to change, else it softlocks.
		#We need to change both of them, and there could be any number of addresses to write to
		#to change just one warp.
		location = removeBrackets(mirrors[mirrorlistRandomized[x]]['location'])
		for y in mirrors[mirrorlist[x]]['eightrom']:
			writeValueToRom(romFile,y,location,5)
		for z in mirrors[mirrorlist[x]]['ninerom']:
			writeValueToRom(romFile,z,(location >> 8),4)
	
	for x in range(len(mirrorList)):
		compareA = mirrorList[x]
		compareB = mirrorListRandomized[x]
		if mirrorList.index(findLincompareB):
			print("WARNING: FOUND TWO-WAY THAT DOES NOT LINK")
#==================================================
if __name__ == '__main__':
	#Make sure we have our arguments and validation and whatever.
	if len(sys.argv) < 5:
		print("Error: invalid number of arguments. Usage: amrMusic.py \"[path to file]\" [seed number] [don't random hub mirrors (0/1)] [total random mode (0/1)]")
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

	if sys.argv[3] != 0 or sys.argv[3] != 1:
		print("Error: Don't random hub mirrors setting must be a 0 or a 1 for Off on On.")
		sys.exit()
		
	if sys.argv[4] != 0 or sys.argv[4] != 1:
		print("Error: Total random setting must be a 0 or a 1 for Off on On.")
		sys.exit()

	katamrom = open(romFile,'rb+')
	random.seed(randomSeed)
	randomizeMirrors(katamrom,sys.argv[3],sys.argv[4])
	katamrom.close()