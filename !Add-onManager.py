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

        #   Checks the different sized folders to make sure they exist, if they do, add them
    for size in ["\\small", "\\normal", "\\big"]: 
        ''

        #   Checks for any new files in the custom blockskin folders
    consistent = []
    for size in sizes:
        consistent.append(True if len((fnmatch.filter(os.listdir(f"{custom}blockskin{size}"), '*.png'))) != 0 else False)

    if True: ###Replace with a check to see if "consistent" is filled with False:
        print("No new blockskins were found")

    elif True: ###Replace with a check to see if "consistent" is filled with True:
        print("new blockskins found!")
        
                #   grabs blockskin count
        BSkinpath = resFolder + "\\graphics\\blockskin\\normal"
        NumBSkins = len((fnmatch.filter(os.listdir(BSkinpath), '*.png')))
        print('Found ' + str(len((fnmatch.filter(os.listdir(custom + "blockskin\\normal"), '*.png')))) + ' blockskins!')

                #   edits the blockskins in their folders to be sequential to what NullpoMino has
        for size in ["\\small", "\\normal", "\\big"]:

            num = NumBSkins
            skinpath = custom + "blockskin\\" + size
            #for fileName in os.listdir(skinpath):
                #os.renames(fileName, fileName.replace(skinpath[11], skinpath[11] + str(num)))

    else:
        ###Might want to make another function for the blockskin stuff
        print("whopsies")
# 