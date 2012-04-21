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
import subprocess
import argparse
import threading
import time

# External Library Imports

# Local Imports
import config
import simpledb

### Constants ################################################################

### Variables ################################################################
nextReceivePort = 0
nextLogPort = 0
nextSendPort = 0

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
        except wx.PyDeadObjectError:
            pass
        except Exception, e:
            print e

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
    #process = subprocess.Popen(argList, 
    #    shell=False, 
    #    stdout=subprocess.PIPE, 
    #    stderr=subprocess.PIPE)
    process = subprocess.Popen(argList, shell=False)
    return process

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
    '''
    def worker(pipe):
        while True:
            line = pipe.readline()
            if line == '': break
            else: print line
    '''

    nextLogPort = config.DEFAULT_LOG_PORT
    nextReceivePort = config.DEFAULT_RECEIVE_PORT
    nextSendPort = config.DEFAULT_SEND_PORT

    simpledb.deleteAll("members")

    args = parse_args()

    processes = []
    for i in range(args.count):
        p = createProcess()
        processes.append(p)
        time.sleep(6)
    '''
    for i in range(args.count):
        proc = createProcess()
        stdout_worker = ThreadWorker(worker, proc.stdout)
        stderr_worker = ThreadWorker(worker, proc.stderr)
        stdout_worker.start()
        stderr_worker.start()
    while True: pass
    '''

    while(True):
        pass
        '''
        for proc in processes:
            stdoutmsg = proc.stdout.read(100)
            stderrmsg = proc.stderr.read(100)
            if len(stdoutmsg) > 0:
                print >>sys.stdout, stdoutmsg
            if len(stderrmsg) > 0:
                print >>sys.stderr, stderrmsg
        '''


