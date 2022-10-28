#!/usr/bin/python3

import os, sys, pdb, re
from pathlib import Path

def calculateWpm(newWordCount, oldWordCount, newDate, oldDate):
    return 60.0 * (newWordCount - oldWordCount) / (newDate - oldDate)

if __name__ == "__main__":

    if (len(sys.argv) < 2):
        print("Usage: wpm_monitor.py fileName")
        sys.exit()

    fileName = sys.argv[1]

wordCount = int(os.popen(f"wc -w < {fileName}").read())
dateSeconds = int(os.popen(f"date +%s").read())
dateHuman = os.popen(f"date").read().strip("\n")
fileNameStem = Path(f"./{fileName}").stem
logFile = f".{fileNameStem}_wpm.log"

wpm = "Undefined"

if Path(logFile).is_file():
    with open(logFile, "r") as myfile:
         lastLine = myfile.readlines()[-1]
         res = re.match("^(\d*)\s*(\d*)", lastLine)
         oldWordCount = int(res.group(1))
         oldTime = int(res.group(2))
    
    wpm = calculateWpm(wordCount, oldWordCount, dateSeconds, oldTime)

with open(logFile, "a") as myfile:
    myfile.write(f"{wordCount}\t{dateSeconds}\t{round(wpm, 2)}\t{dateHuman}\n")
