import os
import fnmatch
import re
import shutil
SETTINGS = {
    # Dictionary of all settings with their default options, by category
    "Directories" : [
        ["NullpoMino Installation Folder", "C:\\NullpoMino"],
        ["Custom Blockskins Folder", "blockskin"],
        ["Custom Visuals Folder", "Skins"],
        ["Custom Sounds Folder", "Sound Effects"],
        ["Custom Font Folder", "Fonts"]
    ],
    "Config (F = False | T = True)" : [
        ["Reconfigure on next launch", "F"],
        ["Check for Blockskins", "T"],
        ["Use DEV [experimental] features", "F"],
        ["[DEV] Delete Logs and Replays", "F"]
    ]
}
sizes = ["\\small", "\\normal", "\\big"]

##########################   Config Setup stuff   ############################

def fullsetup():
    print("Starting set-up routine...")
    configfile = open("config.txt", "w+")
    configfile.write("#Directories:\n")         #   Opens the config file and Immedietly dumps "Directories" in it
    for directorytype in SETTINGS["Directories"]:
        directory = input(
            "Please enter the full path to your {0}.\n[Enter nothing for the default ({1})] "
            .format(*directorytype)
        )
            #   Checks for if the user says literally nothing
        if directory == "" or directory.upper() == "NOTHING":
            directory = directorytype[1]
            try:
                os.mkdir(directory)
            except FileExistsError:
                ''
        while not os.path.isdir(directory):
            directory = input("\nHey now, no funny business - give me the real directory.\n"
            "[if you made a mistake and entered a character by accident, enter nothing and it'll set you up with the defaults]\n")
            if directory == "" or directory.upper() == "NOTHING":
                directory = directorytype[1]
                try:
                    os.mkdir(directory)
                except FileExistsError:
                    ''

        configfile.write("{0} = {1}\n".format(directorytype[0], directory))
    configfile.write("\n#Config (F = False | T = True)\n")
    for config in SETTINGS["Config (F = False | T = True)"]:
        configfile.write("{0} = {1}\n".format(*config))
    configfile.close()
    
def readconfig():
    configfile = open("config.txt", "r")
    match = re.findall(r"(?:([^#\n][^\n]*?)\s+=\s+([^\n]+))", configfile.read())
    dict = {}
    for key, val in match:
        dict[key] = val
    configfile.close()
    return dict

def writeconfig(config):
    configfile = open("config.txt", "w+")
    configfile.write("#Directories:\n")
    for directorytype in SETTINGS["Directories"]:
        configfile.write("{0} = {1}\n".format(directorytype[0], config[directorytype[0]]))
    configfile.write("#Config (F = False | T = True)\n")
    for settingtype in SETTINGS["Config (F = False | T = True)"]:
        configfile.write("{0} = {1}\n".format(settingtype[0], config[settingtype[0]]))
    configfile.close()
    

# ###############################################################

# #################  Function to add blockskins  ################
def BlockskinMove(origin, id, dest):
        #   edits the blockskins in their folders to be sequential to what NullpoMino has
    for size in sizes:
        os.renames(origin+size+".png", dest+size+size[0:2]+str(id)+".png")

# ##################################################################

def resourceMove(origin, dest):
    print(origin)
    itemList = os.listdir(origin)
    for file in itemList:
        if os.path.exists(f"{dest}\\{file}"):
            os.remove(f"{dest}\\{file}")
        shutil.copy2(f"{origin}\\{file}", f"{dest}\\{file}")



# Actual code:



print("Checking for config...")
try:
    configdata = readconfig()
    print("Config found! applying settings right now...")

except FileNotFoundError:
    print("No config found! That's no big deal. We'll get one set up, it'll only take a few minutes at most!")
    fullsetup()
    configdata = readconfig()

try:
    if configdata["Reconfigure on next launch"] == "T":
        fullsetup()
    resFolder = configdata["NullpoMino Installation Folder"] + "\\res"
    blockFolder = configdata["Custom Blockskins Folder"]
    visfolder = configdata["Custom Visuals Folder"]
    sefolder = configdata["Custom Sounds Folder"]
    fontfolder = configdata["Custom Font Folder"]
    experimental = configdata["Use DEV [experimental] features"]
except KeyError:
    print("The config file seems corrupted. Let's fix this by going through the set up again.")
    fullsetup()
    configdata = readconfig()
    resFolder = configdata["NullpoMino Installation Folder"] + "\\res"
    blockFolder = configdata["Custom Blockskins Folder"]
    visfolder = configdata["Custom Visuals Folder"]
    sefolder = configdata["Custom Sounds Folder"]
    fontfolder = configdata["Custom Font Folder"]
    experimental = configdata["Use DEV [experimental] features"]






if blockFolder.upper() == "NONE":
    blockFolder = ""
