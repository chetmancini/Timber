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

### Functions #######################################################
def logMessage(messageObject):
    """
    Log a messsage
    """
    global logcount
    global channel
    global connection

    if USE_QUEUE:
        if (messageObject.getCode() != "EL") or (messageObject.getCode() != "IL"):

            debug("Invalid message" + messageObject.getCode(), error=True)
            raise "Invalid message"

        if connection == None:
            connection = getConnection(client)
        if channel == None:
            channel = getChannel(connection)

        messagequeue.producter_pushText(channel, messageObject)
    else:
        if (messageObject.getCode() != "EL") or (messageObject.getCode() != "IL"):

            debug("Invalid message" + messageObject.getCode(), error=True)
            raise "Invalid message"

    try:
        persist.log(
            messageObject.getLevel(), 
            messageObject.getPayload(), 
            True)

        debug("Message logged", success=True)
    except:
        debug("Message not logged!", error=True)

    logcount += 1

def logCount():
    return logcount