#This script randomizes the chests and items in the game.
#The data that keeps track of which rooms have treasures in them on the in-game map are intertwined with the mirror locations list.
#If we're randomizing the chests, we need to essentially make our own list in order for everything to work squeaky clean.
#It's ugly but it works.
import random
import os
import json
from amrShared import *
#==================================================
def chestlistAppend(list,room,value):
	if list[room][0] == 0:
		list[room][0] = value
	else:
		list[room].append(value)

def randomizeItems(romFile,randomMode):
	print("Randomizing chests and items...")
	items = json.load(open('JSON\items.json'))
	itemlist = []
	itemadd = []
	itemxy = []
	itemroom = []
	chestlist = []
	itemindex = 0
	itemRandomDistribution = [104449309671424, 104449309671424, 104449309671424, 104449309671424, 105548821299200, 105548821299200, 105548821299200, 105548821299200, 106648332926976, 106648332926976, 106648332926976, 107747844554752, 107747844554752, 108847356182528, 108847356182528, 109946867810304, 111046379438080]
	
	for x in range(287):
		chestlist.append([0])
	
	for x in items["BigChest"]["item"]:
		itemlist.append(x)
	for x in items["BigChest"]["address"]:
		itemadd.append(x)
	for x in items["BigChest"]["xy"]:
		itemxy.append(x)
	for x in items["BigChest"]["room"]:
		itemroom.append(x)

	for x in items["SmallChest"]["item"]:
		itemlist.append(x)
	for x in items["SmallChest"]["address"]:
		itemadd.append(x)
	for x in items["SmallChest"]["xy"]:
		itemxy.append(x)
	for x in items["SmallChest"]["room"]:
		itemroom.append(x)
		
	for x in items["Cherry"]["address"]:
		if randomMode == "Shuffle Items":
			itemlist.append(items["Cherry"]["item"][0])
		else:
			itemlist.append(random.choice(itemRandomDistribution))
		itemadd.append(x)
	for x in items["Cherry"]["xy"]:
		itemxy.append(x)
	for x in items["Cherry"]["room"]:
		itemroom.append(x)
		
	for x in items["Drink"]["address"]:
		if randomMode == "Shuffle Items":
			itemlist.append(items["Drink"]["item"][0])
		else:
			itemlist.append(random.choice(itemRandomDistribution))
		itemadd.append(x)
	for x in items["Drink"]["xy"]:
		itemxy.append(x)
	for x in items["Drink"]["room"]:
		itemroom.append(x)
	
	for x in items["Meat"]["address"]:
		if randomMode == "Shuffle Items":
			itemlist.append(items["Meat"]["item"][0])
		else:
			itemlist.append(random.choice(itemRandomDistribution))
		itemadd.append(x)
	for x in items["Meat"]["xy"]:
		itemxy.append(x)
	for x in items["Meat"]["room"]:
		itemroom.append(x)
		
	for x in items["Tomato"]["address"]:
		if randomMode == "Shuffle Items":
			itemlist.append(items["Tomato"]["item"][0])
		else:
			itemlist.append(random.choice(itemRandomDistribution))
		itemadd.append(x)
	for x in items["Tomato"]["xy"]:
		itemxy.append(x)
	for x in items["Tomato"]["room"]:
		itemroom.append(x)
		
	for x in items["Battery"]["address"]:
		if randomMode == "Shuffle Items":
			itemlist.append(items["Battery"]["item"][0])
		else:
			itemlist.append(random.choice(itemRandomDistribution))
		itemadd.append(x)
	for x in items["Battery"]["xy"]:
		itemxy.append(x)
	for x in items["Battery"]["room"]:
		itemroom.append(x)
		
	for x in items["1Up"]["address"]:
		if randomMode == "Shuffle Items":
			itemlist.append(items["1Up"]["item"][0])
		else:
			itemlist.append(random.choice(itemRandomDistribution))
		itemadd.append(x)
	for x in items["1Up"]["xy"]:
		itemxy.append(x)
	for x in items["1Up"]["room"]:
		itemroom.append(x)
		
	for x in items["Candy"]["address"]:
		if randomMode == "Shuffle Items":
			itemlist.append(items["Candy"]["item"][0])
		else:
			itemlist.append(random.choice(itemRandomDistribution))
		itemadd.append(x)
	for x in items["Candy"]["xy"]:
		itemxy.append(x)
	for x in items["Candy"]["room"]:
		itemroom.append(x)
		
	random.shuffle(itemlist)

	for x in range(len(itemadd)):
		writeValueToRom(romFile,itemadd[x],itemlist[x],6)
		
	#Add non-randomized chests to the lists (World map chest and passageway switches...because they're chests apparently).
	itemlist.extend([142932386250752, 142933880078354, 142933880078401, 142933880078410, 142933880078413])
	itemadd.extend([8933912, 8970772, 9032664, 9049580, 9056256])
	itemxy.extend([939810816, 3087036416, 671100928, 3355455488, 805326848])
	itemroom.extend([3, 81, 201, 238, 251]) 
	
	#Move the item list over one room, since the Test Room doesn't have an entry in the item list and that fucks things up.
	for x in range(len(itemroom)):
		if itemroom[x] >= 4:
			itemroom[x] += 1
	
	#Add the new XYs of the chests to the chestlist
	for x in items["SmallChest"]["item"]:
		itemindex = itemlist.index(x)
		chestlistAppend(chestlist,itemroom[itemindex],itemxy[itemindex])
		
	for x in items["BigChest"]["item"]:
		itemindex = itemlist.index(x)
		chestlistAppend(chestlist,itemroom[itemindex],itemxy[itemindex])
	
	for x in items["Unrandomized"]["item"]:
		itemindex = itemlist.index(x)
		chestlistAppend(chestlist,itemroom[itemindex],itemxy[itemindex])

	#Create a new 9ROM list of our own. Oh dear.
	eof = False
	olposition = 9441164 # "Original List" position.
	nlposition = 14745600 # "New List" position.
	nlroomstart = nlposition # We need to keep track of where the room begins so we can write our pointers.
	copydata = 0
	endofroom = False
	roomnumber = 0
	readvalue = 0
	chestcount = 0
	
	print("Creating new treasure table...")
	while eof == False:
		#First, check if we're done here.
		if olposition <= 9449747:
			#Reset these things.
			endofroom = False 
			chestcount = 0
			nlroomstart = nlposition

			#First, let's write our chests to the new list if the are any in this room we're on.
			if chestlist[roomnumber][0] != 0:
				chestcount = len(chestlist[roomnumber])
				for x in chestlist[roomnumber]:
					romFile.seek(nlposition)
					romFile.write(int(17367039).to_bytes(4,'big'))
					romFile.write(x.to_bytes(4,'big'))
					nlposition += 8
					
			#Now we copy the 02 08s.
			while endofroom == False:
				romFile.seek(olposition)
				readvalue = int.from_bytes(romFile.read(4),'big')
				
				if readvalue == 17367039:
					#If our readvalue is 01 08 FF FF, it's a chest. Skip it.
					olposition += 8
				elif readvalue == 34144255:
					#If our readvalue is 02 08 FF FF, it's a mirror. Copy it to the new list.
					romFile.seek(olposition)
					copydata = int.from_bytes(romFile.read(8),'big')
					romFile.seek(nlposition)
					romFile.write(copydata.to_bytes(8,'big'))
					nlposition += 8
					olposition += 8

				elif readvalue == 65535:
					#If our readvalue is 00 00 FF FF, it's the end of the room.
					olposition += 12
					romFile.seek(nlposition)
					romFile.write(int(65535).to_bytes(4,'big'))
					
					#We have to tell the game to look at this new list, so let's tinker with a pointer or two.
					nlposition += 4
					romFile.write(int(nlroomstart+134217728).to_bytes(4,'little'))
					
					#The list of pointers starts at 0xD2F4C0
					romFile.seek((13825216) + (4 * roomnumber))
					romFile.write(int(nlposition+134217728).to_bytes(4,'little'))
					nlposition += 4
					
					#Finally we have to write a byte counting how many chests are in this room.
					romFile.seek(nlposition)
					romFile.write(chestcount.to_bytes(1,'big'))
					nlposition += 4
					
					#Tick up the room counter and get us out of this loop!
					roomnumber += 1
					endofroom = True
		else:
			#Rangers lead the way.
			eof = True
#==================================================