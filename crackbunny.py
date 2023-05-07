#!/usr/bin/env python
import os
import sys
import re
import codecs
try: from PIL import Image
except ImportError: os.system("pip install Pillow")
try: import numpy as np
except ImportError: os.system("pip install numpy")
try: from tqdm import tqdm
except ImportError: os.system("pip install tqdm")
try: import zipfile_deflate64 as zipfile
except ImportError: os.system("pip install zipfile-deflate64")

codecs.ascii_decode

# Print the Flagcrack banner
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
    zipArchive = zipfile.ZipFile(path, mode="r", compression=zipfile.ZIP_DEFLATED64)
    try:
        print("[+] Unzipping zip archive!")
        for fileNames in list(zipArchive.filelist):
            with zipArchive.open(fileNames[0], mode="r", pwd=str.encode("password")) as memberArchive:
                print(memberArchive.read().decode("utf-8"))
        os.remove(path)
    except:
        print("[!] Zip archive is password protected, cracking the password!")
        # wordlist = "rockyou.txt"
        # n_words = len(list(open(wordlist, "rb")))
        # with open(wordlist, "rb") as wordlist:
        #     for word in tqdm(wordlist, total=n_words, unit="word"):
        #         try:
        #             with pyzipper.AESZipFile(path, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
        #                 extracted_zip.extractall(pwd=str.encode("password"))
        #         except:
        #             continue
        #         else:
        #             print("[+] Password found: ", word.decode().strip())
        #             os.remove(path)
        print(f"[!] Password to: {path} not found.")

# LSB decoding for images and files, 
def LSBdecode(path):
    print(f"[+] LSB decoding: {path}")
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
            print(f"[+] Looking for strings matching '{searchString}', in the data of {path}")
            plainText(content, searchString)
            base64(content, searchString)
            rot13(content, searchString)
        else:
            print("[!] Couldnt run strings method on file since no searchstring was defined!")


# File handler, detects specific type of file and starts actions
def fileHandler(path):
    if os.path.exists(path):
        fileExtension = path.split(".")[len(path.split(".")) - 1].lower()
        if os.path.isdir(path):
            print("[+] Path is directory")
        elif os.path.isfile(path):
            if fileExtension == "png" or fileExtension == "bmp":
                LSBdecode(path)
                strings(path)
            elif fileExtension == "zip":
                print("[!] Currently unable to handle zip files, if its password protected use John The Ripper!")
            else:
                strings(path)
    else:
        print("[!] The specified filepath is not valid!")

# Initialise flagcrack
filePath = getArg("-f") or False
if filePath:
    fileHandler(filePath)
elif "-h" in sys.argv or "--help" in sys.argv:
    print("Flagcrack is used to find flags in files")
    print("Flagcrack will check if each line includes the flag")
    print("Flagcrack tries multiple different encodings and reverse strings")
    print("")
    print("-p: path to file with the flag you want to grab")
    print("-f: the prefix of the flag you want to grab e.g. picoCTF")
    print("")
    print("Example: flagcrack -p /file.txt -f picoCTF")
else:
    print("[!] For help type: crackbunny -h")