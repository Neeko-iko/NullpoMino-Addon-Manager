import os
import fnmatch
import re

SETTINGS = {
    # Dictionary of all settings with their default options, by category
    "Directories" : [
        ["NullpoMino Installation Folder", "C:\\NullpoMino\\res"],
        ["Custom Add-ons Folder", "none"],
        ["Custom Visuals Folder", "none"],
        ["Custom Sounds Folder", "none"]
    ],
    "Config (F = False | T = True)" : [
        ["Reset on next launch", "F"],
        ["Check for Blockskins", "T"]
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
        while not os.path.isdir(directory):
            if directory == "none":
                break
            else:
                directory = input("\nHey now, no funny business - give me the real directory.\n"
                "[if you made a mistake and entered a character by accident, enter nothing and it'll set you up with the defaults]\n"
                "[if you entered nothing and I'm yelling at you, you may not have the default directory - if there is one]\n")
            if directory == "" or directory.upper() == "NOTHING":
                directory = directorytype[1]

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
# Actual code:



print("Checking for config...")
try:
    configdata = readconfig()
    print("Config found! applying settings right now...")

except FileNotFoundError:
    print("No config found! That's no big deal. We'll get one set up, it'll only take a few minutes at most!")
    fullsetup()
    configdata = readconfig()

#print(configdata)
try:
    if configdata["Reset on next launch"] == "T":
        fullsetup()
    resFolder = configdata["NullpoMino Installation Folder"]
    custom = configdata["Custom Add-ons Folder"]
    visfolder = configdata["Custom Visuals Folder"]
    sefolder = configdata["Custom Sounds Folder"]
except KeyError:
    print("The config file seems corrupted. Let's fix this by going through the set up again.")
    fullsetup()
    configdata = readconfig()
    resFolder = configdata["NullpoMino Installation Folder"]
    custom = configdata["Custom Add-ons Folder"]
    visfolder = configdata["Custom Visuals Folder"]
    sefolder = configdata["Custom Sounds Folder"]

if custom.upper() == "NONE":
    custom = ""
else:
    custom = custom + "\\"
print("Checking Folders...")
if configdata["Check for Blockskins"] == "T":
    if os.path.isdir(custom + "blockskin") == False:
        permission = input("There isn't a 'blockskin' folder in your custom directory \n\nis it okay if I create one? - Y/N \n" 
        "If you say 'no', I won't ask you again, and I won't check for blockskins on launch. \n\n if you say 'yes' i will create one and check it for blockskins\n")

        if permission[0].upper == "N":
            print("Alrighty, I won't bother you about blockskins anymore - Lemme just update your prefernces really fast...")
            configdata["Check for Blockskins"] = "F"
            writeconfig(configdata)
        else:
            print("Thanks! I'll make sure to add one right now.")
            # Create the folder, instead of lie ##
            os.mkdir(custom + "blockskin")
    """
        #   Checks the different sized folders to make sure they exist, if they do, add them
    for size in sizes:
        if not os.path.isdir(f"{custom}blockskin{size}"):
            os.mkdir(f"{custom}blockskin{size}")

        #   Checks for any new files in the custom blockskin folders
        
    consistent = []
    for size in sizes:
        consistent.append(True if len((fnmatch.filter(os.listdir(f"{custom}blockskin{size}"), '*.png'))) != 0 else False)

    if consistent == [False, False, False]:
        print("No new blockskins were found")

    elif consistent == [True, True, True]:
        print("new blockskins found!")
        BlockskinAdd()
        """
    NullSkinPath = resFolder + "\\graphics\\blockskin"
    NullSkinNum = len(fnmatch.filter(os.listdir(NullSkinPath + "\\normal"), '*.png'))
    print(f"Detected {NullSkinNum} blockskins in NullpoMino folder.")
    for dir in os.listdir(custom + "blockskin"):
        workingDir = custom + "blockskin\\" + dir
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
                    permission = input("Do you want to add the blockskin to NullpoMino anyway? (Y/N)").upper()
                if permission == "N":
                    print("Aighty! I'll leave them be.")
                else:
                    print("okay, I'll try, don't blame me if NullpoMino stops working for whatever reason..")
                    BlockskinMove(workingDir, NullSkinNum, NullSkinPath)
                    NullSkinNum += 1
# 