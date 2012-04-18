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
# node.py                                                                    #
# Node objects                                                               #
##############################################################################

### Imports ##################################################################
# Library imports
import random
import uuid
import socket
import cPickle

# External Library imports
import zope.interface
import twisted.internet.tcp

# Local Imports
import config
import connections
import vectorClock

### Classes ##################################################################
class INode(zope.interface.Interface):

    def getIp():
        """
        Get this nodes IP address
        """

    def getPort():
        """
        Get this node's port
        """

    def getUid():
        """
        Get this node's UID as a hexadecimal string
        """

    def getUidAsObject():
        """
        Get this node's uid as a python UID object.
        """

    def getSerialized():
        """
        Get this node in a serialized form
        """


class BaseNode(object):
    """
    Base class for all other nodes. Minimal to implement interface.
    """

    zope.interface.implements(INode)

    def __init__(self, ip, port=None, uid=None):
        """
        Constructor
        """
        self._ip = ip
        self._port = port
        if uid:
            self._uid = uid
        else:
            self._uid = uuid.uuid1()

    def getIp(self):
        """
        Get the ip for this connection.
        """
        return self._ip

    def getPort(self):
        """
        get the port for this connection
        """
        return self._port

    def getUidAsObject(self):
        """
        get the unique identifier
        """
        return self._uid

    def getUid(self):
        """
        Return the uid as a hex string.
        """
        return self._uid.hex

    def getSerialized(self):
        return cPickle.dumps(self)



class ExternalNode(BaseNode):
    """
    A node of an external node.
    """

    def __init__(self, ip, port, uid=None):
        """
        Constructor
        """
        super(ExternalNode, self).__init__(ip, port, uid)
        self._tcpConnection = None
        self._knownAlive = True

    def openTCPConnection(self):
        """
        Open a new TCP connection from the local node to this node.
        """
        #tcpConnection = connections.HissTCPClientConnection(self, )
        pass

    def setTCPConnection(self, tcpConnection):
        """
        Assign a TCP connection to this node.
        """
        self._tcpConnection = connections.HissTCPClientConnection(self, tcpConnection)

    def getTCPConnection(self):
        """
        return the TCP Connection (twisted Client) to this node.
        """
        if not self.hasTCPConnection():
            self.openTCPConnection()
        return self._tcpConnection

    def hasTCPConnection(self):
        """
        Return if a TCP Connection to this node exists.
        """
        return (self.tcpConnection is not None)

    def destroyTCPConnection(self):
        """
        Destroy the TCP connection 
        """
        if self.hasTCPConnection():
            self.getTCPConnection().loseConnection()
        self._tcpConnection = None




class CurrentNode(BaseNode):
    """
    Wrapper class to represent current node.
    """

    def __init__(self, ip=None, port=None):
        """
        Constructor
        """
        if ip == None:
            ip = socket.gethostbyname(socket.gethostname())
        super(CurrentNode, self).__init__(ip, port, None)

        self._vectorClock = vectorClock.VectorClock(self.getUid())

    def getVectorClock(self):
        """
        get the vector clock at this position.
        """
        return self._vectorClock

    def getBaseData(self):
        return BaseNode(self.getIp(), self.getPort(), self.getUid())


class DoorNode(BaseNode):
    """
    Node that acts as entryway. Only used in entryway code.
    """

    def __init__(self, doornodeip, doornodeport, uid=None):
        """
        constructor
        """
        super(DoorNode, self).__init__(doornodeip, doornodeport, uid)
        self._nodes = {}

    def randomnodes(self, count):
        """
        Get random nodes from the set
        """
        count = min(count, self._nodes.size()) #handle bad input error case.
        return random.sample(self._nodes.keys(), count)

    def addNode(self, node):
        """
        Add a node to the connection pool
        """
        self._nodes.add(node.getId(), node)

    def nodeDead(self, nodeid):
        """
        Notify doorkeeper of a bad node.
        """
        self._nodes.remove(nodeid)

### Functions ################################################################

def buildNode(nodestr):
    """
    Build a node from serialized form
    """
    return cPickle.loads(nodestr)