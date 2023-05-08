#!/usr/bin/env python
import os
import sys
import re
import codecs
import zipfile

# Importing/Installing missing python modules
try: from PIL import Image
except ImportError: 
    os.system("pip install Pillow")
    from PIL import Image
try: import numpy as np
except ImportError: 
    os.system("pip install numpy")
    import numpy as np

# Print the Crackbunny banner
banner = """
         ((`\\
      ___ \\\\ '--._
   .'`   `'    o  )     CRACKBUNNY
  /    \   '. __.'   made by zhiftyDK
 _|    /_  \ \_\_       Copyright ©
{_\______\-'\__\_\\
"""
print(banner)

# getArg returns the argument after the definer
def getArg(argDefiner):
    for index, arg in enumerate(sys.argv):
        if argDefiner == arg:
            return sys.argv[index + 1]

# unzip is used to unzip or crack password encrypted zip files (NOT WORKING!)
def unzip(path):
    try:
        archive = zipfile.ZipFile(path)
        archive.extractall()
        fileNameList = ""
        for file in archive.filelist:
            fileNameList += file.filename + ", "
        print(f"[+] Files found in '{path}': {fileNameList[:-2]}")
        print(f"[+] Extracted files from '{path}'")
    except (zipfile.BadZipFile, RuntimeError) as e:
        if "encrypted" in str(e):
            print(f"[!] Currently unable to handle password protected zip files, use John The Ripper on {path}!")
        else:
            print(f"[!] No embedded files found in '{path}'")

# LSB decoding for images and files, 
def LSBdecode(path):
    fileExtension = path.split(".")[len(path.split(".")) - 1].lower()
    if fileExtension == "png" or fileExtension == "bmp":
        print(f"[+] LSB decoding: '{path}'")
        img = Image.open(path, 'r')
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size//n

        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(0, 3):
                hidden_bits += (bin(array[p][q])[2:][-1])

        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            message += chr(int(hidden_bits[i], 2))
        print("[+] Found hidden message with LSB decoding: " + message)

# Strings looks for specific strings in files, both encoded and reversed
def strings(path):
    def plainText(content, searchString):
        foundMatch = False
        for string in content.split(" "):
            try: 
                if searchString in string:
                    print("[+] Found plaintext string match: " + string)
                    foundMatch = True
            except: pass
            try:
                if searchString in string[::-1]:
                    print("[+] Found reversed plaintext string match: " + string[::-1])
                    foundMatch = True
            except: pass
        if not foundMatch:
            print("[!] Didnt find any matching strings in plaintext!")

    def base64(content, searchString):
        foundMatch = False
        for string in re.sub("[^0-9a-zA-Z+=]+", " ", content).split(" "):
            try: 
                if searchString in codecs.decode(string.encode("ascii"), "base64").decode("ascii"):
                    print("[+] Found base64 encoded string: " + codecs.decode(string.encode("ascii"), "base64").decode("ascii"))
                    foundMatch = True
            except: pass
            try: 
                if searchString in codecs.decode(string[::-1].encode("ascii"), "base64").decode("ascii"):
                    print("[+] Found reversed base64 encoded string: " + codecs.decode(string[::-1].encode("ascii"), "base64").decode("ascii"))
                    foundMatch = True
            except: pass
        if not foundMatch:
            print("[!] Didnt find any base64 encoded strings!")

    def rot13(content, searchString):
        foundMatch = False
        for string in content.split(" "):
            try:
                if searchString in codecs.decode(string, "rot13"):
                    print("[+] Found rot13 encoded string: " + codecs.decode(string, "rot13"))
                    foundMatch = True
            except:
                pass
            try:
                if searchString in codecs.decode(string[::-1], "rot13"):
                    print("[+] Found reversed rot13 encoded string: " + codecs.decode(string[::-1], "rot13"))
                    foundMatch = True
            except:
                pass
        if not foundMatch:
            print("[!] Didnt find any rot13 encoded strings!")

    searchString = getArg("-s") or False
    with open(path, encoding="utf8", errors='ignore') as f:
        content = f.read().replace("\n", "")
        if searchString:
            print(f"[+] Looking for strings matching '{searchString}', in the data of '{path}'")
            plainText(content, searchString)
            base64(content, searchString)
            rot13(content, searchString)
        else:
            print(f"[!] Couldnt run strings method on '{path}' since no searchstring was defined!")

# Directory search for all files in a directory and passes them to the filehandler
def directory(path):
    dirContent = [f for f in os.listdir(path)]
    for member in dirContent:
        memberPath = os.path.join(path, member)
        if os.path.isfile(memberPath):
            fileHandler(memberPath)
        elif os.path.isdir(memberPath):
            directory(memberPath)

# File handler, detects specific type of file and starts actions
def fileHandler(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            directory(path)
        elif os.path.isfile(path):
            LSBdecode(path)
            strings(path)
            unzip(path)
    else:
        print(f"[!] The filepath: {path} is not valid!")

# Initialise flagcrack
filePath = getArg("-f") or False
if filePath:
    fileHandler(filePath)
elif "-h" in sys.argv or "--help" in sys.argv:
    print("Crackbunny is used to find strings or hidden information in files and directories")
    print("Crackbunny's capabilities: LSB decoding, Unzipping/binwalking & finding encoded string matches")
    print("")
    print("-p: <file/directory path> Path of the file or directory you want to crack")
    print("-s: <string> String that you want to look for in files")
    print("-c: <string> String that you want to crack")
    print("Example: crackbunny -f /file.txt -s picoCTF")
else:
    print("[!] For help type: crackbunny -h")