#This script randomizes the game's music.
#Music is randomized into two different groups: looped and non-looped. You don't want to get the victory dance theme as your Olive Ocean music...
import sys
import os
import random
#==================================================
def writeMusicToROM(romFile,musicList,musicAdd):
	for x in range(len(musicList)):
		romFile.seek(musicAdd[x])
		romFile.write(musicList[x].to_bytes(4,'big'))

def randomizeMusic(romFile,randomMode):
	print("Randomizing music...")
	#First shuffle the looped music.
	if randomMode == "Shuffle Music":
		musicLoopedList = [1422774280, 4107259912, 2362888200, 1155321864, 1357172744, 3975008264, 1090244616, 3422802184, 3288977672, 3692286216, 3223703816, 137548040, 808898824, 2957168904, 3830436104, 677302536, 1752027400, 679334152, 3766735112, 1820971272, 277795080, 1620168968, 1016320264, 3969437960, 2158153992, 3770011912, 2830749960, 1891422472]
	else:
		musicLoopedList = [1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608, 1080537608]
	musicLoopedAdd = [11686888, 11686896, 11686904, 11686912, 11686920, 11686928, 11686936, 11686944, 11686952, 11686960, 11686968, 11686976, 11686984, 11686992, 11687000, 11687008, 11687016, 11687024, 11687048, 11687072, 11687080, 11687088, 11687096, 11687104, 11687112, 11687160, 11687176, 11687184]
	random.shuffle(musicLoopedList)

	writeMusicToROM(romFile,musicLoopedList,musicLoopedAdd)
		
	#Then shuffle the non-looped music.
	if randomMode == "Shuffle Music":
		musicNonloopedList = [2222903560, 1618989320, 75944200, 948424968, 614846728, 78106888, 3634876680, 2024329480, 1219088648, 3770077448]
		musicNonloopedAdd = [11687032, 11687040, 11687056, 11687064, 11687120, 11687128, 11687136, 11687144, 11687152, 11687168]
		random.shuffle(musicNonloopedList)

		writeMusicToROM(romFile,musicNonloopedList,musicNonloopedAdd)
#==================================================