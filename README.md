# Flagcrack

### What is it?
Flagcrack is used to find flags in files </br>
Flagcrack will check if each line includes the flag </br>
Flagcrack tries multiple different encodings and reverse strings </br>

### How to use it?
-p: path to file with the flag you want to grab </br>
-f: the prefix of the flag you want to grab e.g. picoCTF </br>
</br>
Example:
```bash
flagcrack -p /file.txt -f picoCTF
```

### Install
```bash
wget https://raw.githubusercontent.com/zhiftyDK/flagcrack/main/flagcrack
chmod +x flagcrack
sudo mv flagcrack /bin
```
