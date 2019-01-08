import os
import fnmatch
def fullsetup():
    print("Starting set-up routine...")
    configfile = open("config.txt", "w+")
    configfile.write("Directories:\n")
        #   asks where stuff is
    for directorytype in ["please copy-paste your NullpoMino directory (NOT YOUR RES FOLDER) \n[Enter nothing for the default]\n Adder NullpoMino res Folder: Default C:\\NullpoMino\\res", "please copy-paste your NullpoMino add-on folder (IF YOU HAVE ONE) \n[Enter nothing for the default]\n Adder Custom Add-ons Folder: Default None"]:
            directory = input(directorytype[:99])
                #   Checks for if the user says literally nothing
            if directory == "" or directory.upper() == "NOTHING":
                directory = directorytype[106:128] + directorytype[136:]
            else:
                directory = directorytype[106:129] + directory
            configfile.write(directory + "\n")
    if directory[-4:].upper() == "NONE":
        configfile.write("Visual Folder: Skins\nSounds Folder: Sound Effects")
    else:
        #   Asks what your visual folder and sound folders are called, if you have them.
        for directorytype in ["What's the name of your graphics folder?\nAdder Visual Folder: ", "What's the name of your sounds folder?\n  Adder Sounds Folder: "]:
            directory = input(directorytype[:41])
            directory = directorytype[47:62] + directory
            configfile.write(directory + "\n")
    configfile.write("\nConfig:  (F = False | T = True)\nReset on next launch = F\nCheck for Blockskins = T")

print("Checking for config...")
try:
    configfile = open("config.txt", "r")
    print("Config found! applying settings right now...")

except FileNotFoundError:
    print("No config found! That's no big deal. We'll get one set up, it'll only take a few minutes at most!")
    fullsetup()
if configdata[7][25] = "T":
    fullsetup()
configdata = configfile.readlines
resFolder = configdata[1][24:]
custom = configdata[2][24:]
visfolder = configdata[3][15:]
sefolder = configdata[4][15:]
configfile.close

if custom.upper != "NONE":
    custom = custom + "\\"
print("Checking Folders...")
if configdata[8][40] = "T":
    if os.path.isdir(custom + "blockskin") == False:
        permission = input("There isn't a 'blockskin' folder in your custom directory \n\nwould you mind if I created one? - Y/N \n If you say 'no', I won't ask you again, and I won't check for blockskins on launch. \n\n if you say 'yes' i will create one and check it for blockskins")
        if permission[0].upper == "N":
            print("Alrighty, I won't bother you about blockskins anymore - Lemme just update your prefernces really fast...")
            configdata[8] = "Check for Blockskins = F\n"
            configfile = open("config.txt" "w+")
            configfile.write(configdata)
            configfile.close
        else:
            print("Thanks! I'll make sure to add one right away.")
    

        #   Checks for any new files in the custom blockskin folder (Only does a check through normal blockskins)

if len((fnmatch.filter(os.listdir(custom + "blockskin\\normal"), '*.png'))) == 0:
    print("No new blockskins found")
else:
    print("new blockskins found!")
            #   grabs blockskin count
    BSkinpath = resFolder + "\\graphics\\blockskin\\normal"
    NumBSkins = len((fnmatch.filter(os.listdir(BSkinpath), '*.png')))
    print('Found ' + str(len((fnmatch.filter(os.listdir(custom + "blockskin\\normal"), '*.png')))) + ' blockskins!')

            #   edits the blockskins in their folders to be sequential to what NullpoMino has
    for size in ["\\small", "\\normal", "\\big"]:

        print("Editing the "+ size[1:] + " blockskins...")

        num = NumBSkins
        skinpath = custom + "blockskin\\" + size
        #for fileName in os.listdir(skinpath):
            #os.renames(fileName, fileName.replace(skinpath[11], skinpath[11] + str(num)))
        print("Finished Editing the " + size[1:] + " blockskins")