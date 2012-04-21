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
import sys
import traceback

# External library imports

# Local Imports
import simpledb
import connections
import nodes
from debug import debug

### Variables ################################################################
members = {}
members_to_delete = set([])

### Constants ################################################################
ITEMKEY = "members"
#ATTRIBUTENAME = "members_list"
#GLUE = "&&&"

### Functions ################################################################
def getRandomWaitTimeMillis():
    """
    Generate a random wait time between member refresh operations.
    """
    return random.randint(20000, 60000)

def getRandomWaitTimeSecs():
    """
    Generate a random wai ttime between member refresh ops
    """
    return random.randint(15, 40)

def getPersistedString():
    """
    Get persisted string direct from SDB
    """
    return simpledb.getAttribute(ITEMKEY, ATTRIBUTENAME)

def getCurrentMemberDict():
    """
    Get the local member set.
    """
    return members

### Functions ################################################################
def membersRefresh():
    """
    Run members refresh operation
    """
    global members

    try:
        for key in members:
            members_to_delete.add(key)
        members.clear()

        newMembersDict = simpledb.getSet(ITEMKEY)
        if (newMembersDict != None) and (len(newMembersDict) > 0):
            #newmembers = joined.split(GLUE)
            for memberUid in newMembersDict:
                if len(memberUid) > 6:
                    memberNode = nodes.buildNode(newMembersDict[memberUid])
                    if not connections.getMe().__eq__(memberNode):
                        result = True #Really should send a noop.
                        if result:
                            members[memberNode.getUid()] = memberNode
                        else:
                            debug("Noop failed. Node removed.", info=True)
                    else:
                        pass
        members[connections.getMe().getUid()] = connections.getMe().getBaseData()

        for key in members:
            if key in members_to_delete:
                members_to_delete.remove(key)

        debug("Members refresh procedure ran.", success=True)
        debug("There are " + str(len(members)) + " members in the system.", 
            info=True)
    except Exception as e:
        print e
        traceback.print_exc(file=sys.stdout)
        debug("Members refresh failed", error=True)

    persistSet()

def persistSet():
    """
    Persist this member set to SimpleDB
    """
    try:
        toWrite = {}
        for member in members:
            toWrite[member] = members[member].getCompressed()
        #output = ""
        #for member in members:
        #    output += member.getCompressed() + GLUE
        debug("String to persist built", info=True)
        simpledb.putSet(ITEMKEY, toWrite)
        if len(members_to_delete) > 0:
            simpledb.deleteSet(ITEMKEY, members_to_delete)
            debug("DELETing members", info=True)
        debug("Member set persisted correctly", success=True)

    except:
        traceback.print_exc(file=sys.stdout)
        debug("Persist set failed", error=True)