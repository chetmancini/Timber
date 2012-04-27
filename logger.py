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
# Local Imports
import message_queue
from debug import debug

### Constants ################################################################
USE_QUEUE = False
THREAD_SLEEP_INTERVAL = 1

### Variables ################################################################
connection = None
channel = None
logcount = 0

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
        msg = message_queue.queue.get(True)
        if msg:
            logMessage(msg)
        else:
            break


def loggerInit():
    """
    Start the logging thread.
    """
    worker = ThreadWorker(queueOutput)
    worker.start()



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

            debug("Invalid message" + message.getCode(), error=True)
            raise "Invalid message"

        if connection == None:
            connection = getConnection(client)
        if channel == None:
            channel = getChannel(connection)

        message_queue.producter_pushText(channel, message)
    else:
        if (message.getCode() != "EL") or (message.getCode() != "IL"):

            debug("Invalid message" + message.getCode(), error=True)
            raise "Invalid message"

    try:
        persist.log(
            message.getLevel(), 
            message.getPayload(), 
            True)

        debug("Message logged", success=True)
    except:
        debug("Message not logged!", error=True)

    logcount += 1


def logCount():
    """
    Get the number of logs made on this machine.
    """
    return logcount