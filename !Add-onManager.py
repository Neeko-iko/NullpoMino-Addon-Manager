import sys
import os
import fnmatch
puller = open("directories.txt", "r")
resFolder = puller.readline()
custom = puller.readline()
if custom == None:
    custom = "*"

#grabs blockskin count
BSkinpath = resFolder + "\\graphics\\blockskin\\normal"
NumBSkins = len((fnmatch.filter(os.listdir(BSkinpath), '*.png')))
#edits the blockskins in their folders to be sequential to what nullpomino has
for i in range(0,3):
    num = NumBSkins
    skinpath = custom + "blockskin\\small"
    if i == 1:
        skinpath = skinpath + "\\normal"
    if i == 2:
        skinpath = skinpath = "\\big"
    for fileName in os.listdir(skinpath):
        os.renames(fileName, fileName.replace(skinpath[11], skinpath[11] + str(num)))