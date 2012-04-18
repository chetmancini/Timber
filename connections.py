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
# connections.py                                                             #
# Contains connection information about the current node and the nodes it    #
# communicates with.                                                         #
##############################################################################

### Imports ##################################################################
# Python Library Imports
import uuid
import random

# External Library Imports
import twisted.internet.tcp
import twisted.internet.interfaces
from zope.interface import Interface, implements

# Local Imports
import config
import message
import nodes
from debug import debug

### Classes ##################################################################

class HissConnection(object):
    """
    Functionally extends the twisted client connection.
    Would make sense to extend, but that was difficult, so for now we'll
    use composition instead of inheritence.
    """

    implements(twisted.internet.interfaces.ITCPTransport)
    """
    Implements all the TCPTransport methods.
    """

    def __init__(self, parentNode, client):
        """
        Constructor
        """
        self._client = client
        self._parentNode = parentNode

    @classmethod
    def fromPrimitives(cls, parentNode, host, port, bindAddress, connector):
        """
        Initialize HissTCPConnection from client.
        """
        client = twisted.internet.tcp.Client(host, port, bindAddress, connector)
        return cls(parentNode, client)

    def loseWriteConnection():
        self._client.loseWriteConnection()
    def abortConnection():
        self._client.abortConnection()
    def getTcpNoDelay():
        return self._client.getTcpNoDelay()
    def setTcpNoDelay(enabled):
        self._client.setTcpNoDelay(enabled)
    def getTcpKeepAlive():
        return self._client.getTcpKeepAlive()
    def setTcpKeepAlive(enabled):
        return self._client.setTcpKeepAlive(enabled)
    def getHost():
        return self._client.getHost()
    def getPeer():
        return self._client.getPeer()
    def write(data):
        self._client.write(data)
    def writeSequence(data):
        self._client.writeSequence(data)
    def loseConnection():
        self._client.loseConnection


    def connectionLost(self, reason):
        """
        Callback called when this connection is lost
        """
        super.connectionLost()
        _parentNode.destroyTCPConnection()

    def dispatchMessage(self, msg):
        """
        wrapper for super.write(). Add some sanity checking and debugging.
        """
        self.write(msg.getSerialized())


class HissTCPClientConnection(twisted.internet.tcp.Client):

    def __init__(self, parentNode, client):
        """
        Constructor
        """
        self = client
        self._parentNode = parentNode

    @classmethod
    def fromPrimitives(cls, parentNode, host, port, bindAddress, connector):
        """
        Initialize HissTCPConnection from client.
        """
        client = twisted.internet.tcp.Client(host, port, bindAddress, connector)
        return cls(parentNode, client)


    def connectionLost(self, reason):
        """
        Callback called when this connection is lost
        """
        super.connectionLost()
        debug("Connection lost for reason: " + str(reason))
        _parentNode.destroyTCPConnection()

    def dispatchMessage(self, msg):
        """
        wrapper for super.write(). Add some sanity checking and debugging.
        """
        super.write(msg.getSerialized())




### Constants ################################################################
me = None
"""
Node representing my transport.
"""

universe = {}
"""
Dictionary of nodes in the system. UID -> ExternalNode. Those contain the TCPConnections
"""

neighbors = set([])
"""
set of uids to gossip with.
"""

knownDead = set([])


### Functions ################################################################

def init():
    me = nodes.CurrentNode()

def getMe():
    if me == None:
        init()
    return me

def lookupNode(uid):
    """
    Find a neighbor in the neighbor dict.
    """
    return universe[uid]

def isNeighbor(uid):
    """
    Is the id a neighbor of this node?
    """
    return uid in neighbors

def addNeighbor(uid):
    """
    Add a node to the neighbor set.
    """
    if uid in universe:
        neighbors.add(uid)
        universe[uid].openTCPConnection()


def removeNeighbor(uid):
    """
    Remove a node from the neighbor set
    """
    if uid in neighbors:
        neighbors.remove(uid)

def getNeighbors():
    """
    Return the nodes to gossip with.
    This algorithm might be expanded later. Right now we just have a constant group.
    Theoretically it would try a few and optimize to gossip with the nearest nodes.
    Definitely an area for further design and implementation.
    """
    return neighbors

def getRandomNeighbors(count=5):
    """
    Return a random set of neighbors.
    """
    return random.sample(universe.keys(), count)


def connectToNeighbors():
    """
    Make sure there's a client connection to all our neighbors
    """
    for uid in getNeighbors():
        externalnode = connections.lookupNode(uid)
        if not externalnode.hasTCPConnection():
            debug("opening a client connection")
            externalnode.openTCPConnection()
        else:
            pass #all good.

def connectionMade(client):
    pass

    """def createNode(uid, ip, port):
    create = Node(ip, port, uid)
    addNode(create)
    knownalive.add(uid)
    return create"""

def deadNode(uid):
    """
    Remove a node from the neighbors.
    """
    try:
        neighbors.remove(uid)
        universe.remove(uid)
    finally:
        knownDead.add(uid)

def foundClient(transport):
    """
    When a TCP Connection is created.
    """
    ip = transport.getPeer().host
    for node in universe.values():
        if item.getIp() == ip:
            item.setTCPConnection(transport)
            print "successfully set transport to",ip
            return True

    #### TODO: Create node.
    print "Node",ip,"does not exist yet. Creating it"
    return False

def lostClient(transport):
    """
    When a TCP Connection is lost.
    """
    ip = transport.getPeer().host
    for node in universe.values():
        if item.getIp() == ip:
            item.destroyTCPConnection()
            print "Lost connection with ", ip
            return True
    print "Could not find connection with ",ip,"to lose"
    return False

def createVectorClockMessage():
    """
    Create a new vector clock message
    """
    return getMe().getVectorClock().createMessage()

def globalReset():
    """
    RESENT EVERYTHING BACK TO ZERO!! CAREFUL!!
    """
    pass
    # Todo implement.