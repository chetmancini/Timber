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
domainName = "TIMBER_NODE_LIST"
domainExists = False

sdbConnection = boto.connect_sdb(config.AWS_ACCESS_KEY, config.AWS_SECRET_KEY)

"""sdbConnection = boto.sdb.connection.SDBConnection(
    config.AWS_ACCESS_KEY, 
    config.AWS_SECRET_KEY)"""

### Functions ################################################################
def initDomain():
    """
    Initialize the domain so items can be stored.
    """
    if not domainExists:
        sdbConnection.create_domain(domainName)
        domainExists = True

def putAttribute(item, name, value):
    """
    Push a particular value for item and name, overwriting the old value.
    """
    if not domainExists:
        initDomain()
    toput = boto.sdb.item.Item(domainName, item)
    toput.add_value(name, value)
    sdbConnection.putAttributes(domainName, item, toput, True)

def getAttribute(item, name):
    """
    Get a particular value for an item and name.
    """
    if not domainExists:
        initDomain()
    return sdbConnection.getAttributes(domainName, item, name)

def destroyDomain():
    """
    Delete the domain. Warning, deletes all items as well!
    """
    sdbConnection.delete_domain(domainName)
    domainExists = False