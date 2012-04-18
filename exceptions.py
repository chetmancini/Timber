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
import zope.interface.Interface

### Interface ################################################################
class IError(zope.interface.Interface):
    pass

### Classes ##################################################################
class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    implements(IError)

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