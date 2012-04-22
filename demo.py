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
import sys
import os
import subprocess
import argparse
import threading
import time
import fcntl
import select
import random

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

# External Library Imports

# Local Imports
import config
import simpledb

### Constants ################################################################

### Variables ################################################################
nextReceivePort = 0
nextLogPort = 0
nextSendPort = 0

ON_POSIX = 'posix' in sys.builtin_module_names

q = Queue()

colordict = {}

### Classes ##################################################################
class Args(object):
    """
    Holds arguments
    """
    pass

class ThreadWorker(threading.Thread):
    def __init__(self, callable, *args, **kwargs):
        super(ThreadWorker, self).__init__()
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.setDaemon(True)

    def run(self):
        try:
            self.callable(*self.args, **self.kwargs)
        #except wx.PyDeadObjectError:
        #    pass
        except Exception, e:
            print e

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class chetcolors:
    BLACKFG = '\x1b[30m'
    REDFG = '\x1b[31m'
    GREENFG = '\x1b[32m'
    YELLOWFG = '\x1b[33m'
    BLUEFG = '\x1b[34m'
    MAGENTAFG = '\x1b[35m'
    CYANFG = '\x1b[36m'
    WHITEFG = '\x1b[37m'
    DEFAULTFG = '\x1b[39m'
    fgcolors = [BLACKFG, REDFG, GREENFG, 
        YELLOWFG, BLUEFG, MAGENTAFG, CYANFG, WHITEFG]


    BLACKBG = '\x1b[40m'
    REDBG = '\x1b[41m'
    GREENBG = '\x1b[42m'
    YELLOWBG = '\x1b[43m'
    BLUEBG = '\x1b[44m'
    MAGENTABG = '\x1b[45m'
    CYANBG = '\x1b[46m'
    WHITEBG = '\x1b[47m'
    DEFAULTBG = '\x1b[49m'
    bgcolors = [BLACKBG, REDBG, GREENBG, 
        YELLOWBG, BLUEBG, MAGENTABG, CYANBG, WHITEBG]

    @staticmethod
    def randomFGColor():
        return random.choice(chetcolors.fgcolors)

    @staticmethod
    def randomBGColor():
        return random.choice(chetcolors.bgcolors)


### Functions ################################################################
def handleLine(line, header=False):
    isSuccess = line[0] == "*"
    isInfo = line[0] == "-"
    isStrange = line[0] == "?"
    isError = line[0] == "!"

    array = line.split("\t")

    if len(array) < 3:
        print line
        return

    if isSuccess:
        #array[0] = chetcolors.GREENBG + array[0] + chetcolors.DEFAULTBG
        array[0] = bcolors.OKGREEN + array[0] + bcolors.ENDC
        array[2] = bcolors.OKGREEN + array[2] + bcolors.ENDC
    if isError:
        array[0] = bcolors.FAIL + array[0] + bcolors.ENDC
        array[2] = bcolors.FAIL + array[2] + bcolors.ENDC    

    if array[1] in colordict:
        color = colordict[array[1]]
    else:
        colordict[array[1]] = chetcolors.randomBGColor()
        color = colordict[array[1]]
    array[1] = color + "  " + array[1] + "  " + chetcolors.DEFAULTBG

    print '\t'.join(array)

def make_async(fd):
    fcntl.fcntl(
        fd, 
        fcntl.F_SETFL, 
        fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)

def read_async(fd):
    try:
        return fd.read()
    except IOError, e:
        if e.errno != errno.EAGAIN:
            raise e
        else:
            return ''

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
    return process

def createAsyncProcess():
    argList = buildCommandArgs()
    proc = asyncproc.Process(argList)
    return proc

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

### Main #####################################################################

if __name__ == "__main__":
    """
    Run demo application.
    """
    def worker(pipe):
        while True:
            line = pipe.readline()
            if line == '':
                break
            else:
                q.put(line.strip())
    """
    #def enqueue_output(*args):
        #for line in iter(out.readline, b''):
        #    queue.put(line)
        #out.close()
    """

    nextLogPort = config.DEFAULT_LOG_PORT
    nextReceivePort = config.DEFAULT_RECEIVE_PORT
    nextSendPort = config.DEFAULT_SEND_PORT

    simpledb.deleteAll("members")

    args = parse_args()

    processes = []

    for i in range(args.count):
        proc = createProcess()
        stdout_worker = ThreadWorker(worker, proc.stdout)
        stderr_worker = ThreadWorker(worker, proc.stderr)
        stdout_worker.start()
        stderr_worker.start()
        time.sleep(1)
    while True: 
        try:
            line = q.get_nowait()
        except Empty:
            pass
        else:
            handleLine(line)