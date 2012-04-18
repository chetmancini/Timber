##############################################################################
#                                                                            #
#  .___________. __  .___  ___. .______    _______ .______                   #
#  |           ||  | |   \/   | |   _  \  |   ____||   _  \                  #
#  `---|  |----`|  | |  \  /  | |  |_)  | |  |__   |  |_)  |                 #
#      |  |     |  | |  |\/|  | |   _  <  |   __|  |      /                  #
#      |  |     |  | |  |  |  | |  |_)  | |  |____ |  |\  \----.             #
#      |__|     |__| |__|  |__| |______/  |_______|| _| `._____|             #
#                                                                            #
#----------------------------------------------------------------------------#
# debug.py                                                                   #
##############################################################################

### Imports ##################################################################
import sys
import os

### Globals ##################################################################
DEBUG_FLG = True

### Functions ################################################################
def printError(msg):
    print >>sys.stderr, str(msg)

def logError(msg):
    printError(msg)

def printMessage(msg):
    print >>sys.stdout, str(msg)

def logMessage(msg):
    printMessage(msg)

def debug(msg):
    if DEBUG_FLG:
        printMessage(msg)

def countLinesOfCode():
    total = 0
    path = '../Python'
    listing = os.listdir(path)
    for fname in listing:
        if fname[-2:] == "py":
            with open(fname) as f:
                for i, l in enumerate(f):
                    pass
            total += i + 1
    print total

if __name__ == "__main__":
    countLinesOfCode()