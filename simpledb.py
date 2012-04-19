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

# External Library Imports
import boto

# Local Imports
import config

### Variables ################################################################
domainExists = False
sdbConnection = None

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
            debug(e, error=True)
            debug("Failed to connect to SimplDB", error=True)

def initDomain():
    """
    Initialize the domain so items can be stored.
    """
    global domainExists

    if not domainExists:
        try:
            sdbConnection.create_domain(config.AWS_SDB_DOMAIN_NAME)
            debug("SDB Domain " + config.AWS_SDB_DOMAIN_NAME + "created", 
                success=True)
            domainExists = True
        except Exception as e:
            debug(e, error=True)
            debug("Could not create domain on SimpleDB.", error=True)

def putAttribute(item, name, value):
    """
    Push a particular value for item and name, overwriting the old value.
    """
    if not sdbConnection:
        sdbConnect()

    if not domainExists:
        initDomain()

    try:
        toput = boto.sdb.item.Item(
            config.AWS_SDB_DOMAIN_NAME, item)

        toput.add_value(name, value)

        sdbConnection.putAttributes(
            config.AWS_SDB_DOMAIN_NAME, item, toput, True)
    except Exception as e:
        debug(e, error=True)
        debug("Failed to PUT item in SimpleDB (" + value + ")", error=True)

def getAttribute(item, name):
    """
    Get a particular value for an item and name.
    """
    if not domainExists:
        initDomain()

    try:
        return sdbConnection.getAttributes(domainName, item, name)
    except:
        debug("Failed to GET item from SimpleDB", error=True)

def destroyDomain():
    """
    Delete the domain. Warning, deletes all items as well!
    """
    sdbConnection.delete_domain(domainName)
    domainExists = False