#The GUI for the randomizer.
from tkinter import filedialog
from tkinter import *
import random
import os
import json

from amrMirrors import *
from amrItems import *
from amrStands import *
from amrSpray import *
from amrMusic import *
#==================================================
#This gets around how py2exe handles included files.
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Open a file dialog and ask for the JP KatAM ROM.
def openROM():
	filepath = filedialog.askopenfilename(filetypes=[("GBA Roms", (".gba")), ("All Files", "*")])
	if filepath != '':
		filepath = filepath.replace('/','\\')
		entry_path_to_rom.delete(0,END)
		entry_path_to_rom.insert(END,filepath)

#Open a file dialog and ask for where to put the randomized ROM.
def openDirectory():
	filepath = filedialog.askdirectory(initialdir = os.getcwd())
	if filepath != '':
		filepath = filepath.replace('/','\\')
		entry_path_to_output.delete(0,END)
		entry_path_to_output.insert(END,filepath)

#Update the advanced "Random Mirror" settings checkboxes.
def checkMirrorSettings():
	if mirrorcheck.get() == 0:
		check_randomize_totalrandom.deselect()
		check_randomize_hubmirrors.deselect()
		check_randomize_totalrandom.config(state=DISABLED)
		check_randomize_hubmirrors.config(state=DISABLED)
	else:
		check_randomize_totalrandom.config(state=NORMAL)
		check_randomize_hubmirrors.config(state=NORMAL)

#Produce a random seed number.
def getRandomSeed():
	entry_seed_number.delete(0,END) 
	entry_seed_number.insert(END,str(random.randint(0,999999)))
	
#Double check if everything is good to go before pulling the trigger.
def validateSettings():
	is_valid = True

	if os.path.isfile("JSON\items.json") == False:
		is_valid = False
		warning_label.config(text="Error: items.json not found!", fg="#FF0000")
		
	if os.path.isfile("JSON\mirrors.json") == False:
		is_valid = False
		warning_label.config(text="Error: mirrors.json not found!", fg="#FF0000")
	
	try:
		optionSeedNumber = int(entry_seed_number.get())
	except ValueError:
		is_valid = False
		warning_label.config(text="Error: The seed must only conatin numbers.", fg="#FF0000")
	
	outputdir = entry_path_to_output.get()
	inputrom = entry_path_to_rom.get()

	if outputdir == "":
		is_valid = False
		warning_label.config(text="Error: No output directory specified.", fg="#FF0000")
	elif os.path.isdir(outputdir) == False:
		is_valid = False
		warning_label.config(text="Error: Output directory does not exist.", fg="#FF0000")

	if inputrom == "":
		is_valid = False
		warning_label.config(text="Error: No input ROM specified.", fg="#FF0000")
	elif os.path.isfile(inputrom) == False:
		is_valid = False
		warning_label.config(text="Error: Input ROM does not exist.", fg="#FF0000")
	else:
		filecheck = open(inputrom,'rb')
		filecheck.seek(160)
		if filecheck.read(16) != b'AGB KIRBY AMB8KJ':
			is_valid = False
			warning_label.config(text="Error: File given is not an Japanese Amazing Mirror ROM.", fg="#FF0000")
		
	if is_valid == True:
		outputrom = outputdir + "\Amazing Mirror " + str(optionSeedNumber) + ".gba"
		generateROM(inputrom,outputrom)
		
def generateROM(originalrom,randomizedrom):
	optionSeedNumber = entry_seed_number.get()
	optionMirrors = mirrorcheck.get()
	optionMirrorsDontRandomizeHub = mirrorhub.get()
	optionMirrorsTotalRandom = mirrortotalcheck.get()
	optionItems = itemcheck.get()
	optionAbilityStands = abilitycheck.get()
	optionMusic = musiccheck.get()
	optionColours = palettecheck.get()
	
	os.system('copy "%s" "%s"' % (originalrom,randomizedrom))
	katamrom = open(randomizedrom,'rb+')
	random.seed(optionSeedNumber)

	#Randomize the items?
	if optionMirrors == 1:
		randomizeMirrors(katamrom,optionMirrorsDontRandomizeHub,optionMirrorsTotalRandom)
	
	#Randomize the items?
	if optionItems == 1:
		print("Randomizing chests and items...")
		randomizeItems(katamrom)
	
	#Randomize the ability stands?
	if optionAbilityStands == 1:
		print("Randomizing ability stands...")
		randomizeStands(katamrom)
	
	#Randomize the spray palettes?
	if optionColours == 1:
		print("Randomizing spray colours...")
		randomizeSpray(katamrom)

	#Randomize the music?
	if optionMusic == 1:
		print("Randomizing music...")
		randomizeMusic(katamrom)

	print("Done.")
	warning_label.config(text="ROM randomized. Enjoy your game!", fg="#000000")
