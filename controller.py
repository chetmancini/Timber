##############################################################################
#  .___________. __  .___  ___. .______    _______ .______                   #
#  |           ||  | |   \/   | |   _  \  |   ____||   _  \                  #
#  `---|  |----`|  | |  \  /  | |  |_)  | |  |__   |  |_)  |                 #
#      |  |     |  | |  |\/|  | |   _  <  |   __|  |      /                  #
#      |  |     |  | |  |  |  | |  |_)  | |  |____ |  |\  \----.             #
#      |__|     |__| |__|  |__| |______/  |_______|| _| `._____|             #
#                                                                            #
##############################################################################

#----------------------------------------------------------------------------#
# controller.py                                                              #
#----------------------------------------------------------------------------#

### Imports ##################################################################
import sys
import subprocess


### Functions ################################################################
def doHelp():
    """
    Show a help menu.
    """
    print "'help', 'kill', 'new', 'exit'"

def doExit():
    """
    Exit the applicaiton
    """
    print "Exiting"
    sys.exit()

def doKill():
    """
    Kill a node in the demo app (watches for kill file)
    """
    subprocess.call('touch kill')
    print "Executing kill node request to demo app."

def doNew():
    """
    Create a node in the demo app (watches for new file)
    """
    subprocess.call('touch new')
    print "Executing new node request to demo app"

### Main #####################################################################
if __name__ == "__main__":

    while True:
        inputstr = raw_input("Enter a command ('help'):")

        if inputstr == 'help':
            doHelp()
        elif inputstr == 'kill'
            doKill()
        elif inputstr == 'new':
            doNew()
        elif inputstr == 'exit':
            doExit()