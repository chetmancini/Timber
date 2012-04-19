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
##############################################################################


### Imports ##################################################################
# Python Library imports
import random

# External library imports

# Local Imports
import simpledb
import connections
import nodes
from debug import debug

### Functions ################################################################
def getRandomWaitTime():
    """
    Generate a random wait time between member refresh operations.
    """
    return random.randint(20000, 60000)

def getPersistedString():
    """
    Get persisted string direct from SDB
    """
    return simpledb.getAttribute(ITEMKEY, ATTRIBUTENAME)

def getCurrentMemberSet():
    """
    Get the local member set.
    """
    return members

### Variables ################################################################
members = set([])
refreshWaitTime = getRandomWaitTime()

### Constants ################################################################
ITEMKEY = "members"
ATTRIBUTENAME = "members_list"
GLUE = "&&&"
### Functions ################################################################
def membersRefresh():
    """
    Run members refresh operation
    """
    global members
    global refreshWaitTime

    try:
        members.clear()
        joined = simpledb.getAttribute(ITEMKEY, ATTRIBUTENAME)
        if (joined != None) and (len(joined) > 0):
            newmembers = joined.split(GLUE)
            for member in newmembers:
                if len(member) > 6:
                    memberNode = nodes.buildNode(member)
                    if connections.getMe().__eq__(memberNode):
                        result = True #Really should send a noop.
                        if result:
                            members.add(memberNode)
                        else:
                            debug("Noop failed. Node removed.", info=True)
        members.add(connections.getMe().getBaseData())
        debug("Members refresh procedure ran.", success=True)
        debug("There are " + str(len(members)) + " in the system.", info=True)
    except:
        debug("Members refresh failed", error=True)

    persistSet()

def persistSet():
    """
    Persist this member set to SimpleDB
    """
    try:
        output = ""
        for member in members:
            output += member.getCompressed() + GLUE
        simpledb.putAttribute(ITEMKEY, ATTRIBUTENAME, output)
        debug("Member set persisted correctly", success=True)
    except:
        debug("Persist set failed", error=True)