#==================================================
#GUI time.
random.seed()

randomizer_window = Tk()
randomizer_window.title("KatAM JP Randomizer")
randomizer_window.resizable(False, False)

randomizer_window.iconbitmap(resource_path("katamrando.ico"))

randomizer_window["padx"] = 14
randomizer_window["pady"] = 14

abilitycheck = IntVar()
itemcheck = IntVar()
mirrorcheck = IntVar()
mirrortotalcheck = IntVar()
mirrorhub = IntVar()
musiccheck = IntVar()
palettecheck = IntVar()

#Set up our frames.
frame_get_rom = Frame(randomizer_window)
frame_get_rom.pack()
frame_seed_number = Frame(randomizer_window)
frame_seed_number.pack()
frame_options = Frame(randomizer_window)
frame_options.pack()
frame_generate_rom = Frame(randomizer_window)
frame_generate_rom.pack()

#File paths section.
Label(frame_get_rom, text="Path to ROM:").grid(row=0,column=0,sticky=E)

entry_path_to_rom = Entry(frame_get_rom)
entry_path_to_rom.config(width=50)
entry_path_to_rom.grid(row=0,column=1)

get_file_button = Button(frame_get_rom, text="...", command=openROM)
get_file_button.grid(row=0,column=2)

Label(frame_get_rom, text="Output dir:").grid(row=1,column=0,sticky=E)

entry_path_to_output = Entry(frame_get_rom)
entry_path_to_output.config(width=50)
entry_path_to_output.grid(row=1,column=1)

get_directory_button = Button(frame_get_rom, text="...", command=openDirectory)
get_directory_button.grid(row=1,column=2)

#Random seed section.
Label(frame_seed_number, text="Seed:").grid(row=0,column=0,sticky=E,pady=6)

entry_seed_number = Entry(frame_seed_number)
entry_seed_number.config(width=10)
entry_seed_number.grid(row=0,column=1,sticky=E)
entry_seed_number.insert(END,str(random.randint(0,999999)))

random_seed_button = Button(frame_seed_number, text="?", command=getRandomSeed)
random_seed_button.grid(row=0,column=2)

#Options section.
check_randomize_mirrors = Checkbutton(frame_options, text="Randomize mirrors.", variable=mirrorcheck, command=checkMirrorSettings)
check_randomize_mirrors.grid(row=0, column=0, sticky=W)

Label(frame_options, text="Mirror options:").grid(row=1,column=0,sticky=W)

check_randomize_totalrandom = Checkbutton(frame_options, text="Total random mode.", variable=mirrortotalcheck, state=DISABLED)
check_randomize_totalrandom.grid(row=2, column=0, sticky=W)

check_randomize_hubmirrors = Checkbutton(frame_options, text="Don't randomize hub mirrors.", variable=mirrorhub, state=DISABLED)
check_randomize_hubmirrors.grid(row=3, column=0, sticky=W)

check_randomize_items = Checkbutton(frame_options, text="Randomize chests and items.", variable=itemcheck)
check_randomize_items.grid(row=0, column=1, sticky=W)

check_randomize_stands = Checkbutton(frame_options, text="Randomize ability stands.", variable=abilitycheck)
check_randomize_stands.grid(row=1, column=1, sticky=W)

check_randomize_music = Checkbutton(frame_options, text="Randomize spray palettes.", variable=palettecheck)
check_randomize_music.grid(row=2, column=1, sticky=W)

check_randomize_music = Checkbutton(frame_options, text="Randomize music.", variable=musiccheck)
check_randomize_music.grid(row=3, column=1, sticky=W)

#Generate ROM section.
generate_button = Button(frame_generate_rom, text="Generate ROM",command=validateSettings)
generate_button.grid(row=0, pady=6)

warning_label = Label(frame_generate_rom, text="Please view the readme for info about the different settings.")
warning_label.grid(row=1)

Label(frame_generate_rom, text="KatAM Randomizer V.05-15-2019").grid(row=2)

randomizer_window.mainloop()