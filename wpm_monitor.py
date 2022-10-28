#!/usr/bin/python3

import os, sys, pdb, re
from pathlib import Path

infVal = 999999999

def calculateWpm(newWordCount, oldWordCount, newDate, oldDate):
    elapsedSeconds = newDate - oldDate
    diffCount = newWordCount - oldWordCount

    if elapsedSeconds == 0:
        if diffCount > 0:
            wpm = infVal
        else:
            wpm = 0
    else:
        wpm = 60.0 * (newWordCount - oldWordCount) / (newDate - oldDate)

    return wpm

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

wpm = "Undef"

if Path(logFile).is_file():
    with open(logFile, "r") as myfile:
         lastLine = myfile.readlines()[-1]
         res = re.match("^(\d*)\s*(\d*)", lastLine)
         oldWordCount = int(res.group(1))
         oldTime = int(res.group(2))
    
    rawWpm = calculateWpm(wordCount, oldWordCount, dateSeconds, oldTime)
    if rawWpm != infVal:
        wpm = round(rawWpm, 2)
    else:
        wpm = "Inf"

with open(logFile, "a") as myfile:
    myfile.write(f"{wordCount}\t{dateSeconds}\t{wpm}\t{dateHuman}\n")


