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
members = set([connections.me])
refreshWaitTime = getRandomWaitTime()

### Constants ################################################################
ITEMKEY = "members"
ATTRIBUTENAME = "members_list"

### Functions ################################################################
def membersRefresh():
    """
    Run members refresh operation
    """
    members.clear()
    joined = simpledb.getAttribute(ITEMKEY, ATTRIBUTENAME)
    if (joined != None) and (len(joined) > 0):
        newmembers = joined.split("&")
        for member in newmembers:
            if len(member) > 6:
                memberNode = Node(member)
                if connections.me.getIp() != memberNode.getIp():
                    result = False #Send NOOP
                    if result:
                        members.add(memberNode)
                    else:
                        print "failed to add node"
    members.add(connections.me)
    persistSet()

def persistSet():
    """
    Persist this member set to SimpleDB
    """
    output = ""
    glue = "&"
    for member in members:
        output += member.toString() + glue
    simpledb.putAttribute(ITEMKEY, ATTRIBUTENAME, output)