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
# Module for debugging. Can be called directly, which compiles everything    #
# and then gives a total line count. Also handles internal printing.         #
##############################################################################

### Imports ##################################################################

# Python Library Imports
import sys
import os
import string
import traceback

# Local Imports
import config

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

def debug(msg, error=False, success=False, info=False, strange=False):
    """
    Main debug function.
    """
    if type(msg) is str:
        if DEBUG_FLG:
            if error:
                printError("! ERROR:\t" + msg)
            elif success:
                printMessage("* SUCCESS:\t" + msg)
            elif info:
                printMessage("- INFO:\t\t" + msg)
            elif strange:
                printMessage("? STRANGE\t" + msg)
            else:
                printMessage(msg)
        else:
            if error:
                printError("! ERROR:\t" + msg)
    else:
        print "! ERROR", msg
        traceback.print_exc(file=sys.stderr)

def countLinesOfCode():
    """
    Procedure to count total lines of code in each file
    """
    total = 0
    path = '../Timber'
    listing = os.listdir(path)
    for fname in listing:
        if fname[-2:] == "py":
            with open(fname) as f:
                for i, l in enumerate(f):
                    if len(l) > 80:
                        print "line " + str(i) + " of " \
                            + fname + " is too long."
            subtotal = i + 1
            print string.rjust(fname, 25) + "\t" + str(subtotal)
            total += subtotal
    print total

if __name__ == "__main__":
    """
    TEST ALL THE THINGS!!!1!
    """
    import launch
    import nodes
    import gossip
    import logger
    import timber_exceptions
    import vectorClock
    import message
    import messagequeue
    import group_membership
    import simpledb
    import timber_simple
    import timber
    import stats
    import connections
    import aggregation


    countLinesOfCode()