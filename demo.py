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
# demo.py                                                                    #
##############################################################################

### Imports ##################################################################
# Python Library Imports
import subprocess
import argparse

# External Library Imports

# Local Imports
import config

### Constants ################################################################

### Variables ################################################################
nextReceivePort = None
nextLogPort = None
nextSendPort = None
nextSendPort = None

### Classes ##################################################################
class Args(object):
    """
    Holds arguments
    """
    pass

### Functions ################################################################

def getNextReceivePort():
    """
    Get the next receive port
    """
    global nextReceivePort
    nextReceivePort += 1
    return nextReceivePort

def getNextLogPort():
    """
    Get the next log port
    """
    global nextLogPort
    nextLogPort += 1
    return nextLogPort

def getNextSendPort():
    """
    Get the next send port
    """
    global nextSendPort
    nextSendPort += 1
    return nextSendPort

def buildCommandArgs():
    """
    Build a command to execute
    """
    toReturn = ['python', 'launch.py']
    toReturn.extend(['--port', str(getNextReceivePort())])
    toReturn.extend(['--logport', str(getNextLogPort())])
    toReturn.extend(['--interval', str(config.DEFAULT_GOSSIP_WAIT_SECONDS)])
    toReturn.extend(['--sendport', str(getNextSendPort())])
    return toReturn

def createProcess():
    """
    Create process and return it.
    """
    argList = buildCommandArgs()
    print "Running: ",' '.join(argList)
    process = subprocess.Popen(argList, 
        shell=False, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
    return p

def handleEvents(process):
    inputstr = ""
    while inputstr:
        if inputstr:
            print inputstr
        inputstr = process.communicate()

def parse_args():
    """
    Parse command line arguments
    """
    arguments = Args()
    parser = argparse.ArgumentParser(
        description="------------Timber/Hiss Settings ----------------",
        epilog="-------------------------------------------------")

    parser.add_argument('--count', 
        default=3, 
        type=int, 
        help='number of nodes to launch')

    parser.parse_args(namespace=arguments)
    return arguments


def run():
    """
    Run demo application.
    """
    global nextLogPort
    global nextReceivePort

    nextLogPort = config.DEFAULT_LOG_PORT
    nextReceivePort = config.DEFAULT_RECEIVE_PORT

    args = parse_args()

    processes = []
    for i in range(args.count):
        p = createProcess()
        processes.append(p)

    while(True):
        for proc in processes:
            handleEvents(proc)



### Main #####################################################################

if __name__ == "__main__":
    run()

