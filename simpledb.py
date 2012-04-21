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
                #debug("Connection to SimpleDB established", success=True)
                print "SimpleDB connection established"
        except Exception as e:
            print e
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
            #debug("SDB Domain " + config.AWS_SDB_DOMAIN_NAME + " created", 
            #    success=True)
            print "Domain created!"

        except Exception as e:
            print e
            raise
    else:
        return

def putSet(item, inputDict):
    #def putAttribute(item, name, value):
    """
    Push a particular value for item and name, overwriting the old value.
    """
    sdbConnect()
    initDomain()

    try:
        if len(inputDict) > 0:
            sdbDomain.put_attributes(item, inputDict, replace=True)
        else:
            #debug("NO INPUT", error=True)
            print "NO INPUT"
    except Exception as e:
        print e
        raise

def getSet(item):
    #def getAttribute(item, name):
    """
    Get a particular value for an item and name.
    """
    sdbConnect()
    initDomain()

    try:
        return sdbDomain.get_attributes(item, consistent_read=True)
    except Exception as e:
        print e
        raise

def deleteSet(item, keys=None):
    """
    Remove keys
    """
    sdbConnect()
    initDomain()

    try:
        sdbDomain.delete_attributes(item, keys)
    except Exception as e:
        print e
        raise

def destroyDomain():
    """
    Delete the domain. Warning, deletes all items as well!
    """
    global sdbConnection
    global sdbDomain

    sdbConnect()

    try:
        sdbConnection.delete_domain(config.AWS_SDB_DOMAIN_NAME)
        sdbDomain = None
        return
    except Exception as e:
        print e
        raise

def deleteAll(item):
    deleteSet(item)