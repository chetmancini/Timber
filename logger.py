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
# logger.py                                                                  #
# contains adaptor logic for logging data                                    #
##############################################################################

### Imports ##################################################################
# Local Imports
import messagequeue
from debug import debug

### Constants ################################################################
USE_QUEUE = False

### Variables ################################################################
connection = None
channel = None
logcount = 0

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

        messagequeue.producter_pushText(channel, message)
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