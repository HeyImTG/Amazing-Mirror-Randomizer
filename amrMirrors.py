#This script ranadomizes the mirrors, cannons, and warp starts.
import random
import os
import json

from amrShared import writeValueToRom, removeBrackets
#==================================================
def findLinkedMirror(string):
	underscore = string.find("_")
	return string[underscore+1:len(string)] + "_" + string[0:underscore]

def randomizeMirrors(romFile,hubMirrors,totalRandom):
	mirrors = json.load(open('JSON\mirrors.json'))
	mirrorlist = list(mirrors.keys())

	#Remove the some rooms from the randomizer.
	mirrorlist.remove("Int1_Int2")
	mirrorlist.remove("Int2_Int3")
	mirrorlist.remove("Int3_Int2")
	mirrorlist.remove("Car19_Reset") #Cause it's fucking aggrivating
	 
	#Don't randomize the hub mirrors?
	if hubMirrors == 1:
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
	warpstaradds = [ [ 8944554, 8944566 ], [ 8964698, 8964710 ], [ 8981034, 8981046 ], [ 8998010, 8998022 ], [ 9006434, 9006446 ], [ 9065234, 9065246 ] ]
	warpstarvalues = [ [ 0, 277076896629504 ], [ 4, 69269484247297 ], [ 1, 12094879601665 ], [ 2, 281471017324801 ], [ 3, 5497809837825 ], [ 5, 281470681800192 ] ]
	
	random.shuffle(warpstarvalues)
	for x in range(len(warpstaradds)):
		writeValueToRom(romFile,warpstaradds[x][0],warpstarvalues[x][0],1)
		writeValueToRom(romFile,warpstaradds[x][1],warpstarvalues[x][1],6)
		
	#Randomize fused cannons.
	cannonadds = [ 8951430, 8999618, 9033722, 9050022 ]
	cannonvalues = [ 4179903404153243910, 3170817811668802562, 9583663305579299867, 937313871469740802 ]
	
	random.shuffle(cannonvalues)
	for x in range(len(cannonadds)):
		writeValueToRom(romFile,cannonadds[x],cannonvalues[x],8)
	
	#Randomize Mirrors
	if totalRandom == 0:
		onewaylist = mirrorlist.copy()
		twowaylist = mirrorlist.copy()
		
		#Sort the mirrors by type.
		for x in mirrorlist:
			if mirrors[x]['type'] == [1]:
				onewaylist.remove(x)
			else:
				twowaylist.remove(x)
		
		twowayrandom = twowaylist.copy()
		onewayrandom = onewaylist.copy()

		#Do a really basic shuffle.
		print("Randomizing mirrors...")
		random.shuffle(onewayrandom)
		random.shuffle(twowayrandom)
		onewaycount = 0
		twowaycount = 0
		
		print("Making sure the first hub mirror isn't bad...")
		while removeBrackets(mirrors[onewayrandom[0]]['type']) != 3:
			random.shuffle(onewayrandom)
		
		print("Pairing two-way mirrors...")
		#Make it so that two way mirrors "go back on each other".
		#Randomize one two-way mirror as normal, then find it's "pair" but using findLinkedMirror.
		#Then put the linked mirrors next to each other in the randomized lists.
		for x in range(int(len(twowaylist) / 2)):
			listvalue = findLinkedMirror(twowayrandom[x*2])
			randomvalue = findLinkedMirror(twowaylist[x*2])
			
			listswap = twowaylist.index(listvalue)
			randomswap = twowayrandom.index(randomvalue)
			
			twowayrandom[randomswap] = twowayrandom[(x*2)+1]
			twowaylist[listswap] = twowaylist[(x*2)+1]
			twowayrandom[(x*2)+1] = randomvalue
			twowaylist[(x*2)+1] = listvalue
			
			#Make it so that a two-way mirror doesn't send you back to itself.
			if twowaylist[x*2] == twowayrandom[x*2] and twowaylist[(x*2)+1] == twowayrandom[(x*2)+1]:
				listswap = twowayrandom[(x*2)+1]
				twowayrandom[(x*2)+1] = twowaylist[x*2]
				twowaylist[x*2] = listswap
		
		print("Writing two-way mirrors to ROM...")
		for x in range(len(twowaylist)):
			location = removeBrackets(mirrors[twowayrandom[x]]['location'])
			for y in mirrors[twowaylist[x]]['eightrom']:
				writeValueToRom(romFile,y,location,4)
			for z in mirrors[twowaylist[x]]['ninerom']:
				writeValueToRom(romFile,z,location,4)

		print("Writing one-way mirrors to ROM...")
		for x in range(len(onewaylist)):
			location = removeBrackets(mirrors[onewayrandom[x]]['location'])
			for y in mirrors[onewaylist[x]]['eightrom']:
				writeValueToRom(romFile,y,location,4)
			for z in mirrors[onewaylist[x]]['ninerom']:
				writeValueToRom(romFile,z,location,4)
	else:
		print("Randomizing mirrors...")
		randomizedlist = mirrorlist.copy()
		#Do a really basic shuffle.
		random.shuffle(randomizedlist)
		
		print("Making sure the first hub mirror isn't bad...")
		while removeBrackets(mirrors[randomizedlist[0]]['type']) != 3:
			random.shuffle(randomizedlist)
		
		for x in range(len(randomizedlist)):
			#Location warps in Amazing Mirror have two places in the ROM to change, else it softlocks.
			#We need to change both of them, and there could be any number of addresses to write to
			#to change just one warp.
			location = removeBrackets(mirrors[randomizedlist[x]]['location'])
			for y in mirrors[mirrorlist[x]]['eightrom']:
				writeValueToRom(romFile,y,location,4)
			for z in mirrors[mirrorlist[x]]['ninerom']:
				writeValueToRom(romFile,z,location,4)
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