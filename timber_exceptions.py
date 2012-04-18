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
# exceptions.py                                                              #
##############################################################################

### Imports ##################################################################

### Classes ##################################################################
class Error(Exception):
    """
    Base class for exceptions in this module.
    """

    def __init__(self, value):
        """
        Constructor
        """
        self._value = value

    def __str__(self):
        """
        Get string representation
        """
        return repr(self._value)

class GeneralError(Error):
    """
    General errors
    """
    def __init__(self, value):
        """
        Constructor
        """
        super(GeneralError, self).__init__(value)

class ConnectionError(Error):
    """
    Connection errors.
    """
    pass

class InvalidPeerIDError(Error):
    """
    Invalid peer id (UID doesnt exist)
    """
    pass

class InvalidAddressError(Error):
    """
    Invalid IP address exception
    """
    pass

class InvalidPortError(Error):
    """
    Invalid port exception
    """
    pass

class UnknownUidError(Error):
    """
    Unknown UID exception
    """
    pass