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
# simpledb.py                                                                #
# contains information for keeping track of running instance on simpledb     #
##############################################################################

### Imports ##################################################################
# Python library imports.

# External Library Imports
import boto

# Local Imports
import config
from timber_exceptions import GeneralError
from debug import debug

### Variables ################################################################
sdbConnection = None
sdbDomain = None

### Functions ################################################################
def sdbConnect():
    """
    Connect to SimpleDB
    """
    global sdbConnection

    if not sdbConnection:
        try:
            sdbConnection = boto.connect_sdb(
                config.AWS_ACCESS_KEY,
                config.AWS_SECRET_KEY)
            if sdbConnection:
                debug("Connection to SimpleDB established", success=True)

        except Exception as e:
            debug(e)
            debug("Failed to connect to SimplDB", error=True)
            raise
    else:
        return

def initDomain():
    """
    Initialize the domain so items can be stored.
    """
    global sdbConnection
    global sdbDomain

    sdbConnect()

    if not sdbDomain:
        try:
            sdbDomain = sdbConnection.create_domain(config.AWS_SDB_DOMAIN_NAME)
            debug("SDB Domain " + config.AWS_SDB_DOMAIN_NAME + " created", 
                success=True)

        except Exception as e:
            debug(e)
            debug("Could not create domain on SimpleDB.", error=True)
            raise
    else:
        return

def putAttribute(item, name, value):
    """
    Push a particular value for item and name, overwriting the old value.
    """
    global sdbConnection
    global domainExists

    sdbConnect()
    initDomain()

    try:
        sdbDomain.put_attributes(item, {name:value}, True)
    except Exception as e:
        debug("Failed to PUT item in SimpleDB", error=True)
        debug(e)
        raise

def getAttribute(item, name):
    """
    Get a particular value for an item and name.
    """
    global sdbConnection

    sdbConnect()
    initDomain()

    try:
        return sdbDomain.get_attributes(item, name)[name]
    except Exception as e:
        debug("Failed to GET item from SimpleDB", error=True)
        debug(e)
        raise

def destroyDomain():
    """
    Delete the domain. Warning, deletes all items as well!
    """
    global sdbConnection

    sdbConnect()

    try:
        sdbConnection.delete_domain(config.AWS_SDB_DOMAIN_NAME)
        sdbDomain = None
        return
    except Exception as e:
        debug("Could not delete domain from SimpleDB", error=True)
        debug(e)
        raise