import os
import fnmatch
import re
import shutil
import tkinter
from tkinter import *
import random
SETTINGS = {
    # Dictionary of all settings with their default options, by category
    "Directories" : [
        ["NullpoMino Installation Folder", "C:\\NullpoMino"],
        ["Custom Blockskins Folder", "blockskin"],
        ["Custom Visuals Folder", "Skins"],
        ["Custom Sounds Folder", "Sound Effects"],
        ["Custom Font Folder", "Fonts"],
        ["Custom Imports Folder", "Imports"]
    ],
    "Config (F = False | T = True)" : [
        ["Reconfigure on next launch", "F"],
        ["Check for Blockskins", "T"],
        ["Delete Logs and Replays without archiving", "F"],
        ["GUI (Can be: (V)Dark, Light, or None)", "Dark"],
        ["Random Icons & Titles upon startup", "T"]
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

def resourceArch(origin, output):
    if configdata["Delete Logs and Replays without archiving"] != "T":
        shutil.make_archive(output, 'zip', origin)
    removelist = os.listdir(origin)
    for file in removelist:
        os.remove(f"{origin}\\{file}")



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
    importfolder = configdata["Custom Imports Folder"]
    nullFolder = configdata["NullpoMino Installation Folder"]
    GUI = configdata["GUI (Can be: (V)Dark, Light, or None)"]
except KeyError:
    print("The config file seems corrupted. Let's fix this by going through the set up again.")
    fullsetup()
    configdata = readconfig()
    resFolder = configdata["NullpoMino Installation Folder"] + "\\res"
    blockFolder = configdata["Custom Blockskins Folder"]
    visfolder = configdata["Custom Visuals Folder"]
    sefolder = configdata["Custom Sounds Folder"]
    fontfolder = configdata["Custom Font Folder"]
    importfolder = configdata["Custom Imports Folder"]
    nullFolder = configdata["NullpoMino Installation Folder"]
    GUI = configdata["GUI (Can be: (V)Dark, Light, or None)"]





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
        workingDir = f"{blockFolder}{dir}"
        print(workingDir)
        if os.path.isdir(workingDir):
            consistent = [os.path.exists(f"{workingDir}{s}.png") for s in sizes]
            print(consistent)
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
                if permission.upper() == "N":
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
#Code and Classic User Interface
#
# The Classic User Interace uses the console to communcate to the user.
#
# Unlike the Newer GUI, which allows the user to click stuff to do things, it makes it more user friendly c:

#  You're Welcome! - Neeky Weeky

if GUI == None:
    selection = None

    print("You seem to have downloaded the 'Master Branch' off of github\n"
    "And that's fine! but if something breaks, or you have any ideas for what to add - please contact Neeko#3370")
    while selection != "":
        selection = input("Would you like to \nMove things?[MOVE] \nArchive things?[EXTRACT]\n\n").upper()
        selection = selection + " "
        if selection[0] == "M":
            while True:
                choice = None
                dirSel = None
                selection = input("Enter what you'd like to do! [Type anything other than what is listed to go back!]\n\n"
                    "Move Visuals(V), Sounds(S), or Fonts(F) Import .ruls/.reps(I) from the Imports folder\n\n").upper()
                selection = selection + " "
                
                if selection[0] == "V":
                    resList = os.listdir(visfolder)
                    while dirSel not in resList:
                        dirSel = input("Please select a skintype\n\n" + ", ".join(resList) + "\n\n")
                    resourceMove(f"{visfolder}\\{dirSel}", f"{resFolder}\\graphics")

                elif selection[0] == "S":
                    resList = os.listdir(sefolder)
                    while dirSel not in resList:
                        dirSel = input("Please select a soundpack\n\n" + ", ".join(resList) + "\n\n")
                    resourceMove(f"{sefolder}\\{dirSel}", f"{resFolder}\\se")
                
                elif selection[0] == "F":
                    resList = os.listdir(fontfolder)
                    while dirSel not in resList:
                        dirSel = input("Please select a font \n[you don't need to write the .ttf]\n\n" + ", ".join(resList) + "\n\n")
                        if dirSel[-4:] != ".ttf":
                            dirSel = dirSel + ".ttf"
                    os.remove(f"{resFolder}\\font\\font.ttf")
                    shutil.copy2(f"{fontfolder}\\{dirSel}", f"{resFolder}\\font\\font.ttf")
                
                elif selection[0] == "I":
                    itemList = os.listdir(importfolder)
                    if len(itemList) == 0:
                        print("There's nothing in here!!!")
                    else:
                        print("OwO there's stuff in here lemme add it all really quickly")
                        for file in itemList:
                            if file[-4:] == ".rul":
                                shutil.copy2(f"{importfolder}\\{file}", f"{nullFolder}\\config\\rule")
                                print("added a .rul (rule file)")
                            if file[-4:] == ".rep":
                                shutil.copy2(f"{importfolder}\\{file}", f"{nullFolder}\\replay")
                                print("added a .rep (replay file)")
                            os.remove(f"{importfolder}\\{file}")

                else:
                    print("That's not an option!\nGoing back!")
                    break

    #"Archive Replays(R), Netplay Chat Logs(L) or Screenshots(P) into a ZIP \n(will be located in the same folder as the script.) \n"
    #                   "[WILL DELETE THE FILES YOU SELECT FROM YOUR NULLPOMINO FOLDER]\n\n"
        elif selection[0] == "E":
            while True:
                permission = None
                selection = input("Archive Replays(R), Netplay Chat Logs(L) or Screenshots(S) into a ZIP\n"
                "\n(will be located in the same folder as the script.) \n"
                "[WILL DELETE THE FILES YOU SELECT FROM YOUR NULLPOMINO FOLDER]\n\n"
                "Extract .ruls(E) into a ZIP[WON'T DELETE CURRENT ONES] \nEnter anything apart from this and you'll go back!\n\n").upper()
                selection = selection + " "

                if selection[0] == "R":
                    while permission != "Y" and permission != "N":
                        permission = input("Are you sure you want to archive your replays? (Y/N) \n [REMINDER: IT WILL REMOVE THE ONES IN YOUR NULLPOMINO FOLDER.] \n\n").upper()
                    if permission == "Y":
                        print("Alrighty!")
                        resourceArch(f"{nullFolder}\\replay", "replyArchive [MOVE BEFORE MAKING ANOTHER]")

                elif selection[0] == "L":
                    while permission != "Y" and permission != "N":
                        permission = input("Are you sure you want to archive your Netplay Chat Logs? (Y/N) \n [REMINDER: IT WILL REMOVE THE ONES IN YOUR NULLPOMINO FOLDER.] \n\n").upper()
                    if permission == "Y":
                        print("Alrighty!")
                        resourceArch(f"{nullFolder}\\log", "logArchive [MOVE BEFORE MAKING ANOTHER]")

                elif selection[0] == "S":
                    while permission != "Y" and permission != "N":
                        permission = input("Are you sure you want to archive your Screenshots? (Y/N) \n [REMINDER: IT WILL REMOVE THE ONES IN YOUR NULLPOMINO FOLDER.] \n\n").upper()
                    if permission == "Y":
                        print("Alrighty!")
                        resourceArch(f"{nullFolder}\\ss", "SShotArchive [MOVE BEFORE MAKING ANOTHER]")
                
                elif selection[0] == "E":
                    shutil.make_archive("Rules", 'zip', f"{nullFolder}\\config\\rule")
                    print("okay done! it will be located where the script is located!")
                else:
                    print("you goose! that's not an option! Back we goooooooooo!!!")
                    break


        else:
            print("That's not an option, silly!")

else:
    if GUI == "Dark":
        bgcolor = "Gray"
        textcolor = "White"
    elif GUI == "VDark":
        bgcolor = "Black"
        textcolor = "White"
    else:
        bgcolor = "White"
        textcolor = "Black"
    root = Tk()
    if configdata["Random Icons & Titles upon startup"] == "T":
        root.iconbitmap("./!Manager GUI/icons/icon" +str(random.randint(1,len(os.listdir("./!Manager GUI/icons")))) + ".ico")
        windowtitle = open("./!Manager GUI/WindowTitles.txt", "r")
        titlelist = windowtitle.readlines()
        windowtitle.close()
        windowtitle = titlelist[random.randint(0, (len(titlelist)-1))]
        #if "\n" in windowtitle:
        #    windowtitle.strip(-1)
        root.title("NMAOM: " +windowtitle)
    else:
        root.iconbitmap("./!Manager GUI/icons/icon4")
        root.title("NullpoMino Add-on Manager")

        
    root.minsize(500, 400)
    root.configure(bg = bgcolor)



    root.mainloop()