else:
    blockFolder = blockFolder + "\\"
print("Checking Folders...")
if configdata["Check for Blockskins"] == "T":
    NullSkinPath = resFolder + "\\graphics\\blockskin"
    NullSkinNum = len(fnmatch.filter(os.listdir(NullSkinPath + "\\normal"), '*.png'))
    print(f"Detected {NullSkinNum} blockskins in NullpoMino folder.")
    for dir in os.listdir(blockFolder):
        workingDir = f"{blockFolder}\\{dir}"
        # print(workingDir)
        if os.path.isdir(workingDir):
            consistent = [os.path.exists(f"{workingDir}{s}.png") for s in sizes]
            if consistent == [True, True, True]:
                print(f"Adding blockskin {dir}.")
                BlockskinMove(workingDir, NullSkinNum, NullSkinPath)
                NullSkinNum += 1
                for file in os.listdir(workingDir):
                    os.remove(f"{workingDir}\\{file}")
                os.rmdir(workingDir)
            elif consistent == [False, False, False]:
                print(f"Skipping empty blockskin {dir}.")
                for file in os.listdir(workingDir):
                    os.remove(f"{workingDir}\\{file}")
                os.rmdir(workingDir)
            else:
                print("There seems to be files missing in blockskin {dir}.")
                permission = ""
                while permission not in ["Y", "N"]:
                    permission = input("Do you want to add the blockskin to NullpoMino anyway? [Y/N]").upper()
                if permission == "N":
                    print("Aighty! I'll get rid of it.")
                    for file in os.listdir(workingDir):
                        os.remove(f"{workingDir}\\{file}")
                    os.rmdir(workingDir)
                else:
                    print("okay, I'll try, don't blame me if NullpoMino stops working for whatever reason..")
                    BlockskinMove(workingDir, NullSkinNum, NullSkinPath)
                    NullSkinNum += 1                    
                    for file in os.listdir(workingDir):
                        os.remove(f"{workingDir}\\{file}")
                    os.rmdir(workingDir)
# 
### Experimental Code and user interface
selection = None
if experimental.upper() == "T":

    print("Oh, the experimental stuff?  That's meant for the devs more than anything\n"
    "but that doesn't mean you can't use it if you want to\n"
    "just... don't expect everything to be super stable - if it crashes, let Neeko#3370 know on discord, thanks!\n")
    while selection != "":
        choice = None
        dirSel = None
        selection = input("Enter what you'd like to do! \n\n"
        "Move Visuals(V), Sounds(S), or Font(F) \n\nArchive Replays(R) or Netplay Chat Logs(L) into a ZIP [WILL DELETE THE ONES YOU CHOOSE FROM YOUR NULLPOMINO FOLDER]\n\n")


        if selection[0].upper() == "V":
            resList = os.listdir(visfolder)
            while dirSel not in resList:
                dirSel = input("Please select a skintype\n\n" + ", ".join(resList) + "\n\n")
            resourceMove(f"{visfolder}\\{dirSel}", f"{resFolder}\\graphics")

        if selection[0].upper() == "S":
            resList = os.listdir(sefolder)
            while dirSel not in resList:
                dirSel = input("Please select a soundpack\n\n" + ", ".join(resList) + "\n\n")
            resourceMove(f"{sefolder}\\{dirSel}", f"{resFolder}\\se")
        
        if selection[0].upper() == "F":
            resList = os.listdir(fontfolder)
            while dirSel not in resList:
                dirSel = input("Please select a font \n[you don't need to write the .ttf]\n\n" + ", ".join(resList) + "\n\n")
                if dirSel[-4:] != ".ttf":
                    dirSel = dirSel + ".ttf"
            os.remove(f"{resFolder}\\font\\font.ttf")
            shutil.copy2(f"{fontfolder}\\{dirSel}", f"{resFolder}\\font\\font.ttf")
                
            









## User interface.
else:
    choice = None
    dirSel = None
    while choice not in ["Y", "N"]:
        choice = input("Do you want to move visuals? [Y/N] \n\n").upper()
    if choice == "Y":
        resList = os.listdir(visfolder)
        while dirSel not in resList:
            dirSel = input("Please select a skintype\n\n" + ", ".join(resList) + "\n\n")
        resourceMove(f"{visfolder}\\{dirSel}", f"{resFolder}\\graphics")
    choice = None
    dirSel = None
    while choice not in ["Y", "N"]:
        choice = input("Do you want to move sounds? [Y/N] \n\n").upper()
    if choice == "Y":
        resList = os.listdir(sefolder)
        while dirSel not in resList:
            dirSel = input("Please select a skintype\n\n" + ", ".join(resList) + "\n\n")
        resourceMove(f"{sefolder}\\{dirSel}", f"{resFolder}\\se")