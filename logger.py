##############################################################################
#  .___________. __  .___  ___. .______    _______ .______                   #
#  |           ||  | |   \/   | |   _  \  |   ____||   _  \                  #
#  `---|  |----`|  | |  \  /  | |  |_)  | |  |__   |  |_)  |                 #
#      |  |     |  | |  |\/|  | |   _  <  |   __|  |      /                  #
#      |  |     |  | |  |  |  | |  |_)  | |  |____ |  |\  \----.             #
#      |__|     |__| |__|  |__| |______/  |_______|| _| `._____|             #
#                                                                            #
##############################################################################

### Imports ##################################################################
# Python Library imports
import threading
import time

# Local Imports
import message_queue
import persist
from debug import debug

### Constants ################################################################
USE_QUEUE = False
THREAD_SLEEP_INTERVAL = 1

### Variables ################################################################
connection = None
channel = None
logcount = 0

worker = None

### Classes ##################################################################
class ThreadWorker(threading.Thread):
    """
    Threadworker
    """

    def __init__(self, callable, *args, **kwargs):
        """
        Constructor
        """
        super(ThreadWorker, self).__init__()
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.setDaemon(True)

    def run(self):
        """
        Run the thread.
        """
        try:
            self.callable(*self.args, **self.kwargs)
        except Exception, e:
            print e

def queueOutput():
    """
    grab items off the queue
    """
    while True:
        try:
            debug("Waiting", info=True)
            msg = message_queue.queue.get(True, 5)
            if msg:
                debug("Received Message. Logging...",success=True)
                logMessage(msg)
            else:
                time.sleep(3)
                debug("Did not receive message. Sleeping",info=True)
        except:
            pass


def loggerInit():
    """
    Start the logging thread.
    """
    global worker
    worker = ThreadWorker(queueOutput)
    worker.start()
    debug("Logger initialized", success=True)
    return

### Functions ################################################################
def logMessage(message):
    """
    Log a messsage.
    """
    global logcount
    global channel
    global connection

    if USE_QUEUE:
        if (message.getCode() != "EL") or (message.getCode() != "IL"):

            debug("Invalid message " + message.getCode(), error=True)
            raise "Invalid message "

        if connection == None:
            connection = getConnection(client)
        if channel == None:
            channel = getChannel(connection)

        message_queue.producter_pushText(channel, message)
    else:
        if message.getCode() not in ["EL","IL"]:

            debug("Invalid message " + message.getCode(), error=True)
            raise "Invalid message "

    try:
        if len(message.getPayload()) > 1:
            persist.log(
                message.getType(),
                message.getPayload(),
                message.getLevel(),
                True)
            debug("Message logged", success=True)
        else:
            debug("Message empty", error=True)
    except Exception,e:
        debug(e)
        debug("Message not logged!", error=True)

    logcount += 1


def logCount():
    """
    Get the number of logs made on this machine.
    """
    return logcount