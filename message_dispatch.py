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
# message_dispatch.py                                                        #
# Message dispatch objects                                                   #
##############################################################################

### Imports ##################################################################
# Library Imports
import time
import zope.interface
# Local Imports
import config

### Interfaces ###############################################################
class IMessageDispatcher(zope.interface.Interface):
    """
    Message dispatcher interface
    """

    def dispatch(message):
        """
        Dispatch a message
        """

### Classes ##################################################################
class MessageDispatcher:
    """
    Concrete message dispatcher
    """
    zope.interface.implements(IMessageDispatcher)

    def __init__(self):
        """
        Constructor
        """
        pass

    def _hasConnectionTo(self, remote):
        """

        """
        return False

    def dispatch(self, message):
        """
        Not sureo how to make this work...the idea was going to be having
        a basci point to point communication.
        """
        if self._hasConnectionTo(message.getRecipients()):
            self.send(message.getSender(), 
                      message.getRecipient(), 
                      message.getPayload())
        else:
            raise "Connection not valid"