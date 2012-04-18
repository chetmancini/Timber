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
import messagequeue

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
    if USE_QUEUE:
        if (messageObject.getCode() != "EL") or (messageObject.getCode() != "IL"):
            raise "Invalid message"

        if connection == None:
            connection = getConnection(client)
        if channel == None:
            channel = getChannel(connection)

        messagequeue.producter_pushText(channel, messageObject)
    else:
        if (messageObject.getCode() != "EL") or (messageObject.getCode() != "IL"):
            raise "Invalid message"

        persist.log(messageObject.getLevel(), messageObject.getPayload(), True)

    logcount += 1

def logCount():
    return logcount