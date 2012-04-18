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
    """
    Print a message to standard error.
    """
    print >>sys.stderr, str(msg)

def logError(msg):
    """
    Log an error message
    """
    printError(msg)

def printMessage(msg):
    """
    Print a message to standard out
    """
    print >>sys.stdout, str(msg)

def logMessage(msg):
    """
    Log a message. (non error)
    """
    printMessage(msg)

def debug(msg, error=False, success=False, info=False):
    """
    Main debug function.
    """
    if DEBUG_FLG:
        if error:
            printError("ERROR:\t" + msg)
        elif success:
            printMessage("SUCCESS:\t" + msg)
        elif info:
            printMessage("INFO:\t" + msg)
        else:
            printMessage(msg)
    else:
        if error:
            printError("ERROR:\t" + msg)

def countLinesOfCode():
    """
    Procedure to count total lines of code.
    """
    total = 0
    path = '../Timber'
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