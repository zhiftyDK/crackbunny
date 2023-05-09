# Flagcrack

## What is it?
Flagcrack is used to find flags in files </br>
Flagcrack will check if each line includes the flag </br>
Flagcrack tries multiple different encodings and reverse strings </br>

## How to use it?
-p: path to file with the flag you want to grab </br>
-f: the prefix of the flag you want to grab e.g. picoCTF </br>
</br>
Example:
```bash
flagcrack -p /file.txt -f picoCTF
```
Output:
```bash
         ((`\
      ___ \\ '--._
   .'`   `'    o  )     CRACKBUNNY
  /    \   '. __.'   made by zhiftyDK
 _|    /_  \ \_\_       Copyright ©
{_\______\-'\__\_\

[-] Didnt find any matching strings in plaintext
[+] Found reversed base64 encoded string: picoCTF{Flagcrack_Is_The_Best_Tool}
[-] Didnt find any rot13 encoded strings
[-] Didnt find any MD5 hashed strings
[-] Didnt find any SHA256 hashed strings
[-] No embedded files found in 'file.txt'

```

## Install
```bash
wget https://raw.githubusercontent.com/zhiftyDK/flagcrack/main/flagcrack
chmod +x flagcrack
sudo mv flagcrack /bin
```

## Update
```bash
sudo rm /bin/flagcrack
wget https://raw.githubusercontent.com/zhiftyDK/flagcrack/main/flagcrack
chmod +x flagcrack
sudo mv flagcrack /bin
```
